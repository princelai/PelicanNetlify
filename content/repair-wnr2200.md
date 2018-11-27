Title: 修复变砖的 WNR2200
Date: 2013-12-31 21:51
Category: 玩电脑
Tags: 路由器
Slug: repair-wnr2200
Authors: Kevin Chen

手中有个 NetGear WNR2200 路由器，当初买这个就是看重可以刷机,但是买回来才发现只能刷 DD-wrt，于是就刷了 DD 安心的用了半年。

最近看到 Openwrt 的 trunk 目录里有我这款机器的固件了，立刻操刀刷起。不幸的是刷完后 telnet 不通网关，failsafe 模式也无法开启。无奈中发现 NetGear 官网提供了 tftp 小工具确实有效，让我变砖的路由器起死回生。

方法也很简单，官方文库里说明的很详细，这里简单记录下要点。  
1.下载工具和路由器官方固件  
2.打开下载好的软件，设置好网关 192.168.1.1，加载下载好的固件，密码不用填  
3.断开路由器电源 10 秒左右，之后接通电源，立刻点击软件上的 Upgrade，等待修复完成

修复好后决定这个路由器还是老实的用 DD-wrt，抛开扩展性和一些不是特别常用的功能，DD-wrt 确实和所有路由器官方提供的固件一样人性化，当初刷完 DD-wrt 稳定运行了半年多，无重启、无断流，稳定性不是盖的。不想受 Openwrt 折磨的人可以在 DD-wrt 的[FTP 目录][3]里按照日期和型号索引自己的路由器。

当然自己也不会放弃 Openwrt，自己又入手了一个水星 MW4530r，300 元内可刷 Openwrt 的性价比神器,继续折腾 Openwrt 去了。

> [网件官方文库][1] [工具下载地址][2]  
> 如果地址不可用，可 Google tftp2.exe

[1]: http://neclub.netgear.cn/Knowledgebase/Document_detail.aspx?Did=934
[2]: http://www.shadowsoftware.net/shadowgameworld/downloads/tftp2.exe
[3]: ftp://dd-wrt.com/others/eko/BrainSlayer-V24-preSP2
