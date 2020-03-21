Title: 一文玩转V2ray 透明代理
Date: 2020-03-16 02:26
Category: 玩电脑
Tags: openwrt,v2ray
Slug: openwrt-v2ray
Authors: Kevin Chen



<br />

本文主要是自己配置过程的流水帐，也算作是一个备份，防止以后再弄的时候忘了流程。本文使用[openwrt-v2ray](https://github.com/kuoruan/openwrt-v2ray)和[luci-app-v2ray](https://github.com/kuoruan/luci-app-v2ray)作为配置工具，前者为V2ray的Openwrt的二进制文件，后者为可视化的配置工具。经过一段时间的摸索，发现该配置工具比原版V2ray+手动配置透明代理要简单的多，希望能够帮助到正在研究V2ray+透明代理的玩家。

<br />



## 更换源

### 1.安装支持https的工具

如果你想快速安装软件，那么必须换成国内的openwrt的源，但是目前国内好用的源都是https的。

```bash
opkg update
opkg install ca-certificates luci-ssl-openssl
```

<br />



### 2.替换系统源（推荐）

编辑源文件`/etc/opkg/customfeeds.conf`，我是软路由，所以是x86_64，请根据自己实际情况替换这部分。最后的kmod那条可加可不加，这个自己随意。编辑好自定义源文件后，还要把同目录下系统自带的源文件`distfeeds.conf`里的内容全部注释掉或删除。自定义源文件内容如下：

```ini
src/gz openwrt_core https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/19.07.1/targets/x86/64/packages
src/gz openwrt_base https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/19.07.1/packages/x86_64/base
src/gz openwrt_luci https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/19.07.1/packages/x86_64/luci
src/gz openwrt_packages https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/19.07.1/packages/x86_64/packages
src/gz openwrt_routing https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/19.07.1/packages/x86_64/routing
src/gz openwrt_telephony https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/19.07.1/packages/x86_64/telephony
src/gz openwrt_kmods https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/19.07.1/targets/x86/64/kmods/4.14.167-1-e1dd7676581672f6f0bdb1363506dee1
```

<br />

如果不知道自己的架构，可以使用下面的命令查询

```bash
opkg print-architecture | awk '{print $2}'
```

<br />

### 3.安装openwrt-v2ray

openwrt-v2ray作者非常良心，提供了多种架构的编译文件，以及可以在线更新的源，方便日后更新使用，但我们要先把第三方源的key导入才能正常使用。

```bash
wget -O kuoruan-public.key http://openwrt.kuoruan.net/packages/public.key
opkg-key add kuoruan-public.key
```



<br />

然后在上面提到的**自定义源**里增加下面的内容，注意替换架构目录。

```ini
src/gz kuoruan_packages https://openwrt.kuoruan.net/packages/releases/x86_64/
src/gz kuoruan_universal https://openwrt.kuoruan.net/packages/releases/all
```



<br />

### 4.添加Shadowsocks源（可跳过）

方法同上，这里就不赘述了。需要说明的是，这个源是安装ss和dns-forward这类工具的源，有需要可以添加，没需要就跳过吧，我下面的教程没有用到这里的相关程序。

```bash
wget http://openwrt-dist.sourceforge.net/openwrt-dist.pub
opkg-key add openwrt-dist.pub
```

<br />

**注意替换为自己的架构**

```ini
src/gz openwrt_dist http://openwrt-dist.sourceforge.net/packages/base/x86_64/
src/gz openwrt_dist_luci http://openwrt-dist.sourceforge.net/packages/luci
```



<br />

##  安装软件

### 5.替换dnsmasq

系统自带的dnsmasq功能不全，需要替换掉，而dnsmasq又是系统重要的组成部分（负责分配ip的dhcp和dns解析那部分工作），所以一旦删除，可能会短暂的无法联网，需要先下载到本地再安装，下面的方法和顺序都是用血泪探索出来的。

注意，我下面的代码没有写错，第一条是下载ipk文件到本地，第二条dnsmasq-full安装一定会失败，但目的是让系统自动安装所需要的依赖。

```bash
opkg download dnsmasq-full
opkg install dnsmasq-full
opkg remove dnsmasq
opkg install dnsmasq-full_2.80-15_x86_64.ipk
rm dnsmasq-full_2.80-15_x86_64.ipk 
```

<br />

### 6.全面更新（可以跳过）

我是更新强迫党，要尽量保持软件最新。

```bash
opkg update
opkg list-upgradable | cut -f 1 -d ' ' | xargs opkg upgrade
```



<br />

### 7.安装全部插件

下面包含了必要软件、系统工具和部分中文翻译补丁，建议全部安装，如果路由器空间实在不够，可以看看我写的Extroot教程。

```bash
opkg update
opkg install luci-i18n-base-zh-cn uhttpd libuhttpd-openssl luci-app-uhttpd luci-i18n-uhttpd-zh-cn ip-full ipset iptables-mod-tproxy iptables-mod-nat-extra libpthread coreutils-base64 ca-bundle curl vim-full vim-runtime v2ray-core luci-app-v2ray luci-i18n-v2ray-zh-cn
```

<br />

安装好openwrt-v2ray后需要为geo文件增加执行权限，不然启动可能报错， 即使你用不到这两个文件。

```bash
chmod a+x /usr/bin/geoip.dat 
chmod a+x /usr/bin/geosite.dat
```



<br />

## 可视化配置V2ray

配置v2ray其实是一个很痛苦的过程，一旦按照官方弄好就懒得再去折腾。我开始使用luci-app-v2ray的时候就觉得摸不着头脑，只想直接加载配置好的json文件，但是这样弄真是问题多多，需要手动下载更新中国CIDR文件和GFWlist文件，还需要配置dnsmasq和ipset，然后再配合iptables等等，一旦重装，这些东西想想就头疼。后来经过几次尝试，发现luci-app-v2ray其实非常的好用，上面说的问题只要配置好，都是一键启动，这里把我的配置步骤一步步贴出来，供还没有找到门路的各位参考，而且luci-app-v2ray的官方文档也做的不好，这里就当为他们做个推广教程。

<br />

### 入站连接

按照上面安装好所有软件后，我们要从服务--V2Ray进入主界面，先不看全局设置，来看看入站连接，如图

![openwrt-v2ray_2.png](https://wx1.sinaimg.cn/large/65f2a787ly1gcv4fdk2psj21hc16ujvm.jpg)
这是默认就带的一个配置，没有的话就按照我图中的完整复制一份也可以，你只需要修改一个你喜欢的端口号就可以了，注意别把协议改了。

<br />

### 出站连接

然后来看看出站连接，下图是整体配置，绿色框内是我把默认配置删除后留下的两个，完全没有修改。黄色框内是我新增的三台服务器，因为之后我要用到负载均衡，当然你就一台也没关系，不使用负载均衡就可以了。

![openwrt-v2ray_3.png](https://wx1.sinaimg.cn/large/65f2a787ly1gcv4fdkciyj20ri0h8767.jpg)



<br />


随便看一个服务器的配置里，按照你自己服务器的连接方式配置好，相信搞过官方json配置文件的都能看明白这些配置的含义，我这里是用的WS+TLS，所以必须要用443端口。黄色框内是标识名，用于负载均衡，用不到的话可以不写。

![openwrt-v2ray_4.png](https://wx1.sinaimg.cn/large/65f2a787ly1gcv4fdmfyqj21hc1bbjvl.jpg)



<br />

### 路由

路由部分稍微复杂一点，同样，绿色框内是默认配置就带的，我没有修改。下方黄色框内是我自己添加的一个配置，用于真实的代理，这个之后再看，上方黄色框内打勾的是最后启动的配置，所以我只是启用了个别的路由配置。蓝色框内是负载均衡的配置，最下方的标识匹配要和你出站连接里的标识一致。

![openwrt-v2ray_5.png](https://wx1.sinaimg.cn/large/65f2a787ly1gcv4fdk4o1j21hc10ywi7.jpg)



<br />

下面这个图就是我新增的真实代理路由规则，配置非常简单，含义就是所有TCP和UDP连接都走负载均衡器，当然如果你没有设置负载均衡，那么就要设置好出站连接标识。
![openwrt-v2ray_6.png](https://wx1.sinaimg.cn/large/65f2a787ly1gcv4fdkjqfj21hc0qbq5u.jpg)



<br />

上面我的代理配置为什么这么简单，还要把我的代理架构简单说一下。所有路由条件其实都在路由器的iptables/ipset层面完成了，能够被输送到v2ray的连接一定是被屏蔽了的，所以可以理解为只要进入v2ray路由系统的一定要走代理，我这里是在v2ray的路由系统中新增了BT下载和去广告的过滤，把这两个规则去掉其实就更好理解了。
![v2ray透明代理架构.png](https://wx1.sinaimg.cn/large/65f2a787ly1gcv4fdomjpj20qo0ogq4m.jpg)



<br />


### 透明代理
搞懂了路由路线，再来看看最重要的透明代理设置，就是由于luci-app-v2ray有这部分的配置，省下玩家去搞iptables、ipset和dnsmasq这部分的工作。整体也是非常的简单，但是需要注意的是红框内的部分，我没有开启任何UDP相关的转发，因为一旦开启转发DNS，再配合我上面的路由，那么所有的DNS都要走国外，这让访问国内的网站非常的慢;如果开启UDP转发，那么所有网络都访问不通，这个原因我还没有弄清，不知道是bug还是我没有完全搞明白透明代理。蓝色框内就是帮你完成iptables、ipset和dnsmasq要完成的所有工作，弥补了上面有几率被DNS污染的缺点，也算是在简单和完美之间找到了一个平衡。
![openwrt-v2ray_7.png](https://wx1.sinaimg.cn/large/65f2a787ly1gcv4fdp6tcj21hc14jdk8.jpg)

<br />


### 全局设置
最后全部设置完成再回过头来看看全局设置，黄色框内勾选好你要启用的各组件的配置，然后勾上已启用，最后保存并应用，不出意外，你的透明代理就搭建好了。

![openwrt-v2ray_1.png](https://wx1.sinaimg.cn/large/65f2a787ly1gcv4fdjuznj20qr0qbgnt.jpg)



<br />

## 结语

V2ray的玩法很多，配套工具也很丰富，这里只是抛砖引玉，希望大家布不局限于此。我这套东西前前后后折腾了几个月才弄明白，现在已经在家里三个路由器上实验成功，最短也只需要1小时左右就能完全搞定，现在路由器重装起来也不发愁了。另外这套配置不能够代理Telegram手机客户端，添加IP也不行，不知道是不是与UDP有关系，我在入站、出站和路由上搞过MTproxy协议，但是一旦使用，v2ray程序就会崩溃，所以就没再尝试了。最后还有一个小技巧，luci-app-v2ray的配置文件在`/etc/config/v2ray`，每次只要保存了这个文件，在新的路由器上覆盖配置就能快速配置好哦。