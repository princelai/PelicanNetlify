Title:
Date: 2018-12-05 10:56
Category: 机器学习,金融与算法,玩电脑,杂记
Tags:
Slug: lede-ddns
Authors: Kevin Chen
Status: draft



```
cd /etc
mkdir script
touch checkIP.sh 
```

```
#/bin/sh

/usr/bin/host -t A chenwrt.com
```



`chmod a+x checkIP.sh `

# 参考

[openwrt-dist](http://openwrt-dist.sourceforge.net/)

[OpenWrt 基于 HAProxy 的透明代理负载均衡和高可用部署](https://blog.csdn.net/lvshaorong/article/details/53034513)

[HAproxy 指南之 haproxy 配置详解](http://blog.51cto.com/blief/1750952)