Title:家庭出国网络升级（二）：配置openclash作为透明代理
Date: 2020-10-15 23:13
Category: 玩电脑
Tags: openwrt, openclash
Slug: using-openclash
Authors: Kevin Chen
Status: draft



```
opkg install coreutils coreutils-base64 coreutils-nohup bash iptables dnsmasq-full curl jsonfilter ca-certificates ipset ip-full iptables-mod-tproxy luci-compat iptables-mod-nat-extra libpthread kmod-tun libcap iptables-mod-extra
```

 ```
wget https://github.com/vernesong/OpenClash/releases/download/v0.40.7-beta/luci-app-openclash_0.40.7-beta_all.ipk

opkg install luci-app-openclash_0.40.7-beta_all.ipk 
 ```



```
* luci
* luci-base
* iptables
* dnsmasq-full
* coreutils
* coreutils-nohup
* bash
* curl
* jsonfilter
* ca-certificates
* ipset
* ip-full
* iptables-mod-tproxy
* kmod-tun(TUN模式)
* luci-compat(Luci-19.07)
```

[openclash releases](https://github.com/vernesong/OpenClash/releases)

