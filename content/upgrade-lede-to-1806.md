Title: 升级 Openwrt/LEDE 大版本至 18.06
Date: 2018-07-31 14:31
Category: IT 笔记
Tags: openwrt, lede
Slug: upgrade-lede-to-1806
Authors: Kevin Chen

# 下载升级包

首先下载新版文件，点击下方链接中任意一个，进入你的路由器架构，然后搜索路由器型号，如果你已经是 Openwrt/LEDE 系统，可以下载升级包\*-squashfs-sysupgrade.bin，如果不是，则要下载完整安装包\*-squashfs-factory.img。

[官方下载](https://downloads.openwrt.org/releases/18.06.0/targets/)

[中科大](https://mirrors.ustc.edu.cn/lede/releases/18.06.0/targets/)

[清华大学](https://mirrors.tuna.tsinghua.edu.cn/lede/releases/18.06.0/targets)

# 备份 & 更新

下载好文件后，进入路由器 Luci 界面，System ---> Backup / Flash Firmware

![backup and flash](http://kevinstuchuang.qiniudn.com/blog-pic/lede-backup-flash.png)

建议先备份一份配置到本地，备份好后，上传文件，开刷！等待路由器重启后进入后面的步骤。

# 更新源

关于详细的如何更换源操作，我在[LEDE/OpenWRT 路由器打造家庭媒体影音中心（一）](https://www.solarck.com/lede-media-center1.html)中有写，这里仅给出自定义源文件的内容。

`vim /etc/opkg/customfeeds.conf`

```ini
#Tsinghua
src/gz reboot_core https://mirrors.tuna.tsinghua.edu.cn/lede/releases/18.06.0/targets/mvebu/cortexa9/packages
src/gz reboot_base https://mirrors.tuna.tsinghua.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/base
src/gz reboot_luci https://mirrors.tuna.tsinghua.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/luci
src/gz reboot_packages https://mirrors.tuna.tsinghua.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/packages
src/gz reboot_routing https://mirrors.tuna.tsinghua.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/routing
src/gz reboot_telephony https://mirrors.tuna.tsinghua.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/telephony

#USTC
#src/gz reboot_core https://mirrors.ustc.edu.cn/lede/releases/18.06.0/targets/mvebu/cortexa9/packages
#src/gz reboot_base https://mirrors.ustc.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/base
#src/gz reboot_luci https://mirrors.ustc.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/luci
#src/gz reboot_packages https://mirrors.ustc.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/packages
#src/gz reboot_routing https://mirrors.ustc.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/routing
#src/gz reboot_telephony https://mirrors.ustc.edu.cn/lede/releases/18.06.0/packages/arm_cortex-a9_vfpv3/telephony

#shadowsocks
src/gz openwrt_dist http://openwrt-dist.sourceforge.net/packages/base/arm_cortex-a9_vfpv3
src/gz openwrt_dist_luci http://openwrt-dist.sourceforge.net/packages/luci
```

改好源后，可以使用下面的命令更新软件

```bash
opkg update
opkg list-upgradable | cut -f 1 -d ' ' | xargs opkg upgrade
```

# 一个无聊的脚本

整个过程到上面就已经结束了，不过本着继(凑)续(字)深(数)挖的态度，花点时间写了个 python 脚本，用来分析所有 ipk 包的升级情况。对了，写这个脚本的时候还发现有个源网址改变了，所以写自定义源的时候一定要注意。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 14:40:26 2018

@author: kevin
"""

from requests_html import HTMLSession
from collections import defaultdict

web_main = ['http://downloads.lede-project.org/releases/17.01.5',
            'http://downloads.lede-project.org/releases/18.06.0']
web_packages = [('/targets/mvebu/generic/packages/','/targets/mvebu/cortexa9/packages/'),
                '/packages/arm_cortex-a9_vfpv3/base',
                '/packages/arm_cortex-a9_vfpv3/luci',
                '/packages/arm_cortex-a9_vfpv3/packages',
                '/packages/arm_cortex-a9_vfpv3/routing',
                '/packages/arm_cortex-a9_vfpv3/telephony']

d = defaultdict(list)
for pack in web_packages:
    for i,main in enumerate(web_main):
        if isinstance(pack,tuple):
            website = main + pack[i]
        else:
            website = main + pack
        session = HTMLSession()
        resp = session.get(website,timeout=10)
        td = resp.html.find('body > table > tr > td > a')
        ispackages = [elem.text for elem in td if elem.text.endswith('.ipk')]
        for p in ispackages:
            packname,version,*_ = p.split('_')
            d[packname].append(version)

output_str = []
for k,v in d.items():
    if len(v) == 1:
        output_str.append('New Add:\t{}'.format(k))
    elif v[0] != v[1]:
        output_str.append('Version Up:\t{}|{} --> {}'.format(k,v[0],v[1]))
    else:
        pass

with open('lede_upgrade.txt','w') as f:
    f.write('\n'.join(output_str))
```

写完这个脚本才发现有个 bug，~~但是我懒得改了~~，我忽略了在两个版本的相同 packages 包中，一个有某软件包一个没有的情况，也就是说输出文件的`New Add`不是真正的新增，还有被剔除的包。

两个版本相同源地址的软件包共 6473 个，本次升级有版本升级、新增、剔除的包一共 5665 个，可见大部分还都是进行了例行的升级。

```bash
$ cat lede_upgrade.txt|grep "New Add"|wc -l
2180
```

新增、剔除的包共 2180 个，具体那个是新增哪个是剔除我没有区分出来。

```bash
$ cat lede_upgrade.txt|grep "Version Up"|wc -l
3485
```

版本升级的包有 3485 个，这两项加起来正好 5665 个。

由于版本号的命名十分不规则，本来还想弄个大版本号、次版本号、小版本号的对比，无奈最终还是搁浅了。
