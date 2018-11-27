Title: LEDE/OpenWRT 路由器打造家庭媒体影音中心（一）
Date: 2018-07-10 13:07
Category: 玩电脑
Tags: openwrt, lede,wrt1900acs
Slug:lede-media-center1
Authors: Kevin Chen

# 前言

### 软/硬件

软件：本文系统都是基于 LEDE 17.01.4

硬件：Linksys WRT1900ACS V2

其他：一台电脑，最好是 Linux 带 SSH，Windows 的话可以下个 putty 安装上

前提：我不会从头写起，而是从路由器已刷好 LEDE 17.01.4，WAN 口已联网，且已经可以 SSH 登录之后开始，其他外设，如硬盘、硬盘盒、用于 Extroot 的 U 盘都已准备好。

### 实现目的

基于 Linksys WRT1900ACS 强悍的性能和扩展功能丰富的 LEDE，打造一个有权限控制的 NAS，支持 DLNA，可以离线下载和远程访问的 DDNS 系统的多媒体中心。

# Extroot

extroot 的作用就是扩充存储空间，这样就可以安装更多的软件。详细介绍可以查看很早之前我写过的一篇文章——[用 extroot 为 openwrt 扩充存储空间](https://solarck.com/openwrt-extroot.html)，这里就不赘述了。由于那篇文章比较老，LEDE 也早已经升级了好几个含本，所以实际的操作还是以下面的内容为主。

### 安装工具

这里我准备把 U 盘格式化为 f2fs 格式，关于各种存储格式和下面需要安装的工具的作用，我会放在下一篇文章一起讲，这一步照着做就可以了。

```
opkg update
opkg install block-mount kmod-fs-ext4 kmod-usb-storage e2fsprogs kmod-fs-f2fs f2fs-tools
```

### 格式化 U 盘

```bash
mkfs.f2fs /dev/sda1
```

### 迁移系统

```bash
mount /dev/sda1 /mnt ; tar -C /overlay -cvf - . | tar -C /mnt -xf - ; umount /mnt
```

### 生成分区表

```
block detect > /etc/config/fstab
uci set fstab.@mount[0].target='/overlay'
uci set fstab.@mount[0].enabled='1'
uci set fstab.@mount[0].options='rw'
uci set fstab.@mount[0].fstype='f2fs'
uci commit
```

最后`fstab`应该如下

`cat /etc/config/fstab`

```
config global
        option anon_swap '0'
        option anon_mount '0'
        option auto_swap '1'
        option auto_mount '1'
        option delay_root '5'
        option check_fs '1'


config mount
        option enabled '1'
        option uuid 'd9aa4451-780a-4fe5-b08d-d7f0a7ae0ba4'
        option target '/overlay'
        option fstype 'f2fs'
        option options 'rw'
```

### 验证

重启系统后执行命令

`df -h`

```
Filesystem                Size      Used Available Use% Mounted on
/dev/root                 2.8M      2.8M         0 100% /rom
tmpfs                   250.8M    556.0K    250.2M   0% /tmp
/dev/sdb1                14.3G    496.6M     13.7G   3% /overlay
overlayfs:/overlay       14.3G    496.6M     13.7G   3% /
ubi1:syscfg              29.6M    268.0K     27.8M   1% /tmp/syscfg
tmpfs                   512.0K         0    512.0K   0% /dev
```

如果`/overlay`分区已经变为 U 盘容量大小，那就是成功了。

`block info`信息也已经显示正确

```
/dev/mtdblock7: TYPE="jffs2"
/dev/ubiblock0_0: UUID="9f419b56-31564c19-0a0c1b12-a2f9b77b" VERSION="4.0" MOUNT="/rom" TYPE="squashfs"
/dev/ubi0_1: UUID="1361ff26-cc87-40f1-8b99-00caf223093c" VERSION="w4r0" TYPE="ubifs"
/dev/ubi1_0: UUID="413d13a9-0f0a-4811-a0cb-3e3786ce26d7" VERSION="w4r0" TYPE="ubifs"
/dev/sda1: UUID="d9aa4451-780a-4fe5-b08d-d7f0a7ae0ba4" VERSION="1.8" MOUNT="/overlay" TYPE="f2fs"
```

# 更换源

### 添加对 https 的支持

如果你在替换源后执行更新，那么会收到一条错误消息：

> SSL support not available, please install one of the libustream-ssl-\* libraries as well as the ca-bundle and ca-certificates packages.

很明显，系统还不支持 SSL，因为官方的源都是 http 的，而我们添加的源都是 https 的。不过也很简单，按照错误信息的提示安装相应的包就可以了。**这一步一定要在替换源之前执行**

```bash
opkg update
opkg install ca-certificates luci-ssl-openssl
```

### 更换源

国内访问 LEDE 官方源比较不稳定，速度也很慢，幸好[中科大](https://mirrors.ustc.edu.cn/lede/)和[清华](https://mirrors.tuna.tsinghua.edu.cn/lede/)都提供了 LEDE 的软件镜像源，为了后边操作能够顺利进行，首先需要更换源。

LEDE OPKG 的软件源配置文件有两个：

`/etc/opkg/distfeeds.conf`：发行版本自带的官方源，需要把里面的内容全部注释掉或者清空。

`/etc/opkg/customfeeds.conf`：自定义源，把我们需要的内容粘贴到这里，内容如下：

```ini
src/gz reboot_core https://mirrors.ustc.edu.cn/lede/releases/17.01.4/targets/mvebu/generic/packages
src/gz reboot_base https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/base
src/gz reboot_luci https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/luci
src/gz reboot_packages https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/packages
src/gz reboot_routing https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/routing
src/gz reboot_telephony https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/telephony

#src/gz reboot_core https://mirrors.tuna.tsinghua.edu.cn/lede/releases/17.01.4/targets/mvebu/generic/packages
#src/gz reboot_base https://mirrors.tuna.tsinghua.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/base
#src/gz reboot_luci https://mirrors.tuna.tsinghua.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/luci
#src/gz reboot_packages https://mirrors.tuna.tsinghua.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/packages
#src/gz reboot_routing https://mirrors.tuna.tsinghua.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/routing
#src/gz reboot_telephony https://mirrors.tuna.tsinghua.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/telephony
```

### 更新系统

镜像源替换完成后，把所有已安装程序全部更新到最新

```bash
opkg update
opkg list-upgradable | cut -f 1 -d ' ' | xargs opkg upgrade
```

# 其他

### 汉化

```
opkg update
opkg install luci-i18n-base-zh-cn
```

# 参考链接

[How to get rid of LuCI https certificate warnings](https://openwrt.org/docs/guide-user/luci/getting-rid-of-luci-https-certificate-warnings)

[Extroot configuration](https://openwrt.org/docs/guide-user/additional-software/extroot_configuration)
