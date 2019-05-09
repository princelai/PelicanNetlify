Title:
Date: 2019-02-13 14:33
Category: 杂记
Tags: darktable
Slug: darktable
Authors: Kevin Chen
Status: draft



## 中文

获取中文mo文件
```
wget -o zh_CN.po https://raw.githubusercontent.com/darktable-org/darktable/master/po/zh_CN.po
```

转换

```
yaourt -S poedit
msgfmt -o darktable.mo zh_CN.po
sudo cp darktable.mo /usr/share/locale/zh_CN/LC_MESSAGES
```

