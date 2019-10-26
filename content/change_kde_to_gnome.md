Title: 从KDE切换到Gnome
Date: 2019-10-26 16:43
Category: 机器学习,金融与算法,玩电脑,杂记
Tags:
Slug: change_kde_to_gnome
Authors: Kevin Chen
Status: draft



MysqlBench，deepin-wxwork



```
sudo pacman -Rcns manjaro-kde-settings
sudo pacman -S gnome gnome-extra gdm manjaro-gnome-assets manjaro-gdm-theme manjaro-settings-manager 

sudo systemctl disable sddm -f
sudo systemctl enable gdm.service -f

sudo pacman -Rcns plasma kio-extras kde-applications kdebase sddm manjaro-kde-settings sddm-breath-theme manjaro-settings-manager-knotifier manjaro-settings-manager-kcm

https://wiki.manjaro.org/index.php/Install_Desktop_Environments#Gnome_3
https://linuxconfig.org/how-to-install-gnome-desktop-on-manjaro-18-linux
```

