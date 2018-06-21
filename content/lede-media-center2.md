Title: LEDE/OpenWRT路由器打造家庭媒体影音中心（二）
Date: 2018-06-15 13:07
Category: IT笔记
Tags: openwrt, lede,wrt1900acs,samba, nas
Slug:lede-media-center2
Authors: Kevin Chen
Status: draft





# USB驱动

### 查看已安装的驱动

```
opkg update
opkg list-installed | grep usb
```



### 安装驱动和工具

如果下列驱动未出现在上一步的结果中，请务必首先安装缺失的驱动

```
opkg install kmod-usb-core kmod-usb-storage kmod-usb2 kmod-ata-marvell-sata
```

`kmod-usb-core`:USB核心驱动

`kmod-usb-storage`:大容量存储设备驱动

`kmod-usb2`:WRT1900ACS有一个USB2.0/eSATA口

`kmod-ata-marvell-sata`:Marvell SATA接口驱动

网上搜到的教程和官方指南里还让安装一些其他的应用，但这些都是不必要或已被编译至内核中，包括：`kmod-usb-ohci`、`kmod-usb-uhci`、`kmod-usb3`、`kmod-usb-storage-uas`



### 安装相关工具

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



以下几个命令查看已连接/挂载的USB设备

```bash
df -h
lsusb -t
ls -l /dev/sd*
block info | grep "/dev/sd"
```

*小提示：硬盘格式化为什么格式最好？*

在Linux和LEDE平台上，微软的NTFS和FAT32绝对不是一个好的格式，设计的优劣不谈，这两个格式不是Linux平台原生支持的，安装额外的驱动可能会带来发热、读写速度慢、不稳定等多种负面效果。所以，对于机械硬盘来说，EXT4和BTRFS是最好的，对于SSD来说，F2FS格式是最好的。



# 硬盘相关操作

### 硬盘分区

```bash
gdisk /dev/sda
```

根据软件提示进行操作，主要命令有：

`n`:新建分区

`w`:保存分区内容

`d`:删除分区

`p`:打印分区列表

`?`:查看帮助



这里我把一块硬盘分为两个区`/dev/sda1`，`/dev/sda2`，分区1大小700G，分区2大小231G，总计1T。



### 格式化硬盘

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



### 自动挂载分区

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

**卸载/挂载服务**

```
block umount && block mount
```



### 硬盘休眠

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



如果不想按照上面一步一步来，那么官方也提供了快速操作，请根据自己的实际情况修改后执行。

```bash
# Copy/paste each line below, then press Return
opkg update && opkg install block-mount e2fsprogs kmod-fs-ext4 kmod-usb3 kmod-usb2 kmod-usb-storage
mkfs.ext4 /dev/sda1
block detect > /etc/config/fstab 
uci set fstab.@mount[0].enabled='1' && uci set fstab.@global[0].check_fs='1' && uci commit 
/sbin/block mount && service fstab enable
```



# Samba

### 安装Samba

查看可安装的版本

```bash
opkg update
opkg list | grep samba
```

根据结果，安装适当的版本

```bash
opkg install samba36-server luci-app-samba luci-i18n-samba-zh-cn
```



### 配置防火墙

` vim /etc/config/firewall`

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



### Samba配置

*官方**强烈建议**使用luci来配置Samba，然后通过修改临时文件来完成配置。*

*路由器每次重启，`/etc/samba/smb.conf`文件都将从`/etc/samba/smb.conf.template`文件重新创建，所以修改配置时请修改后者。*



全局和共享配置可以在LuCi界面编辑也可以直接编辑文件，按照我的配置实现如下几个功能：

- 禁止root用户访问，防止权限出现问题
- 允许匿名用户访问`/mnt/sda1`，即Media文件夹
- 访问`/mnt/sda2`，即Document文件夹必须登录，用户只能访问到自己创建的文件夹和文件



#### **全局配置**

`vim /etc/samba/smb.conf.template`

```bash
[global]
    #netbios name = LEDE  #不设置默认是路由器host名
    #workgroup = LEDE #不设置默认是WORKGROUP
	server string = Samba on LEDE
	syslog = 5
	encrypt passwords = true
	socket options = TCP_NODELAY IPTOS_LOWDELAY
	unix charset = UTF-8 
	browseable = yes
    local master = yes
	preferred master = yes
	security = user
	null passwords = yes
	guest account = nobody
	invalid users = root
	passdb backend = smbpasswd
	smb passwd file = /etc/samba/smbpasswd
    map to guest = Bad User
```



#### **共享文件夹设置**

`vim /etc/config/samba `

```bash
config samba
        option charset 'UTF-8'
        option homes '0'
        option interface 'loopback lan'
        option name 'Lede'
        option description 'Samba on Lede'
        option workgroup 'Lede'

config sambashare
        option name 'Media'
        option path '/mnt/sda1'
        option read_only 'no'
        option guest_ok 'yes'
        option create_mask '0777'
        option dir_mask '0777'

config sambashare
        option path '/mnt/sda2'
        option read_only 'no'
        option create_mask '0700'
        option dir_mask '0700'
        option name 'Document'
        option guest_ok 'no'
```



#### **文件夹初始权限设置**

`/mnt/sda2`其实没必要更改所属用户和组，但是强迫症就是要给统一了。

```bash
chown -R nobody /mnt/sda1
chgrp -R nogroup /mnt/sda1
chmod -R 777 /mnt/sda1

chown -R nobody /mnt/sda2
chgrp -R nogroup /mnt/sda2
chmod -R 777 /mnt/sda2
```



#### **添加用户**

LEDE默认不带`useradd`命令，需要手动安装

```bash
opkg update
opkg install shadow-useradd
```



添加用户和设置密码要分两步走，首先要添加系统用户，然后再为该用户设置Samba密码。

```
useradd newuser
passwd newuser
smbpasswd -a newuser
```



至此，Samba设置完成，也达到了我的目的，有可以匿名随意访问的共享文件夹，也有实现了权限控制的私有文件夹。而且是全平台都可以访问，Windows、Linux和手机（需要有支持SMB协议的软件）。




# 参考链接
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
