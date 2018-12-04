Title: 路由器自动翻墙
Date: 2018-12-04 14:15
Category: 玩电脑
Tags: lede,openwrt,shadowsocks
Slug: lede-shadowsocks
Authors: Kevin Chen
Status: draft



> 本文完全参考了[飞羽博客](https://cokebar.info)的两篇文章（[文章1](https://cokebar.info/archives/664)，[文章2](https://cokebar.info/archives/962)），这篇文章只做了微小的修改，用于备份自己的操作流程。想要实现LEDE+Shadowsocks的朋友可以跳转到那两篇文章研究。



# 安装

### 安装密钥

```bash
wget http://openwrt-dist.sourceforge.net/openwrt-dist.pub
opkg-key add openwrt-dist.pub
```



### 新增源

查看路由器架构，需要添加相应的版本

```bash
cat /etc/os-release |grep "LEDE_ARCH" |awk '{split($0,a,"=");print substr(a[2],2,length(a[2])-2)}'
```



添加自定义源

`vim /etc/opkg/customfeeds.conf`

```
src/gz openwrt_dist http://openwrt-dist.sourceforge.net/packages/base/arm_cortex-a9_vfpv3
src/gz openwrt_dist_luci http://openwrt-dist.sourceforge.net/packages/luci
```



### 安装pkg

```bash
opkg update
opkg install ChinaDNS luci-app-chinadns shadowsocks-libev luci-app-shadowsocks ip-full ipset iptables-mod-tproxy libpthread
```



# 配置

## Shadowsocks配置

### 添加服务器

添加四个服务器（图）

### 访问控制

（图）

`被忽略IP列表`：因为之后要使用ChinaDNS分流，所以这里要选择这一项

`额外被忽略的IP`：有几个服务器，就把服务器加入到忽略列表

`强制走代理IP`：境外DNS



（图）

`代理类型`：直接连接就是，正常代理就是

`代理自身`：路由器自身代理模式

这里我让所有链接全部让路由器根据路由表选择线路，如果代理类型选择直接连接，那么还需要在下面内网主机里添加需要走代理的设备IP，并把代理类型设为正常代理或全局代理。



### 开启代理

（图）

因为路由器翻墙只需要用到透明代理，而DNS转发需要用到端口转发，所以把这两项按图设置好就可以了。



## DNS配置

在路由表内的网址

> 路由器DNS--->ChinaDNS（#5353）--->DNS转发（#5311）--->境外DNS（8.8.8.8#53）

如果不在路由表内

> 路由器DNS--->ChinaDNS（#5353）--->国内DNS（114.114.114.114#53）







# 额外的优化

### TCP Fast Open

向`/etc/sysctl.conf`文件添加一行配置

`vim /etc/sysctl.conf`

```
net.ipv4.tcp_fastopen = 3
```

然后执行命令即可生效

```
sysctl -p
```



### 定时更新脚本

```bash
wget -O- 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' | awk -F\| '/CN\|ipv4/ { printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /etc/chinadns_chnroute.txt
```



# 参考

[openwrt-dist](http://openwrt-dist.sourceforge.net/)

[OpenWrt 基于 HAProxy 的透明代理负载均衡和高可用部署](https://blog.csdn.net/lvshaorong/article/details/53034513)

[HAproxy 指南之 haproxy 配置详解](http://blog.51cto.com/blief/1750952)
