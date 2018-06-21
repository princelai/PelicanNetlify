Title: LEDE/OpenWRT路由器打造家庭媒体影音中心（一）
Date: 2018-06-15 13:07
Category: IT笔记
Tags: openwrt, lede,wrt1900acs
Slug:lede-media-center1
Authors: Kevin Chen
Status: draft





# 前言

### 软/硬件

软件：本文系统都是基于LEDE 17.01.4

硬件：Linksys WRT1900ACS V2

其他：一台电脑，最好是Linux带SSH，Windows的话可以下个putty安装上

前提：我不会从头写起，而是从路由器已刷好LEDE 17.01.4，WAN口已联网，且已经可以SSH登录之后开始，其他外设，如硬盘、硬盘盒、用于Extroot的U盘都已准备好。



### 实现目的

基于Linksys WRT1900ACS强悍的性能和扩展功能丰富的LEDE，打造一个有权限控制的NAS，支持DLNA，可以离线下载和远程访问的DDNS系统的多媒体中心。



# Extroot

extroot的作用就是扩充存储空间，这样就可以安装更多的软件。详细介绍可以查看很早之前我写过的一篇文章——[用extroot为openwrt扩充存储空间](https://solarck.com/openwrt-extroot.html)，这里就不赘述了。由于那篇文章比较老，LEDE也早已经升级了好几个含本，所以实际的操作还是以下面的内容为主。



### 安装工具

这里我准备把U盘格式化为f2fs格式，关于各种存储格式和下面需要安装的工具的作用，我会放在下一篇文章一起讲，这一步照着做就可以了。

```
opkg update
opkg install block-mount kmod-fs-ext4 kmod-usb-storage e2fsprogs kmod-fs-f2fs f2fs-tools
```



### 格式化U盘

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
```

`vim /etc/config/fstab`



### 验证

重启系统后执行命令

`df -h`



如果`/overlay`分区已经变为U盘容量大小，那就是成功了。





# 更换源

### 添加对https的支持

如果你在替换源后执行更新，那么会收到一条错误消息：

> SSL support not available, please install one of the libustream-ssl-* libraries as well as the ca-bundle and ca-certificates packages.

很明显，系统还不支持SSL，因为官方的源都是http的，而我们添加的源都是https的。不过也很简单，按照错误信息的提示安装相应的包就可以了。**这一步一定要在替换源之前执行**

```bash
opkg update
opkg install ca-certificates libustream-openssl luci-ssl-openssl
```



### 更换源

国内访问LEDE官方源比较不稳定，速度也很慢，幸好[中科大](https://mirrors.ustc.edu.cn/lede/)和[清华](https://mirrors.tuna.tsinghua.edu.cn/lede/)都提供了LEDE的软件镜像源，为了后边操作能够顺利进行，首先需要更换源。

LEDE OPKG的软件源配置文件有两个：

`/etc/opkg/distfeeds.conf`：发行版本自带的官方源，需要把里面的内容全部注释掉或者清空。

`/etc/opkg/customfeeds.conf`：自定义源，把我们需要的内容粘贴到这里，内容如下：

```ini
src/gz reboot_core https://mirrors.ustc.edu.cn/lede/releases/17.01.4/targets/mvebu/generic/packages
src/gz reboot_base https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/base
src/gz reboot_luci https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/luci
src/gz reboot_packages https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/packages
src/gz reboot_routing https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/routing
src/gz reboot_telephony https://mirrors.ustc.edu.cn/lede/releases/17.01.4/packages/arm_cortex-a9_vfpv3/telephony

#只启用上面中科大的源，下面的作为备份
#src/gz reboot_core http://downloads.lede-project.org/releases/17.01.4/targets/mvebu/generic/packages
#src/gz reboot_base http://downloads.lede-project.org/releases/17.01.4/packages/arm_cortex-a9_vfpv3/base
#src/gz reboot_luci http://downloads.lede-project.org/releases/17.01.4/packages/arm_cortex-a9_vfpv3/luci
#src/gz reboot_packages http://downloads.lede-project.org/releases/17.01.4/packages/arm_cortex-a9_vfpv3/packages
#src/gz reboot_routing http://downloads.lede-project.org/releases/17.01.4/packages/arm_cortex-a9_vfpv3/routing
#src/gz reboot_telephony http://downloads.lede-project.org/releases/17.01.4/proot@ChenWrt:~# cat /etc/opkg/distfeeds.conf
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





# 优化LuCi

### SSL支持

#### **安装openssl**

```
opkg update
opkg install libopenssl
opkg install openssl-util
opkg install luci-app-uhttpd
```



#### **创建配置文件**

`vim /etc/ssl/myconfig.cnf`

```
[req]
distinguished_name  = req_distinguished_name
x509_extensions     = v3_req
prompt              = no
[req_distinguished_name]
C           = US
ST          = CA
L           = WRT1900ACS
O           = Home
OU          = Router
CN          = 192.168.1.1
[v3_req] 
keyUsage           = keyEncipherment, dataEncipherment
extendedKeyUsage   = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = 192.168.1.1
IP.1 = 192.168.1.1
```

这里需要把**CN**、**DNS.1**、**IP.1**填写正确，其余的保持或任意填。



#### **生成密钥**

```
cd /etc/ssl
openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout mycert.key -out mycert.crt -config myconfig.cnf
```

执行上面命令后，会在当前文件夹生成私钥和公钥，`mycert.key` 和 `mycert.crt`



#### **uHTTPd添加证书**

`HTTPS Certificate (DER Encoded) `:mycert.crt 

`HTTPS Private Key (DER Encoded) `:mycert.key 

#### **备份**



#### **管理浏览器证书**





### 汉化

```
opkg update
opkg install luci-i18n-base-zh-cn
```






# 参考链接
[How to get rid of LuCI https certificate warnings](https://openwrt.org/docs/guide-user/luci/getting-rid-of-luci-https-certificate-warnings)

[Extroot configuration](https://openwrt.org/docs/guide-user/additional-software/extroot_configuration)

