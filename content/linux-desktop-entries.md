Title: 自定义Linux桌面启动程序
Date: 2017-11-17 15:58
Category: IT笔记
Tags: linux
Slug: linux-desktop-entries
Authors: Kevin Chen


Anaconda自带的Spyder是一个我最喜欢使用的IDE，对于科学计算有很好的支持，但是在Linux上它并没有自带.desktop文件，所以并不能在程序列表里找到，每次都要手动在命令行执行才能开启，非常不方便，所以决定自己搜索下方法，自己给它添加一个桌面快捷方式。

Linux的主流DE的桌面文件都遵循[桌面配置项规范][1]，按照这个规范配置一个相应的.desktop文件，放在指定的目录即可，当然你也可以放在<code>~/.local/share/applications/</code>目录里，这样这个快捷方式只针对当前用户。

<!--more-->

```
sudo vim /usr/share/applications/spyder.desktop

[Desktop Entry]
Version=1.0
Type=Application
Name=Spyder
GenericName=Spyder
Comment=Scientific Python Development EnviRonment
TryExec=/opt/anaconda/bin/spyder
Exec=/opt/anaconda/bin/spyder
Categories=Development;Science;IDE;Qt;
Icon=/opt/anaconda/lib/python3.6/site-packages/spyder/images/spyder.png
Terminal=false
StartupNotify=false
```
TryExec和Exec后面是可执行文件的地址，可以只写后者
Icon是快捷方式的图标，没有的话可以去网上下载一个或者根据自己喜好随便放一个。
更多内容可以参考这篇[Wiki][2]
[1]:https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html#recognized-keys
[2]:https://wiki.archlinux.org/index.php/Desktop_entries_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
