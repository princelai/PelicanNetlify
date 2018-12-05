Title: 路由器自动翻墙
Date: 2018-12-04 14:15
Category: 玩电脑
Tags: lede,openwrt,shadowsocks
Slug: lede-shadowsocks
Authors: Kevin Chen
Status: draft



> 本文完全参考了[飞羽博客](https://cokebar.info)的[文章](https://cokebar.info/archives/664)，我这篇文章只做了微小的修改，用于备份自己的操作流程。想要查看更详细的LEDE+Shadowsocks配置细节的朋友可以跳转到那篇文章研究。



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



添加自定义源，下面`arm_cortex-a9_vfpv3`就是上面查到的版本

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



```
opkg install coreutils-base64 ca-certificates ca-bundle curl
```





# 配置

## Shadowsocks配置

### 添加服务器

这里添加一个服务器，如果开启TCP快速打开，后面会说道如何让路由器支持，其余的要与服务器端配置相同。
![add one](https://ws1.sinaimg.cn/large/65f2a787ly1fxv41slbu5j20dp0gujsc.jpg)



添加完所有服务器后的列表
![服务器列表](https://ws1.sinaimg.cn/large/65f2a787ly1fxv41slllxj20qs0bedh5.jpg)






### 访问控制

![访问控制1](https://ws1.sinaimg.cn/large/65f2a787ly1fxv4ep5qw4j20dg0dwgmf.jpg)

`被忽略IP列表`：因为之后要使用ChinaDNS分流，所以这里要选择这一项

`额外被忽略的IP`：有几个服务器，就把服务器加入到忽略列表

`强制走代理IP`：境外DNS

在第一次使用前建议更新chnroute路由表，以及之后每几个月更新一次，更新方法在文章最后的定时更新脚本中。





![访问控制2](https://ws1.sinaimg.cn/large/65f2a787ly1fxv4b9z2x0j20dw07a0t0.jpg)

`代理类型`：直接连接就是，正常代理就是

`代理自身`：路由器自身代理模式

这里我让所有链接全部让路由器根据路由表选择线路，如果代理类型选择直接连接，那么还需要在下面内网主机里添加需要走代理的设备IP，并把代理类型设为正常代理或全局代理。



### 开启代理

![透明代理](https://ws1.sinaimg.cn/large/65f2a787ly1fxv6rhr0oaj20db0910sy.jpg)



![端口转发](https://ws1.sinaimg.cn/large/65f2a787ly1fxv6rhr39gj20cr08xmxc.jpg)



因为路由器翻墙只需要用到透明代理，而DNS转发需要用到端口转发，所以把这两项按图设置好就可以了。

这部分属于Shadowsocks配置，但是建议放到最后再执行，因为配置好一旦保存就要开始了，但是现在DNS还没配置好。



## DNS配置

### 示意图

不在chnroute路由表内的网址

> 路由器DNS--->ChinaDNS（#5353）--->SS端口转发（#5300）--->境外DNS（8.8.8.8#53）

在chnroute路由表内

> 路由器DNS--->ChinaDNS（#5353）--->国内DNS（114.114.114.114#53）



### ChinaDNS

![ChinaDNS](https://ws1.sinaimg.cn/large/65f2a787ly1fxv6rhra4zj20e40bp3z3.jpg)

### 系统DNS设置
在Luci中切换至`网络--->DHCP/DNS--->基本设置`，DNS 转发填入`127.0.0.1#5353`

切换至`网络--->DHCP/DNS--->HOSTS和解析文件`，勾选“忽略解析文件”

切换至`网络--->接口--->WAN--->高级设置`，取消勾选“使用对端通告的 DNS 服务器”，并在“使用自定义的 DNS 服务器”中填入`127.0.0.1`



### 优化DNS配置

```
mkdir /etc/dnsmasq.d
uci add_list dhcp.@dnsmasq[0].confdir=/etc/dnsmasq.d
uci add_list dhcp.@dnsmasq[0].cachesize=50000
uci commit dhcp
```

新建一个文件夹，让dnsmasq关联到这个配置文件路径，增大缓存



### 强制DNS走代理和强制DNS直连

#### China-List

```
curl -L -o generate_dnsmasq_chinalist.sh https://github.com/cokebar/openwrt-scripts/raw/master/generate_dnsmasq_chinalist.sh
chmod +x generate_dnsmasq_chinalist.sh
sh generate_dnsmasq_chinalist.sh -d 114.114.114.114 -p 53 -o /etc/dnsmasq.d/accelerated-domains.china.conf
```

这段脚本会生成`/etc/dnsmasq.d/accelerated-domains.china.conf`配置文件



#### GFWList

```
curl -L -o gfwlist2dnsmasq.sh https://github.com/cokebar/gfwlist2dnsmasq/raw/master/gfwlist2dnsmasq.sh
chmod +x gfwlist2dnsmasq.sh
sh gfwlist2dnsmasq.sh -d 127.0.0.1 -p 5300 -o /etc/dnsmasq.d/dnsmasq_gfwlist.conf
```

这段脚本会生成`/etc/dnsmasq.d/dnsmasq_gfwlist.conf`配置文件



#### 重启dnsmasq服务

```
/etc/init.d/dnsmasq restart
```

重启后dnsmasq会自动加载上面两个配置文件




# 额外的优化

## TCP Fast Open

向`/etc/sysctl.conf`文件添加一行配置

`vim /etc/sysctl.conf`

```
net.ipv4.tcp_fastopen = 3
```

然后执行命令即可生效

```
sysctl -p
```



## 定时更新脚本

### chnroute

创建一个脚本文件夹和shell脚本

```
cd /etc
mkdir script
touch gen_chnroute.sh
```



脚本内容如下

`vim /etc/gen_chnroute.sh`

```bash
#/bin/sh

wget -O- 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' | awk -F\| '/CN\|ipv4/ { printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /etc/chinadns_chnroute.txt
```

### China-List和GFWList

把之前步骤已经下载好的脚本拷贝到脚本文件夹

```bash
cd ~
mv *.sh /etc/script/
```



### 计划任务

可以在Luci界面`系统--->计划任务`或者直接在shell中输入`crontab -e`，把下面的内容复制进去，这个任务在每月8日凌晨4点多把全部需要更新的脚本执行一遍并重启dnsmasq。

```
14  4  8  *  *  sh /etc/script/gen_chnroute.sh 
15  4  8  *  *  sh /etc/script/generate_dnsmasq_chinalist.sh -d 114.114.114.114 -p 53 -o /etc/dnsmasq.d/accelerated-domains.china.conf
16  4  8  *  *  sh /etc/script/gfwlist2dnsmasq.sh -d 127.0.0.1 -p 5300 -o /etc/dnsmasq.d/dnsmasq_gfwlist.conf
17  4  8  *  *  /etc/init.d/dnsmasq restart
```






