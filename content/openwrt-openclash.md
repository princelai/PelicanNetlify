Title:家庭出国网络升级（二）：配置openclash作为透明代理
Date: 2020-10-15 23:13
Category: 玩电脑
Tags: openwrt, openclash
Slug: using-openclash
Authors: Kevin Chen
Status: draft



```
opkg install libustream-openssl ca-bundle ca-certificates
```



```
opkg install coreutils coreutils-base64 coreutils-nohup bash iptables curl jsonfilter ipset ip-full iptables-mod-tproxy luci-compat iptables-mod-nat-extra libpthread kmod-tun libcap iptables-mod-extra
```

```
opkg list-upgradable | cut -f 1 -d ' ' | xargs opkg upgrade
```



```
opkg download dnsmasq-full
opkg install dnsmasq-full
opkg remove dnsmasq
opkg install dnsmasq-full_2.80-16.1_mipsel_24kc.ipk
rm dnsmasq-full_2.80-16.1_mipsel_24kc.ipk
```



```
opkg install vim-full wget luci-i18n-base-zh-cn
```



 ```
wget https://github.com/vernesong/OpenClash/releases/download/v0.40.7-beta/luci-app-openclash_0.40.7-beta_all.ipk

opkg install luci-app-openclash_0.40.7-beta_all.ipk 
 ```




[openclash releases](https://github.com/vernesong/OpenClash/releases)

