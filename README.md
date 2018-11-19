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



# using netlify

python env

```
conda create -n pelican36 python==3.6.7
```

激活

```
conda activate pelican36
```



安装必要扩展

```
pip install pelican markdown typogrify bs4
```







install pelican themes and plugins



```
echo ".directory\n__pycache__/\noutput/\n\!.gitignore\n" >> .gitignore  
```



新建github

```python
git remote add origin git@github.com:princelai/PelicanNetlify.git
git push -u origin master
```



```
pelican -s publishconf.py -t themes/plumage  
```





```
/opt/Anaconda/envs/pelican36/bin/pelican ~/Blog/content/ -s publishconf.py -t themes/plumage
```



```
pip freeze > requirements.txt
echo "3.6" > runtime.txt
```

