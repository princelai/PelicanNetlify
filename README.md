# 使用方法

## 备份
cd to blog dir
```
./cp_theme.sh
git add *
git commit -m ''
git push origin master
fab github
```



## 恢复

### Only for first time excute

#### clone blog

cd to ~

```
git clone git@github.com:princelai/blog_backup.git Blog
```

#### 

#### clone output

cd to blog dir /Blog

```
git clone git@github.com:princelai/princelai.github.io.git output
```



#### install plugin

cd to pelican dir

```
git clone --recursive https://github.com/getpelican/pelican-plugins plugins
```



#### install themes

cd to this dir/themes

```
pelican-themes -i themes/plumage
pelican-themes -i themes/gum
pelican-themes -i themes/pelicanyan
```

#### 

### for evertimes excute

#### update blog

cd to ~

```
git pull origin master
```



#### update output 

cd to Blog

```
git pull origin master
```


#### update theme

cd to Blog

```
pelican-themes -r plumage
pelican-themes -i themes/plumage
```

