Title:
Date: 2018-07-10 14:15
Category: IT笔记, 金融笔记
Tags:
Slug: lede-haproxy-shadowsocks
Authors: Kevin Chen
Status: draft



安装密钥

```bash
wget http://openwrt-dist.sourceforge.net/openwrt-dist.pub
opkg-key add openwrt-dist.pub
```



新增源

```bash
cat /etc/os-release |grep "LEDE_ARCH" |awk '{split($0,a,"=");print substr(a[2],2,length(a[2])-2)}'

```

```
src/gz openwrt_dist http://openwrt-dist.sourceforge.net/packages/base/arm_cortex-a9_vfpv3
src/gz openwrt_dist_luci http://openwrt-dist.sourceforge.net/packages/luci
```

```bash
opkg update
opkg install ChinaDNS luci-app-chinadns shadowsocks-libev luci-app-shadowsocks simple-obfs haproxy
```





# 参考

[openwrt-dist](http://openwrt-dist.sourceforge.net/)