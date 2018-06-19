Title: LEDE路由器打造家庭媒体影音中心（一）
Date: 2018-06-15 13:07
Category: IT笔记
Tags: openwrt, samba, nas
Slug:lede-media-center1
Authors: Kevin Chen
Status: draft



### 前言

### 更换源



### USB驱动

**查看已安装的驱动**
```
opkg update
opkg list-installed | grep usb
```
**安装驱动和工具**

如果下列驱动未出现在上一步的结果中，请务必首先安装缺失的驱动

```
opkg install kmod-usb-core kmod-usb-storage kmod-ata-marvell-sata
```

`kmod-usb-core`:USB核心驱动

`kmod-usb-storage`:非高速usb-storage设备，高速设备驱动是[UAS](https://en.wikipedia.org/wiki/USB_Attached_SCSI)，已编译在内核中

`kmod-usb2`:WRT1900ACS有一个USB2.0/eSATA口，只用到eSATA未用到USB2.0，所以不安装这个驱动，如果需要也可以安装

`kmod-ata-marvell-sata`:Marvell SATA接口驱动

网上搜到的教程和官方指南里还让安装一些其他的应用，但这些都是不必要或已被编译至内核中，包括：`kmod-usb-ohci`、`kmod-usb-uhci`、`kmod-usb3`

*小技巧：如何分辨uas设备和usb-storage设备*

`lsusb -t`

```
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/6p, 5000M
    |__ Port 2: Dev 3, If 0, Class=Mass Storage, Driver=uas, 5000M
    |__ Port 4: Dev 5, If 0, Class=Mass Storage, Driver=usb-storage, 5000M
```

Dev 3就是uas，Dev 5就是usb-storage，如果返回的结果类似于下面这样，Driver为空，那么就是驱动没有安装好。

```
|__ Port 4: Dev 5, If 0, Class=Mass Storage, Driver=, 5000M
```



**安装相关工具**

```bash
opkg install mount-utils usbutils block-mount e2fsprogs kmod-fs-ext4 gdisk fdisk 
```
`mount-utils`:提供unmount,findmnt

`usbutils`:提供lsusb

`block-mount`:提供block，查看挂载点信息

`e2fsprogs`:格式化工具mkfs

`kmod-fs-ext4`:格式化为ext4格式

`kmod-fs-ntfs`:我不用ntfs格式，所以不安装这个，需要可以安装上

`gdisk`:分区工具，支持GPT，硬盘容量超过2T需要用这个工具，当然容量小的也可以用这个

`fdisk`:分区工具，不支持GPT，常用来查看分区信息

查看已连接的USB设备

```bash
lsusb -t
ls -l /dev/sd*
block info | grep "/dev/sd"
```

*小提示：硬盘格式化为什么格式最好？*

在Linux和LEDE平台上，微软的NTFS和FAT绝对不是一个好的格式，设计的优劣不谈，这两个格式不是Linux平台原生支持的，安装额外的驱动可能会带来发热、速度慢、不稳定等多种负面效果。所以，对于机械硬盘来说，EXT4和BTRFS是最好的，对于SSD来说，F2FS格式是最好的。

### 硬盘相关操作

**硬盘分区**

根据软件提示进行操作
```bash
gdisk /dev/sda
```
这里我把一块硬盘分为两个区`/dev/sda1`，`/dev/sda2`，分区1大小700G，分区2大小231G，总计1T。

**格式化硬盘**

```bash
mkfs.ext4 /dev/sda1
mkfs.ext4 /dev/sda2
```
如果是SSD硬盘，则可以按照如下方式安装操作
```bash
opkg install f2fs-tools
opkg install kmod-fs-f2fs
mkfs.f2fs /dev/sda1
```

**自动挂载分区**
```bash
block detect > /etc/config/fstab
uci set fstab.@mount[0].enabled='1'
uci set fstab.@mount[1].enabled='1'
uci set fstab.@mount[0].options='rw'
uci set fstab.@mount[1].options='rw'
uci set fstab.@global[0].check_fs='1'
uci commit
```
查看当前挂载点设置
```bash
uci show fstab
```

**开启/重启挂载服务**

```
service fstab restart
service fstab enable
```



**[可选]硬盘休眠**

```bash
opkg update
opkg install hdparm luci-app-hd-idle
```
执行下面的命令启动休眠
```bash
hdparm -S 120 /dev/sda1
hdparm -S 120 /dev/sda2
```

-S后的参数含义为：
1. 0:关闭休眠
2. 1-240：数字乘以5秒是时间，在设定时间内未使用则休眠
3. 241-251：以30分钟为步进，时间为30分钟-5.5小时



测试硬盘读取性能

```bash
hdparm -Tt /dev/sda1
hdparm -Tt /dev/sda2
```



如果不想按照上面一步一步来，那么官方也提供了快速操作，请根据自己的实际情况修改后执行。

```bash
# Copy/paste each line below, then press Return
opkg update && opkg install block-mount e2fsprogs kmod-fs-ext4 kmod-usb3 kmod-usb2 kmod-usb-storage
mkfs.ext4 /dev/sda1
block detect > /etc/config/fstab 
uci set fstab.@mount[0].enabled='1' && uci set fstab.@global[0].check_fs='1' && uci commit 
/sbin/block mount && service fstab enable
```



### 配置Samba

**安装Samba**

查看可安装的版本

```bash
opkg update
opkg list | grep samba
```

根据结果，安装适当的版本

```bash
opkg install samba36-server luci-app-samba luci-i18n-samba-zh-cn
```

**配置防火墙**

` vi /etc/config/firewall`

```ini
config 'rule'
        option 'src' 'lan'
        option 'proto' 'udp'
        option 'dest_port' '137-138'
        option 'target' 'ACCEPT'

config 'rule'
        option 'src' 'lan'
        option 'proto' 'tcp'
        option 'dest_port' '139'
        option 'target' 'ACCEPT'

config 'rule'
        option 'src' 'lan'
        option 'proto' 'tcp'
        option 'dest_port' '445'
        option 'target' 'ACCEPT'
```

**Samba配置文件**

*官方**强烈建议**使用luci来配置Samba，然后通过修改临时文件来完成配置。*

*路由器每次重启，`/etc/samba/smb.conf`文件都将从/etc/samba/smb.conf.template文件从新创建，所以修改配置时请修改后者。*

`vi /etc/samba/smb.conf.template`

```bash
[global]
	netbios name = |NAME| 
	workgroup = |WORKGROUP|
	server string = |DESCRIPTION|
	syslog = 10
	encrypt passwords = true
	passdb backend = smbpasswd
	obey pam restrictions = yes
	socket options = TCP_NODELAY
	unix charset = UTF-8
    local master = yes #For Browsing shares folders
	preferred master = yes #For Browsing shares folders
	os level = 20
	security = share
	guest account = nobody
	invalid users = root #禁止root用户登录访问
	smb passwd file = /etc/samba/smbpasswd
```



`vi /etc/config/samba `

```bash
config 'samba'
        option 'name' 'OpenWrt'
        option 'workgroup' 'OpenWrt'
        option 'description' 'Samba on OpenWrt'
        option 'charset' 'UTF-8'
        option 'homes' '0'
        option 'interface' 'loopback lan'
        
config 'mediashare'
        option 'name' 'Shares'
        option 'path' '/mnt/sda1'
        option 'guest_ok' 'yes'
        option 'create_mask' '0777'
        option 'dir_mask' '0777'
        option 'read_only' 'no'
        
config 'fileshare'
        option 'name' 'Files'
        option 'path' '/mnt/sda2'
        option 'guest_ok' 'yes'
        option 'create_mask' '0777'
        option 'dir_mask' '0777'
        option 'read_only' 'no'
```




### 参考链接
[Installing USB Drivers](https://openwrt.org/docs/guide-user/storage/usb-installing)

[Using storage devices](https://openwrt.org/docs/guide-user/storage/usb-drives)
[Share USB Hard-drive with Samba using the Luci web-interface](https://openwrt.org/docs/guide-user/services/nas/usb-storage-samba-webinterface)
[SMB Samba share overview](https://openwrt.org/docs/guide-user/services/nas/samba_configuration)

[cifs.server](https://openwrt.org/docs/guide-user/services/nas/cifs.server)

[Samba](https://openwrt.org/docs/guide-user/services/nas/samba)

<hr />
[智能路由器-OpenWRT 系列五 （NAS-SMB家庭共享）](https://www.cnblogs.com/wizju/p/6923625.html)

[OpenWrt搭建文件共享服务（NAS）](https://www.jianshu.com/p/a122a036e8d9)

[Openwrt 网络存储NAS之Samba服务](https://blog.csdn.net/yicao821/article/details/49929207)

[【智能路由】用路由器低成本打造NAS+迅雷离线下载+同步android文件](https://luolei.org/openwrt-router-wifi-android-sync-iclould/)

[基于OpenWrt打造NAS以及脱机下载中心](https://blog.zlf.me/%E5%9F%BA%E4%BA%8EOpenWrt%E6%89%93%E9%80%A0NAS%E4%BB%A5%E5%8F%8A%E8%84%B1%E6%9C%BA%E4%B8%8B%E8%BD%BD%E4%B8%AD%E5%BF%83.html)
