Title: 从lean大神的LEDE系统刷回原版Openwrt
Date: 2019-10-02 22:45
Category: 玩电脑
Tags: openwrt, lede
Slug: leanlede-to-openwrt
Authors: Kevin Chen



自从知道恩山lean大神开源的LEDE系统，一直沉迷于它的方便，自己想要什么就编译什么，比如他自己开发的adbyby和ssr-plus插件，但是使用了一段时间以后，就发现某些软件的兼容性有问题，不定时重启且重启后无法联网，无奈只能选择刷回原版，但是刷回的过程非常艰辛，今天把握成功刷回的过程记录下来分享给大家。如下图，这是我路由器的型号和架构。

![pic1](https://wx1.sinaimg.cn/large/65f2a787ly1g7k7ebpbomj20oy08m74o.jpg)



我从openwrt的官网下载了几乎所有我能下载到的固件，不论是稳定版还是开发版。（中间混杂着一个newifi3的固件请无视）

![pic2](https://wx1.sinaimg.cn/large/65f2a787ly1g7k7ebpkp2j20h504nt9u.jpg)



任何一个固件使用luci自带的刷写页面都会提示“不支持所上传的映像文件格式，请选择适合当前平台的通用映像文件”。这就让我很郁闷，我也是刷过上百次原版固件的人了，怎么这次就不行了呢？

![pic3](https://wx1.sinaimg.cn/large/65f2a787ly1g7k7ebphakj20kn05daai.jpg)



我查阅了openwrt官网几乎所有的教程，比如[这个](https://openwrt.org/toh/linksys/linksys_wrt1900acs)和[这个](https://openwrt.org/toh/linksys/wrt_ac_series)，在里面学到从命令行使用`sysupgrade`刷回，但也是提示各种各样的错误，见下面的代码，我甚至已经买好USB-TTL线准备拆机救砖了。

```bash
# sysupgrade -F -n -v -T /tmp/FW_WRT1900ACS_1.0.3.187766_prod.img 
Image metadata not found
Image check 'fwtool_check_image' failed but --force given - will update anyway!
```





就在我等着快递送货的期间，偶然发现在[openwrt uninstall](https://openwrt.org/docs/guide-user/installation/generic.uninstall)页面隐藏这一个更底层了方法，使用mtd刷机，这种方法会直接把固件强行写入默认分区，从而跳过验证，最终成功恢复了原版系统，方法如下：





**上传固件**

我这里使用了Linksys的原版固件，而不是openwrt的固件，然后需要从原版再刷入openwrt。下面代码需要替换自己路由器的IP、端口和原版固件文件名。

```bash
scp -P 22 FW_WRT1900ACS_1.0.3.187766_prod.img root@192.168.250.1:/tmp/
```





**刷入固件**

```bash
# mtd  -r write /tmp/FW_WRT1900ACS_1.0.3.187766_prod.img kernel1
Unlocking kernel1 ...

Writing from /tmp/FW_WRT1900ACS_1.0.3.187766_prod.img to kernel1 ...     
Rebooting ...
Connection to 192.168.1.1 closed by remote host.
Connection to 192.168.1.1 closed.
```

注意，输入上面命令之前需要了解你自己路由器的*firmware*情况，可以在openwrt网站查看，然后再在自己的路由器上使用下面的命令查看是否能对应上某个分区，确认无误后，把你*firmware*的名字替换掉*kernel1*即可。

```
# cat /proc/mtd 
dev:    size   erasesize  name
mtd0: 00200000 00020000 "u-boot"
mtd1: 00040000 00020000 "u_env"
mtd2: 00040000 00020000 "s_env"
mtd3: 00100000 00020000 "devinfo"
mtd4: 02800000 00020000 "kernel1"
mtd5: 02200000 00020000 "rootfs1"
mtd6: 02800000 00020000 "kernel2"
mtd7: 02200000 00020000 "ubi"
mtd8: 02600000 00020000 "syscfg"
mtd9: 00680000 00020000 "unused_area"
```

