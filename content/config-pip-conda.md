Title: 配置pip和conda
Date: 2017-11-07 11:43
Category: IT笔记
Tags: pip,conda,python
Slug: config-pip-conda
Authors: Kevin Chen

首先需要确认已经安装Python环境，建议用于科学计算的朋友下载安装[Anaconda](https://www.anaconda.com/download/)或者[Miniconda](https://conda.io/miniconda.html)。

### 环境变量和启用配置
安装好后还需要把安装路径添加到系统环境变量

Linux用户查看系统环境变量
```bash
echo $PATH
```
Windows用户查看系统环境变量
```bash
echo %PATH%
```
如果没有Anaconda的路径，就需要自己手动添加



Linux用户编辑~/.bashrc，在最后添加以下内容，注意自己修改安装路径
```bash
export PATH="$HOME/anaconda3/bin:$PATH"
```
最后再执行
```bash
source ~/.bashrc
```
如果没有效果，可是尝试编辑~/.profile或 ~/.bash_profile文件
zsh或其他shell用户可以自行修改

Windows用户在cmd执行如下命令，如果不是默认安装到用户目录，需要手动修改下路径。如果创建了自定义env，那么root改为你自己的env名字。
```bash
set PATH=%USERPROFILE%\Anaconda3;%USERPROFILE%\Anaconda3\Library\bin;%USERPROFILE%\Anaconda3\Scripts;%PATH%
activate root
```
### 更换源
conda官方源非常慢，甚至有时候经常无法连接；pip时快时慢，也是经常无法连接，所以我们把更新源换为国内的，加快更新速度。

#### **pip**

目前国内常用的pip源有[阿里云](http://mirrors.aliyun.com/help/pypi)和豆瓣。

Linux用户编辑~/.pip/pip.conf文件，粘贴以下内容
```ini
[global]
index-url = https://pypi.doubanio.com/simple/
format = columns
```
或
```ini
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
format = columns
```

Windows用户编辑%USERPROFILE%\pip\pip.ini，没有就新建一个，内容和Linux一样。

#### **conda**

目前国内常用的conda源有[清华](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)和[中科大](http://mirrors.ustc.edu.cn/help/anaconda.html)两个

Linux和Windows用户执行下面的命令添加conda源
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

```bash
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```
### 更新
#### **conda**

conda常用更新命令

```bash
conda update XXX        #更新XXX包
conda update --all      #更新所有可更新的包到最新
conda update conda      #conda整体升级，并不一定最新，但是稳定
conda update anaconda   #同上
```

conda其他常用命令
```bash
conda info              #当前conda环境信息
conda install XXX       #安装XXX
conda search XXX        #搜索XXX
conda clean --all       #清除无用包和缓存
conda list > a.txt      #输出所有已安装的包
conda remove XXX        #卸载XXX
conda config --get channels     #获取当前使用的源，配合下面的命令使用
conda config --remove channels https://XXX
```

#### **pip**

pip常用更新命令

```bash
pip search XXX      #搜索
pip install XXX     #安装
pip uninstall XXX   #卸载
pip list > b.txt    #列出所有已安装的包
pip list -o         #列出所有可更新的包
pip show XXX        #查看包的路径和依赖等信息
```
