Title: Openwrt新的Extroot姿势
Date: 2020-03-15 23:54
Category: 玩电脑
Tags: openwrt, extroot
Slug: new-extroot
Authors: Kevin Chen




之前写过一篇文章[用 extroot 为 openwrt 扩充存储空间](https://www.solarck.com/openwrt-extroot.html)，最近重装openwrt的时候，发现官方文档已经更新了扩展方法，觉得有必要单独写一篇作为更正，以免误导新人。



1. 首先，需要更新系统、安装必要程序

   ```
   opkg update && opkg install block-mount kmod-fs-ext4 kmod-usb-storage e2fsprogs kmod-usb-ohci kmod-usb-uhci fdisk usbutils
   ```

2. 之后更新rootfs数据

   ```
   DEVICE="$(awk -e '/\s\/overlay\s/{print $1}' /etc/mtab)"
   uci -q delete fstab.rwm
   uci set fstab.rwm="mount"
   uci set fstab.rwm.device="${DEVICE}"
   uci set fstab.rwm.target="/rwm"
   uci commit fstab
   ```

3. 然后格式化硬盘，后再次更新文件系统表

   ```
   mkfs.ext4 /dev/sda1
   
   DEVICE="/dev/sda1"
   eval $(block info "${DEVICE}" | grep -o -e "UUID=\S*")
   uci -q delete fstab.overlay
   uci set fstab.overlay="mount"
   uci set fstab.overlay.uuid="${UUID}"
   uci set fstab.overlay.target="/overlay"
   uci commit fstab
   ```

4. 最后，迁移数据

   ```
   mount /dev/sda1 /mnt
   cp -a -f /overlay/. /mnt
   umount /mnt
   ```

5. 重启，完成

   ```
   reboot
   ```

   

## 参考

- [Extroot configuration](https://openwrt.org/docs/guide-user/additional-software/extroot_configuration)