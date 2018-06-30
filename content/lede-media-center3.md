Title: LEDE/OpenWRT路由器打造家庭媒体影音中心（三）
Date: 2018-06-15 13:07
Category: IT笔记
Tags: openwrt, lede,wrt1900acs
Slug:lede-media-center3
Authors: Kevin Chen
Status: draft



# aria2下载

```
opkg update
opkg install aria2 luci-app-aria2 luci-i18n-aria2-zh-cn
```



# DDNS

几个比较著名的DDNS服务商

> https://www.dnsdynamic.org
> http://www.pubyun.com/
> https://www.changeip.com/
> https://www.noip.com/



安装工具和脚本

```
opkg update
opkg install wget curl bind-host knot-host drill ddns-scripts luci-app-ddns luci-i18n-ddns-zh-cn ddns-scripts_cloudflare.com-v4 ddns-scripts_no-ip_com
```

uhttpd设置

修改http监听端口

即使是公网IP，国内ISP基本也都封了80端口，如果能破解光纤猫，那确实有办法打开80端口，但是惹不起躲得起，把http监听端口改一下就可以绕过这个限制。

uhttpd在保存应用后，不会自动重启，需要手动执行

```
/etc/init.d/uhttpd restart   
```



防火墙设置

流量规则

firewall->Traffic Rules

开启666端口



端口转发

firewall->Port Forwards

把所有666端口的请求转发到



# DLNA

```
opkg install minidlna luci-app-minidlna luci-i18n-minidlna-zh-cn
```



# Adblock

```
opkg update
opkg install adblock luci-app-adblock luci-i18n-adblock-zh-cn
```



# Other

```
opkg install miniupnpd luci-app-upnp luci-i18n-upnp-zh-cn

opkg install qos-scripts luci-app-qos luci-i18n-qos-zh-cn
```



# Python3

```
opkg update
opkg install python3 python3-pip
```

> terminfo.   python3-base.   libffi.   libbz2.   python3-light.   python3-pydoc.   liblzma.   python3-email.   python3-decimal.   python3-xml.   libxml2.   libncurses.   python3-ncurses.   python3-distutils.   python3-codecs.   python3-multiprocessing.   python3-unittest.   python3-ctypes.   libgdbm.   python3-gdbm.   libsqlite3.   python3-sqlite3.   python3-logging.   python3-openssl.   libdb47.   python3-dbm.   python3-asyncio.   python3-lzma.   python3.   

大约会占30M



# 参考链接

[DDNS Client](https://openwrt.org/docs/guide-user/services/ddns/client)

[DLNA Media Server](https://openwrt.org/docs/guide-user/services/media_server/dlna)

