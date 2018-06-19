Title: openwrt-samba2
Date: 2018-06-15 13:07
Category: IT笔记, 金融笔记
Tags: openwrt, samba, nas
Slug:openwrt-samba2
Authors: Kevin Chen
Status: draft

### USB驱动
**查看已安装的驱动**
```
opkg update
opkg list-installed | grep usb
```
**安装驱动和工具**

如果下列驱动未出现在上一步的结果中，请务必首先安装缺失的驱动
```
opkg install kmod-usb-core kmod-usb-storage kmod-usb2 kmod-ata-marvell-sata kmod-usb-storage-extras
```

**安装相关工具**
```bash
opkg install mount-utils #提供unmount,findmnt
opkg install usbutils #提供lsusb
opkg install block-mount #查看挂载点信息
opkg install e2fsprogs #格式化工具mkfs
opkg install kmod-fs-ext4
#opkg install kmod-fs-ntfs #我不用ntfs格式，所以不安装这个
opkg install gdisk #分区工具
opkg install fdisk #分区工具，安装上一个就不用安装这个了
```
查看已连接的USB设备
```bash
lsusb -t
ls -l /dev/sd*
block info | grep "/dev/sd"
```


### 硬盘相关操作
**硬盘分区**

根据软件提示进行操作
```bash
gdisk /dev/sda
```
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



如果不想按照上面一步一步来，那么官方也提供了快速操作

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
