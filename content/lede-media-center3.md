Title: LEDE/OpenWRT 路由器打造家庭媒体影音中心（三）
Date: 2018-06-15 13:07
Category: 玩电脑
Tags: openwrt, lede,wrt1900acs
Slug:lede-media-center3
Authors: Kevin Chen
Status: draft

# DDNS

几个比较著名的 DDNS 服务商

> <https://www.dnsdynamic.org> > <http://www.pubyun.com/> > <https://www.changeip.com/> > <https://www.noip.com/>

安装工具和脚本

```
opkg update
opkg install wget curl bind-host knot-host drill ddns-scripts luci-app-ddns luci-i18n-ddns-zh-cn ddns-scripts_cloudflare.com-v4
```

uhttpd 设置

修改 http 监听端口

即使是公网 IP，国内 ISP 基本也都封了 80 端口，如果能破解光纤猫，那确实有办法打开 80 端口，但是惹不起躲得起，把 http 监听端口改一下就可以绕过这个限制。

uhttpd 在保存应用后，不会自动重启，需要手动执行

```
/etc/init.d/uhttpd restart
```

防火墙设置

流量规则

firewall->Traffic Rules

开启 666 端口

端口转发

firewall->Port Forwards

把所有 666 端口的请求转发到

# DLNA

```
opkg install minidlna luci-app-minidlna luci-i18n-minidlna-zh-cn
```

# Adblock

```
opkg update
opkg install adblock luci-app-adblock luci-i18n-adblock-zh-cn
```

# Python3

```
opkg update
opkg install python3 python3-pip
```

> terminfo. python3-base. libffi. libbz2\. python3-light. python3-pydoc. liblzma. python3-email. python3-decimal. python3-xml. libxml2\. libncurses. python3-ncurses. python3-distutils. python3-codecs. python3-multiprocessing. python3-unittest. python3-ctypes. libgdbm. python3-gdbm. libsqlite3\. python3-sqlite3\. python3-logging. python3-openssl. libdb47\. python3-dbm. python3-asyncio. python3-lzma. python3.

大约会占 30M

# 参考链接

[DDNS Client](https://openwrt.org/docs/guide-user/services/ddns/client)

[DLNA Media Server](https://openwrt.org/docs/guide-user/services/media_server/dlna)
