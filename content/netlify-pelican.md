Title: Netlify全自动部署静态博客
Date: 2018-11-20 14:08
Category: IT笔记
Tags: netligy, pelican
Slug: using-netlify-auto-deployed-pelican
Authors: Kevin Chen



![netlify](https://flaviocopes.com/netlify/netlify-logo.png)

> Netlify是一家位于旧金山的云计算公司，为静态网站提供托管和无服务器后端服务。 它具有Git在全球应用交付网络中的持续部署，无服务器表单处理，对AWS Lambda功能的支持以及与Let's Encrypt的完全集成。它提供免费和付费计划。 [维基百科（英文)](https://en.wikipedia.org/wiki/Netlify)



在之前，我使用Python写的Pelican程序生成静态博客，然后托管到Github Pages。长期使用这个组合后，发现这样有很多缺点：

1. github pages在国内访问速度较慢，有的地方甚至给屏蔽掉了。

2. 使用免费版cloudflare加速效果并不明显，要调教的东西还很多
3. 跨平台非常麻烦，因为github pages只接受output文件夹（只包含HTML），其余的环境还需要建个仓库备份起来。



在了解了Netlify的作用之后，我发现网上写的教程都是怎么把它当做一个静态环境使用，也就是类似于github pages，完全忽略了他的自动部署功能，然而这个功能才是我迁移到Netlify的最大理由。下面说说怎么一步步完成迁移。



## 一、在github新建一个repo

我之前的博客就是托管在github的，但是原来的是github pages，原来的仓库里只有静态html，而新建的这个仓库将来会把所有环境放进去，让Netlify帮我自动生成静态文章。



新建好后就先放在那，最后才会用到。

![new repo](https://ws1.sinaimg.cn/large/65f2a787ly1fxdivt257cj20l40i1wfs.jpg)



## 二、本地新建模拟环境

我自己的Python环境是3.7.1，Netlify当前对Python的最高支持版本是3.6.4。版本其实在这里并无所谓，因为我们以后也不会在本地生成静态网页了，这一步主要是为了得到一个最小的环境告诉Netlify。



我使用的是conda管理环境，新建激活环境非常简单

```bash
conda create -n pelican36 python==3.6.7
conda activate pelican36
```



根据Pelican官方文档的安装说明和自己的测试，在一个新环境中只需要安装如下几个包就可以让Pelican运行

```
pip install pelican markdown typogrify bs4
```



## 三、初始化博客文件夹

安装好Python环境和Pelican后，初始化博客就很简单了，只要一个命令就可以完成

```bash
mkdir Blog
cd Blog
pelican-quickstart
```

详细内容可以参考[Pelican文档](http://docs.getpelican.com/en/stable/install.html)





## 四、安装Pelican主题和插件

在Blog根目录新建两个文件夹

`themes` : 这个目录用于存放你要用的主题，大量主题可以在Github搜索

`plugins ` : 这个目录用于你要用的主题必须的插件， Pelican所有插件可以在[这里](https://github.com/getpelican/pelican-plugins)找到





##　五、博客生成环境

之后把这个最精简环境及依赖输出为文件

```
pip freeze > requirements.txt
```



如果你懒得新建环境，就按照我的来写问题应该不大

```
beautifulsoup4==4.6.3
blinker==1.4
bs4==0.0.1
certifi==2018.10.15
docutils==0.14
feedgenerator==1.9
Jinja2==2.10
Markdown==3.0.1
MarkupSafe==1.1.0
pelican==4.0.0
Pygments==2.2.0
python-dateutil==2.7.5
pytz==2018.7
six==1.11.0
smartypants==2.0.1
typogrify==2.0.7
Unidecode==1.0.22
```



这一步就是为了得到`requirements.txt`，要把这个文件放在blog文件夹的根目录





## 六、Netlify部署配置

这一步更简单，只需要一条命令

```
echo "3.6" > runtime.txt
```

在blog根目录执行这条命令，是为了告诉Netlify我们要用Python3.6而不是默认的2.7





## 七、把Blog上传至github

一切准备工作都已就绪，最终的目录应该像下面这样

`tree  -L 1 --dirsfirst Blog`

```
Blog
├── content # Pelican自动生成的目录，这里放你写的Markdown文件
├── output # Pelican自动生成的目录，如果你不需要在本地预览可以删掉
├── plugins # 步骤四新建的，放置需要的插件，插件在pelicanconf.py中指明
├── themes # 步骤四新建的，放置需要的主题，主题在pelicanconf.py中指明
├── fabfile.py # Fabric配置文件，用于自动化执行本地操作（类似宏）
├── pelicanconf.py # Pelican主配置文件
├── publishconf.py # Pelican发布配置文件
├── README.md
├── requirements.txt # 步骤五生成的
└── runtime.txt # 步骤六生成的
```



还记得步骤一新建的repo还放在那里，我们要把整个Blog文件夹同步到github，按照步骤一中的指导操作，不过建议在add和commit前把gitignore加上

```bash
echo ".directory\n__pycache__/\noutput/\n\!.gitignore\n" > .gitignore 
```





## 八、关联Netlify和Github

我选择使用github账号[登录Netlify](https://app.netlify.com/)，然后需要为Netlify授权可以访问那个仓库，如图，这里选择步骤一中新建好的repo。

![Netlify connect Github](https://ws1.sinaimg.cn/large/65f2a787ly1fxdivt26fpj20l80rpmyp.jpg)





连接授权完成后，还是选择这个repo，然后下一步。

![pick repo](https://ws1.sinaimg.cn/large/65f2a787ly1fxdivt23b9j20yv0lj3zv.jpg)





在编译和部署的最后一步，需要填入下面的命令

`Build command`  : 

`pelican -d -s publishconf.py -t themes/plumage`

使用publishconf.py配置，主题使用themes文件夹下的plumage来生成静态网页，每次生成前都删除output文件夹。



`Publish directory`  : 

`output`

生成的文件放在output文件夹，如果你要使用其他文件夹，除了要修改这里，还要修改pelicanconf.py文件内的配置。

![build option](https://ws1.sinaimg.cn/large/65f2a787ly1fxdivt2rozj20yz0px401.jpg)





## 九、绑定域名和https

在Netlify的后台Settings --> Domain Management设置页面里，填入你的域名，之后要在你的域名管理商那里进行设置，方式有两种：

1. 增加一条A记录，指向`104.198.14.52`

2. 修改NS记录为如下内容

   > dns1.p05.nsone.net
   >
   > dns2.p05.nsone.net
   >
   > dns3.p05.nsone.net
   >
   > dns4.p05.nsone.net

使用第二种方法更简单，我就用这种方法把域名全权托管给Netlify了。





设置好上面内容后就可以申请SSL证书了，Netlify使用[Let’s Encrypt](https://letsencrypt.org/)免费证书还是在相同的页面内申请，等待证书生效就好了。





## 更自动化的配置

我使用fabric再次简化工作，首先需要安装fabric扩展包

```bash
pip install fabric3
```



之后在Blog根目录新建一个`fabfile.py`文件，Pelican初始化的博客文件夹可能自带了该文件，我只是对其进行了大幅瘦身和修改

```python
import os
from datetime import datetime

from fabric.api import env, local

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
env.content_path = 'content'


META = """Title:
Date: {:%Y-%m-%d %H:%M}
Category: IT笔记, 金融笔记
Tags:
Slug:
Authors: Kevin Chen
Status: draft
"""


def new():
    os.chdir(env.content_path)
    with open('new.md', 'w') as f:
        f.write(META.format(datetime.now()))

def preview():
    local('pelican -d -s pelicanconf.py')
    os.chdir(env.deploy_path)
    local('python -m http.server 8000 -b 127.0.0.1')


def github():
    local('git add --all')
    local('git commit -m "update at {:%Y-%m-%d %H:%M}"'.format(datetime.now()))
    local('git push origin master')

```



可用的命令有三个：

`fab new` : 在content文件夹内新建一个new.md文件，并初始化META信息

`fab preview` : 生成静态文件，并开启一个python的simpleHTTPServer

`fab github` : 自动添加文件并上传至github，剩余的工作就交给Netlify了