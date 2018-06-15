# 使用方法

## 备份
cd to blog dir
```
./cp_theme.sh
git add *
git commit -m ''
git push origin master
```

## 恢复
### install plugin
cd to pelican dir
```
git clone --recursive https://github.com/getpelican/pelican-plugins plugins
```

### install themes
cd to this dir/themes
```
pelican-themes -i themes/plumage
pelican-themes -i themes/gum
pelican-themes -i themes/pelicanyan
```

### clone blog
cd to ~
```
git clone git@github.com:princelai/blog_backup.git Blog
```
### first clone output
cd to blog dir
```
git clone git@github.com:princelai/princelai.github.io.git output
```

### sync output eveytimes
```
git pull origin master
```