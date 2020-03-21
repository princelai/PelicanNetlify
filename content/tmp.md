Title: 临时文件
Date: 2020-03-16 00:26
Category: 机器学习,金融与算法,玩电脑,杂记
Tags:
Slug: tmp-draft
Authors: Kevin Chen
Status: draft





```
#mkdir /etc/dnsmasq.d
#uci add_list dhcp.@dnsmasq[0].confdir=/etc/dnsmasq.d
uci add_list dhcp.@dnsmasq[0].cachesize=10000
uci commit dhcp

mkdir -p /etc/scripts
cd /etc/scripts

curl -L -o /etc/scripts/generate_dnsmasq_chinalist.sh https://github.com/cokebar/openwrt-scripts/raw/master/generate_dnsmasq_chinalist.sh
chmod +x /etc/scripts/generate_dnsmasq_chinalist.sh
sh /etc/scripts/generate_dnsmasq_chinalist.sh -d 223.5.5.5 -p 53 -s v2ray_dst_direct_v4 -o /etc/dnsmasq.d/dnsmasq_chinalist.conf

curl -L -o /etc/scripts/gfwlist2dnsmasq.sh https://github.com/cokebar/gfwlist2dnsmasq/raw/master/gfwlist2dnsmasq.sh
chmod +x /etc/scripts/gfwlist2dnsmasq.sh
sh /etc/scripts/gfwlist2dnsmasq.sh -d 8.8.4.4 -p 53 -s v2ray_dst_proxy_v4 -o /etc/dnsmasq.d/dnsmasq_gfwlist.conf

/etc/init.d/dnsmasq restart
```



ddns

```
wget https://github.com/honwen/luci-app-aliddns/releases/download/v20171205/luci-app-aliddns_0.2.0-1_all.ipk -O /tmp/aliddns.ipk
opkg install /tmp/aliddns.ipk
```



安装python3

```
opkg install python3 python3-requests python3-pip
```





get

```bash
wget https://www.v2ray.com/download/Core_v3.31/v2ray-linux-arm.zip
unzip v2ray-linux-arm.zip
cd v2ray-v3.31-linux-arm/
cp geoip.dat geosite.dat v2ctl v2ray v2ray_armv7 /usr/bin/v2ray/
```

tmp

```
iptables -t nat -nvL V2RAY --line-numbers

/usr/bin/v2ray/gfwlist2dnsmasq.sh -d 8.8.8.8  -p 53 -o /tmp/gfwlist.overall
```

```bash
#!/bin/ash
chnroute_url=http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest
curl $chnroute_url | grep ipv4 | grep CN | awk -F\| '{ printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /etc/chnroute.txt

# Create new chain
iptables -t nat -N V2RAY

# Ignore your V2Ray server's addresses
iptables -t nat -A V2RAY -d 95.169.10.107 -j RETURN
iptables -t nat -A V2RAY -d 95.169.3.48 -j RETURN
iptables -t nat -A V2RAY -d 107.172.103.201 -j RETURN

# Ignore LANs and any other addresses you'd like to bypass the proxy
iptables -t nat -A V2RAY -d 0.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 10.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 127.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 169.254.0.0/16 -j RETURN
iptables -t nat -A V2RAY -d 172.16.0.0/12 -j RETURN
iptables -t nat -A V2RAY -d 192.168.0.0/16 -j RETURN
iptables -t nat -A V2RAY -d 224.0.0.0/4 -j RETURN
iptables -t nat -A V2RAY -d 240.0.0.0/4 -j RETURN

# Ignore chinaroute
ipset create chnroute hash:net
for i in `cat /tmp/chnroute.txt`;
do
  ipset add chnroute $i
done

iptables -t nat -A V2RAY -m set --match-set chnroute dst -j RETURN

# Anything else should be redirected to Dokodemo-door's local port
iptables -t nat -A V2RAY -p all -j REDIRECT --to-ports 1060
iptables -t nat -A PREROUTING -p all -j V2RAY
exit 0
```

get h2y

```bash
wget https://github.com/ToutyRater/v2ray-SiteDAT/releases/download/v0.0.1/h2y.dat
chmod a+x h2y.dat
```

init script

