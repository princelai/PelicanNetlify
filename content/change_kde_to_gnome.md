Title: 从KDE切换到Gnome
Date: 2019-10-26 17:34
Category: 玩电脑
Tags: kde,gnome,linux
Slug: change_kde_to_gnome
Authors: Kevin Chen

<br />

在新单位中，经常要用到MysqlBench，这个软件的密码存储使用的是`gnome-keyring`，而且必须使用企业微信这种软件，例如deepin-wxwork，这个软件依赖于`gnome-settings-daemon`。然而我使用的是KDE桌面系统，有轻微洁癖的我很难接受Gnome和KDE共存于系统，在加上KDE有点审美疲劳，就尝试把我的Manjaro KDE换为Gnome桌面。

<br />

查阅了一些网上资料后，发现其实也很简单，至少比重新安装要简单很多。首先要进入单用户模式，你可以在网上搜索这个词，有很多的教程，其实就是在grub启动内核那段代码后加上`single`字符串即可在启动的时候直接进入命令行而不启动X11图形界面。

<br />

然后要卸载KDE的一个组件，不然会和Gnome冲突

```bash
pacman -Rcns manjaro-kde-settings
```

<br />

接下来安装Gnome所有组件，我这里是安装了全部

```bash
pacman -S gnome gnome-extra gdm manjaro-gnome-assets manjaro-gdm-theme manjaro-settings-manager 
```

<br />

安装完毕后，先把KDE的登录服务sddm替换为Gnome的gdm

```bash
systemctl disable sddm -f
systemctl enable gdm.service -f
```

<br />

最后卸载KDE所有组件即可

```bash
pacman -Rcns plasma kio-extras kde-applications kdebase sddm manjaro-kde-settings sddm-breath-theme manjaro-settings-manager-knotifier manjaro-settings-manager-kcm
```

当然我这里卸载的并不全，KDE的组件很多，需要利用shell的提示所有kde开头的程序并删除。

<br />

大功告成，现在可以重启系统，启动后就能看到gdm的登录界面了，不过当前这个版本我还遇到一个问题，就是文件管理器nautilus打不开，在命令行启动就能看到报错，提示找不到`libgnome-desktop-3.so.17`库文件，临时的解决办法就是把现有的高版本库文件链接到这个低版本的哭文件上

```bash
cd /usr/lib
sudo ln -s libgnome-desktop-3.so.18 libgnome-desktop-3.so.17
```

<br />

好了，剩下的就是个性化调整时间了。不过不得不说一下，我用的版本是3.34.1版本的Gnome，相比与KDE，卡顿非常明显，非常非常明显，有的时候能够卡住3-5秒，卡住1-2秒简直就是家常便饭，所以已经在用KDE且没有特别原因还是不建议瞎折腾。



<br />

## 参考

1. [Install_Desktop_Environments](https://wiki.manjaro.org/index.php/Install_Desktop_Environments#Gnome_3)
2. [how to install gnome desktop on manjaro 18 linux](https://linuxconfig.org/how-to-install-gnome-desktop-on-manjaro-18-linux)