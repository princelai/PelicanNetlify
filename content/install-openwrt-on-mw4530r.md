Title: 水星（Mercury）MW4530r刷Openwrt
Date: 2014-01-02 01:08
Category: IT笔记
Tags: openwrt
Slug: install-openwrt-on-mw4530r
Authors: Kevin Chen

经过两天的不屑折腾，终于为我的Mw4530r安装上了Openwrt。从最后安装成功往回看，其实整个过程非常简单，但是由于是第一次接触，走了不少弯路，本应该一个小时就完成的工作，却整整花了我两天时间。再次发篇文章庆祝下，也给其他朋友一些参考。


### 下载文件
水星这款路由器是ar71xx芯片的，因为较新，所以还没有官方的稳定版。在Openwrt的[snapshots/trunk][1]目录搜索下载我们需要的刷机文件，一般情况一个型号有两个文件，一个名字里带factory，从其他固件系统刷Openwrt下载这个文件；一个名字带sysupgrade，已经是Openwrt系统的用此文件升级。

### 刷机
组装好路由器，接通电源，电脑网卡口连接路由器任意Lan口，打开浏览器访问http://192.168.1.1 就可以看见水星的原厂界面。利用原厂固件的升级功能，提交下载好的Openwrt刷机文件即可直接刷机，非常的方便。稍等片刻等待路由器自动重启，此时刷机完成。

<!--more-->

### 初始化
Openwrt的固件是不带UI界面的，在安装用户界面之前，用户需要先进行简单的初始化工作。    
使用telnet登陆路由器
```bash
telnet 192.168.1.1
```
Linux系统自带命令，Windows用户需要在控制面板-->程序里面启用telnet功能。

修改登录密码
```bash
passwd
```
更改好密码后，dropbear（ssh）登录方式开启，telnet登录方式关闭。

退出telnet，用ssh方式登陆，Windows用户可以下载putty登陆
```bash
exit
ssh root@192.168.1.1
```
到此我们已经成功初始化了Openwrt。

### 网络配置
**强烈建议基础配置尤其是网络设置都使用CLI界面，切勿乱修改原始配置，我就在这里经历的惨痛的教训**  
我使用的是联通ADSL，所以需要拨号（pppoe）才能上网。     


配置网络连接，修改wan部分
```bash
root@openwrt:~# vi /etc/config/network
config interface 'wan'
	option ifname 'eth0.2'
	option proto 'pppoe'
	option username 'ISP提供的用户名'
	option password '密码'

```
或者用uci方式进行配置
```bash
uci set network.wan.proto=pppoe
uci set network.wan.username='ISP提供的用户名'
uci set network.wan.password='密码'
uci commit network
ifup wan
```
配置wifi，根据你的路由器配置生成一个默认的配置文件
```bash
wifi detect > /etc/config/wireless
```
重启后，互联网和wifi都应该已经正常工作，wifi的密码和名称我们之后可以在UI界面修改，接下来安装用户界面。

### 用户界面
安装Luci    
```bash
opkg update
opkg install luci luci-ssl luci-i18n-chinese
```
启动Luci服务
```bash
/etc/init.d/uhttpd start
/etc/init.d/uhttpd enable
```
打开浏览器输入http://192.168.1.1 ，就可以进入WebUI界面了，现在就可以向普通路由器一样进行管理了。

### 小提示
>1.MW4530r进入failsafe的方法是：路由器断电-->接通电源-->断续的按面板前的WPS键，直到SYS指示灯从慢闪变为快闪就是成功进入了failsafe模式了。    
>2.初始配置尽量用CLI方式配置（或uci），最好不要用WebUI。
>3.不要乱动乱删配置文件，尤其是端口路由表（switch0）。

贴一张Openwrt的路由架构图，这张图帮助我理解了端口和路由的关系。      

<img src="http://www.macfreek.nl/memory/images/Linksys_internals.png" title="switch" width="450" />

[1]:http://downloads.openwrt.org/snapshots/trunk/ar71xx/
