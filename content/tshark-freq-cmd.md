Title: tshark常用命令详解
Date: 2018-11-16 18:35
Category: 玩电脑
Tags: wireshark, tshark
Slug: tshark-freq-cmd
Authors: Kevin Chen




### Wireshark简介

> Wireshark 是一款免费开源的包分析器。可用于网络排错、网络分析、软件和通讯协议开发以及教学等。tshark是wireshark的cli版本



### 安装

Archlinux

```
yaourt -Syu wireshark-cli
```



Debian

```
apt-get update
apt-get install tshark
```



查看权限

```
$ getcap /usr/bin/dumpcap
/usr/bin/dumpcap = cap_net_admin,cap_net_raw+eip
```

dumpcap的位置也可能在`/usr/sbin/dumpcap`，如果输出结果不像上面那样，则还需要设置权限

```
# setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' /usr/sbin/dumpcap
```

把用户添加至wireshark用户组

```
# gpasswd -a username wireshark
```

切换至新用户组

```
$ newgrp wireshark
```





### 查看http请求1

```
tshark -i em1 -n -Y http.request -T fields  -e "ip.src" -e "http.request.method" -e "http.request.uri"
```
#### 参数

`-i`：网络设备名，默认为第一个非环路设备，可用`ip link`或`ifconfig`查看

`-n`：禁止域名解析，显示原始IP地址

`-Y`：显示过滤，使用Wireshark display filter语法，通常用于后接单一过滤器；查看过滤语法，[DisplayFilters](https://wiki.wireshark.org/DisplayFilters)，[CheatSheet](http://packetlife.net/blog/2008/oct/18/cheat-sheets-tcpdump-and-wireshark/)

`-T`：文本输出格式

`-e`：输出Fields的某一字段

#### 输出结果

```
117.136.0.189   POST    /api/anonymous/notice/new
119.123.197.16  POST    /web/wechat/login
113.120.250.84  POST    /api/projectlib/detail
113.120.250.84  POST    /api/projectlib/getProjectFile
113.120.250.84  POST    /api/projectlib/getBasicProject
113.120.250.84  POST    /api/projectlib/getGuessProjectList
113.120.250.84  POST    /api/projectcomment/commentlist
119.123.197.16  POST    /web/wechat/login
```







### 查看http请求2


```
tshark -i em1 -f 'tcp dst port 80 and src host 111.207.128.226' -R 'http.host and http.request.uri' -T fields  -e http.request.uri -e http.user_agent
```
#### 参数

`-f`：包过滤，使用libpcap filter语法；查看过滤语法，[CaptureFilters](https://wiki.wireshark.org/CaptureFilters)

`-R`：显示过滤，使用Wireshark display filter语法，通常用于后接多个过滤器；查看过滤语法，[DisplayFilters](https://wiki.wireshark.org/DisplayFilters)，[CheatSheet](http://packetlife.net/blog/2008/oct/18/cheat-sheets-tcpdump-and-wireshark/)

#### 输出结果

```
/api/projectlib/getProvincelist290      okhttp/3.3.1
/api/projectlib/findBaseDataInfo        okhttp/3.3.1
/api/corpinvestor/getInvestorCity       okhttp/3.3.1
/api/advertisement/splashScreen okhttp/3.3.1
/api/commons/check      okhttp/3.3.1
/api/userinfo/getPending        okhttp/3.3.1
/api/index/getIndexCard okhttp/3.3.1
/api/myinvest/checkPrefer       okhttp/3.3.1
/api/index/450/indexInfo        okhttp/3.3.1
/api/chat/list  okhttp/3.3.1
/api/employee/getMyInfomsgNew   okhttp/3.3.1
/api/index/getTopNewsList       okhttp/3.3.1
/api/anonymous/list     okhttp/3.3.1
/api/anonymous/notice/new       okhttp/3.3.1
```



### 查看DNS包

```
tshark -n  -f "dst port 53" -T fields -e dns.qry.name -e dns.resp.addr
```
上面是老版本的写法，如果提示无效的过滤器`dns.resp.addr`，可以使用下面的新版命令
```
tshark -n  -f "dst port 53" -T fields -e dns.qry.name -e dns.a
```

#### 输出结果

```
lightcone.jd.com        211.151.10.150,123.126.36.173
logo.clearbit.com       52.85.82.40,52.85.82.50,52.85.82.241,52.85.82.178
lightcone.jd.com        211.151.10.150,123.126.36.173
www.ipip.net    		180.97.158.241
logo.clearbit.com       54.230.147.88,54.230.147.109,54.230.147.76,54.230.147.126
cloud.mongodb.com       18.210.185.2
```



### 统计http包

```
tshark -f "tcp  port 80 or  port 443 and host 58.68.234.140" -n -q -z http,stat, -z http,tree
```
#### 参数

`-q`：只有在抓包结束后才显示结果，通常用于统计

`-z`：统计变量，可以使用`tshark -z help  `查看

#### 输出结果

```
2249 packets captured

===================================================================
 HTTP/Packet Counter           value            rate         percent
-------------------------------------------------------------------
 Total HTTP Packets             350       0.000077                
  HTTP Request Packets           175       0.000038          50.00%
   POST                           172       0.000038          98.29%
   GET                              3       0.000001           1.71%
  HTTP Response Packets          174       0.000038          49.71%
   ???: broken                      0       0.000000           0.00%
   1xx: Informational               0       0.000000           0.00%
   2xx: Success                   174       0.000038         100.00%
    200 OK                         174       0.000038         100.00%
   3xx: Redirection                 0       0.000000           0.00%
   4xx: Client Error                0       0.000000           0.00%
   5xx: Server Error                0       0.000000           0.00%
  Other HTTP Packets               1       0.000000           0.29%

===================================================================

===================================================================
HTTP Statistics
* HTTP Status Codes in reply packets
    HTTP 200 OK
* List of HTTP Request methods
        POST  172 
         GET  3 
===================================================================
```

