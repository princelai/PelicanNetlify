Title: 水星（Mercury）MW4530r 刷 Openwrt
Date: 2014-01-02 01:08
Category: 玩电脑
Tags: openwrt
Slug: install-openwrt-on-mw4530r
Authors: Kevin Chen

经过两天的不屑折腾，终于为我的 Mw4530r 安装上了 Openwrt。从最后安装成功往回看，其实整个过程非常简单，但是由于是第一次接触，走了不少弯路，本应该一个小时就完成的工作，却整整花了我两天时间。再次发篇文章庆祝下，也给其他朋友一些参考。

### 下载文件

水星这款路由器是 ar71xx 芯片的，因为较新，所以还没有官方的稳定版。在 Openwrt 的[snapshots/trunk][1]目录搜索下载我们需要的刷机文件，一般情况一个型号有两个文件，一个名字里带 factory，从其他固件系统刷 Openwrt 下载这个文件；一个名字带 sysupgrade，已经是 Openwrt 系统的用此文件升级。

### 刷机

组装好路由器，接通电源，电脑网卡口连接路由器任意 Lan 口，打开浏览器访问http://192.168.1.1 就可以看见水星的原厂界面。利用原厂固件的升级功能，提交下载好的 Openwrt 刷机文件即可直接刷机，非常的方便。稍等片刻等待路由器自动重启，此时刷机完成。

### 初始化

Openwrt 的固件是不带 UI 界面的，在安装用户界面之前，用户需要先进行简单的初始化工作。  
使用 telnet 登陆路由器

```bash
telnet 192.168.1.1
```

Linux 系统自带命令，Windows 用户需要在控制面板-->程序里面启用 telnet 功能。

修改登录密码

```bash
passwd
```

更改好密码后，dropbear（ssh）登录方式开启，telnet 登录方式关闭。

退出 telnet，用 ssh 方式登陆，Windows 用户可以下载 putty 登陆

```bash
exit
ssh root@192.168.1.1
```

到此我们已经成功初始化了 Openwrt。

### 网络配置

**强烈建议基础配置尤其是网络设置都使用 CLI 界面，切勿乱修改原始配置，我就在这里经历的惨痛的教训**  
我使用的是联通 ADSL，所以需要拨号（pppoe）才能上网。

配置网络连接，修改 wan 部分

```bash
root@openwrt:~# vi /etc/config/network
config interface 'wan'
	option ifname 'eth0.2'
	option proto 'pppoe'
	option username 'ISP提供的用户名'
	option password '密码'
```

或者用 uci 方式进行配置

```bash
uci set network.wan.proto=pppoe
uci set network.wan.username='ISP提供的用户名'
uci set network.wan.password='密码'
uci commit network
ifup wan
```

配置 wifi，根据你的路由器配置生成一个默认的配置文件

```bash
wifi detect > /etc/config/wireless
```

重启后，互联网和 wifi 都应该已经正常工作，wifi 的密码和名称我们之后可以在 UI 界面修改，接下来安装用户界面。

### 用户界面

安装 Luci

```bash
opkg update
opkg install luci luci-ssl luci-i18n-chinese
```

启动 Luci 服务

```bash
/etc/init.d/uhttpd start
/etc/init.d/uhttpd enable
```

打开浏览器输入http://192.168.1.1 ，就可以进入 WebUI 界面了，现在就可以向普通路由器一样进行管理了。

### 小提示

> 1.MW4530r 进入 failsafe 的方法是：路由器断电-->接通电源-->断续的按面板前的 WPS 键，直到 SYS 指示灯从慢闪变为快闪就是成功进入了 failsafe 模式了。  
> 2.初始配置尽量用 CLI 方式配置（或 uci），最好不要用 WebUI。 3.不要乱动乱删配置文件，尤其是端口路由表（switch0）。

贴一张 Openwrt 的路由架构图，这张图帮助我理解了端口和路由的关系。

![linksys](https://ws1.sinaimg.cn/large/65f2a787ly1fxuvfpqw1gj20e70a5q3g.jpg)

[1]: http://downloads.openwrt.org/snapshots/trunk/ar71xx/
