Title: 为原版Openwrt安装SSR-plus插件
Date: 2019-10-05 00:01
Category: 玩电脑
Tags: shadowsocks, v2ray, openwrt, lede
Slug: install-ssr-plus
Authors: Kevin Chen



之前文章提到过，我使用恩山lean大神的固件，主要是看中了他固件中的`luci-app-ssr-plus`这个插件，但是由于自己编译的固件稳定性上总是差点意思，不得已换回了官方原版openwrt，随之科学上网的插件也换成了`shadowsocks-libev`，这个插件是非常优秀的，但还是存在几个我非常介意的问题：

> 1. ss的特征貌似已经能被GFW识别，国庆前我的三台私人服务器就全挂了，全面换成v2ray是迫在眉睫，但是该插件只支持原版ss
> 2. 该插件的地址只能是IP地址，不支持域名，所以对于justmysocks这样被封后自动动换IP的服务就非常麻烦

v2ray官方没有提供我路由器架构的二进制文件，当然，openwrt就是以插件多闻名，其实可选的v2ray方案也很多，比如第三方固件[openwrt-v2ray](https://github.com/kuoruan/openwrt-v2ray)就提供了我需要的文件，再配合[luci-app-v2ray](https://github.com/kuoruan/luci-app-v2ray)也可以搭建出来，不过这套配置我是试过的，说实话配置起来比较复杂，DNS的解析转发、ChinaList、GFWList等功能也都需要自己来，所以我的第一选择还是`luci-app-ssr-plus`



在原版openwrt上使用这个插件有两种方法

> 1. 编译出适合架构的程序及依赖程序的ipk文件
> 2. 在原版系统中加入插件然后整体编译出一个固件刷入

我使用的是第一种方案，第二种方案没有尝试呢，有时间的话试过之后再来分享，下面正式开始。





## 编译插件

**注意：编译过程中必须全程全局科学上网，否则某些package下载不下来，有非常大的概率编译出错**



1. 首先要把lean的整套源码从github克隆下来，然后进入该目录

```bash
git clone https://github.com/coolsnowwolf/lede
cd lede
```



2. 然后为你的固件更新/安装扩展包

```bash
./scripts/feeds update -a && ./scripts/feeds install -a
```



3. 个性化你自己的固件

   这一步最为重要，先执行下面的命令
   
```bash
make menuconfig 
```

   之后会进入类似下面这样的界面，前三个分别是系统架构、子架构和路由器型号，这三个必须根据你自己的情况选对。

   ![menuconfig](https://ws1.sinaimg.cn/large/65f2a787ly1g7miwhzuafj21hc0h9q58.jpg)

   选择好以后，向下翻，找到LuCI --> Applications进入，找到图片中的插件然后空格选中

   ![menucconfig2](https://ws1.sinaimg.cn/large/65f2a787ly1g7miwhykvcj21hc0h9n03.jpg)

   由于我只用到了ss和v2ray，所以方括号中我只选择了我需要的，如有要用kcp和ssr可以相应选中，但是后续的依赖文件可能会更多。

   如果你在`luci-app-ssr-plus`处按M而不是空格，那么相当于把该插件编译为模块而不是编译入固件，这样做当然可以，但是建议第一次先全部编译，然后再次单独编译，不然单独编译一个插件会失败。

   

4. 下载所有脚本和程序

   这一步就是要科学上网的原因所在，不然很多程序不能顺利下载导致编译失败。

   代码最后的`-j5`可以把数字替换为你`CPU核数+1`。

```bash
make download -j5
```

   


5. 开始编译

   同上，数字可以改，核越多越快，这一步需要等待几分钟～几十分钟不等。

```bash
make -j5 V=s
```

   





## 安装依赖及插件

**在安装前，建议先看看我之前写过的两篇文章[升级 Openwrt/LEDE 大版本至 18.06](https://www.solarck.com/upgrade-lede-to-1806.html)或[LEDE/OpenWRT 路由器打造家庭媒体影音中心（一）](https://www.solarck.com/lede-media-center1.html)关于更换源那部分，这样会大大提升下载安装插件的速度。**

上面编译完成后，编译出的文件就可以在`bin/packages/路由器架构/base/`里找到你要的全部文件，先把`luci-app-ssr-plus`传到路由器安装试试。

```bash
cd bin/packages/arm_cortex-a9_vfpv3/base/
scp -P 22 luci-app-ssr-plus*.ipk root@192.168.250.1:/tmp/
```



切换到路由器shell执行（插件文件名每个人可能略有不同）

```bash
opkg install /tmp/luci-app-ssr-plus_1-99_all.ipk
```



如果你是原版openwrt，那么执行完安装后一定会报错，提示到不到依赖

```
 * satisfy_dependencies_for: Cannot satisfy the following dependencies for luci-app-ssr-plus:
 *      shadowsocksr-libev-alt
 *      ipset
 *      ip-full
 *      iptables-mod-tproxy
 *      dnsmasq-full
 *      coreutils
 *      coreutils-base64
 *      bash
 *      pdnsd-alt
 *      wget
 *      shadowsocks-libev-ss-redir
 *      v2ray
 * opkg_install_cmd: Cannot install package luci-app-ssr-plus.
```



你的提示可能会和我的有点出入，缺少的依赖或多或少，但一定会报错，原因就在于`luci-app-ssr-plus`依赖三个插件不在官方源中，所以我们要把下面几个编译好的插件传上路由器提前安装好。文件都在上面提到的目录中，上传方法也相同，这里就不赘述了。

> shadowsocksr-libev-alt
>
> pdnsd-alt
>
> v2ray

最后还有一点要注意的，在安装所有非官方依赖后，安装`luci-app-ssr-plus`前，还有一步操作。openwrt系统都会内置`dnsmasq`用于DNS服务，但是这个插件与`dnsmasq-full`是冲突的，所以要手动卸载掉，但是可以不手动安装，作为官方源中可以找到的依赖插件，它是可以自动安装的。

```bash
opkg remove dnsmasq
opkg install /tmp/luci-app-ssr-plus_1-99_all.ipk
```

安装好后，默认是看不到插件的，需要开启彩蛋，在路由器shell执行下面的命令

```bash
echo 0xDEADBEEF > /etc/config/google_fu_mode
```



至此就算大功告成。不过在我的路由器上还有一个小问题需要修复，没有问题的配置好自己的服务器应该就可以科学上网了，无需往下看。





## 替换pdnsd

在我安装配置好之后，依然不能访问外网，搜索一番发现[#817](https://github.com/coolsnowwolf/lede/issues/817)和[#1599](https://github.com/coolsnowwolf/lede/issues/1599)这两个问题和我遇到的一样，经过排查，问题确实出在pdnsd没有运行，索性我就用`dnsforwarder`把它替换掉。这个插件官方源中也不提供，不过好在有第三方提供，我们可以添加上直接使用，具体方法查看我之前的文章[路由器自动翻墙](https://www.solarck.com/lede-shadowsocks.html)中的安装密钥和新增源两部分。

准备就绪后就可以开始安装

```bash
opkg install dns-forwarder luci-app-dns-forwarder
```



最后按照下面两张图片分别设置好就可以了

1. dns-forwarder

   ![dnsforwarder](https://ws1.sinaimg.cn/large/65f2a787ly1g7mkknx28nj20ej08faa7.jpg)

2. ssr-plus

   ![ssrplus3](https://ws1.sinaimg.cn/large/65f2a787ly1g7mkknxataj20h70ak759.jpg)







## 后记

`luci-app-ssr-plus`在我的路由器上还是有些问题，比如运行模式那里，只有绕过中国大陆IP模式可用，GFW列表模式是不起效的，这样就导致有很多IP是国外的，但是国内访问速度还不错的网站也必须走代理。问题具体原因我还没有找到，目前只能说是凑合用，之后找到办法再说吧。