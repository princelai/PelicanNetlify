Title: LEDE路由器打造家庭媒体影音中心（三）
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

```
opkg install wget curl bind-host knot-host drill
ddns-scripts
luci-app-ddns
luci-i18n-ddns-zh-cn
https://www.dnsdynamic.org
http://www.pubyun.com/
https://www.changeip.com/
https://www.noip.com/
```



# DLNA

```
opkg install minidlna luci-app-minidlna luci-i18n-minidlna-zh-cn
```



# Other

```
opkg install transmission-daemon-openssl transmission-web luci-app-transmission luci-i18n-transmission-zh-cn

opkg install miniupnpd luci-app-upnp luci-i18n-upnp-zh-cn

opkg install qos-scripts luci-app-qos luci-i18n-qos-zh-cn

opkg remove --autoremove *
```






# 参考链接