```bash
# Put your custom commands here that should be executed once
# the system init finished. By default this file does nothing.
ulimit -n 8192
alias upgrade="opkg list-upgradable | cut -f 1 -d ' ' | xargs opkg upgrade"
mkdir /var/log/v2ray/
nohup /usr/bin/env v2ray.ray.buffer.size=1024 /usr/bin/v2ray/v2ray_armv7 -config /etc/v2ray/LEDE-H2-client.json &
#nohup /usr/bin/env v2ray.ray.buffer.size=1024 /usr/bin/v2ray/v2ray_armv7 -config /etc/v2ray/LEDE-KCP-client.json &
/usr/bin/v2ray/update_iptables.sh
exit 0
```

```
#############################################

mkdir /etc/dnsmasq.d
uci add_list dhcp.@dnsmasq[0].confdir=/etc/dnsmasq.d
uci add_list dhcp.@dnsmasq[0].cachesize=10000
uci commit dhcp

mkdir -p /etc/scripts
cd /etc/scripts

ipset -N gfwlist iphash
ipset -N chinalist iphash
ipset -N telegram iphash
ipset -N chnroute hash:net


chnroute_url=http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest
curl $chnroute_url | grep ipv4 | grep CN | awk -F\| '{ printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /etc/chnroute.txt

curl -L -o /etc/scripts/generate_dnsmasq_chinalist.sh https://github.com/cokebar/openwrt-scripts/raw/master/generate_dnsmasq_chinalist.sh
chmod +x /etc/scripts/generate_dnsmasq_chinalist.sh
sh /etc/scripts/generate_dnsmasq_chinalist.sh -d 223.5.5.5 -p 53 -s chinalist -o /etc/dnsmasq.d/dnsmasq_chinalist.conf

curl -L -o /etc/scripts/gfwlist2dnsmasq.sh https://github.com/cokebar/gfwlist2dnsmasq/raw/master/gfwlist2dnsmasq.sh
chmod +x /etc/scripts/gfwlist2dnsmasq.sh
sh /etc/scripts/gfwlist2dnsmasq.sh -d 8.8.4.4 -p 53 -s gfwlist -o /etc/dnsmasq.d/dnsmasq_gfwlist.conf


for i in `cat /etc/chnroute.txt`;
do
  ipset add chnroute $i
done



iptables -t nat -N V2RAY

iptables -t nat -A V2RAY -d 95.169.10.107 -j RETURN
iptables -t nat -A V2RAY -d 95.169.3.48 -j RETURN
iptables -t nat -A V2RAY -d 67.230.177.79 -j RETURN

iptables -t nat -A V2RAY -d 0.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 10.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 127.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 169.254.0.0/16 -j RETURN
iptables -t nat -A V2RAY -d 172.16.0.0/12 -j RETURN
iptables -t nat -A V2RAY -d 192.168.0.0/16 -j RETURN
iptables -t nat -A V2RAY -d 224.0.0.0/4 -j RETURN
iptables -t nat -A V2RAY -d 240.0.0.0/4 -j RETURN

iptables -t nat -I PREROUTING -p tcp  -m set --match-set gfwlist dst -j REDIRECT --to-ports 12345
iptables -t nat -I PREROUTING -p tcp  -m set --match-set telegram dst -j REDIRECT --to-ports 12345
iptables -t nat -I PREROUTING -p tcp  -m set --match-set chinalist dst -j RETURN
iptables -t nat -I PREROUTING -p tcp  -m set --match-set chnroute dst -j RETURN

iptables -t nat -A V2RAY -p tcp -j RETURN -m mark --mark 0xff
iptables -t nat -A OUTPUT -p tcp -j V2RAY

iptables -t mangle -N V2RAY_MARK
iptables -t mangle -A V2RAY_MARK -p udp --dport 53 -j MARK --set-mark 1
iptables -t mangle -A OUTPUT -j V2RAY_MARK
```





# 参考

[init.d](https://github.com/v2ray/v2ray-core/issues/101)

[利用 V2Ray + GFWList 实现路由器自动翻墙](https://cryptopunk.me/posts/27406/)

[网关服务器上设置 V2Ray+dnsmasq 透明代理](https://dakai.github.io/2017/11/27/v2ray.html)

[extroot](https://openwrt.org/docs/guide-user/additional-software/extroot_configuration)