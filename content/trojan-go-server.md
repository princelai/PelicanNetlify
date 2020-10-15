Title: 家庭出国网络升级（一）：使用trojan-go作为服务端
Date: 2020-10-16 1:18
Category: 玩电脑
Tags: trojan-go, nginx, v2ray
Slug: trojan-go-server
Authors: Kevin Chen



## 1. 写在前面

​    我使用V2ray已经有一年时间，之前一直在用websocket+tls+web这套配置，路由器上使用openwrt-v2ray作为客户端，这套配置非常稳定，一年多来三台VPS从没出现问题。但当下v2ray也在研发新的vless协议，但作为beta版本很多客户端还没有跟进，而trojan-go作为trojan的升级版本异军突起也非常引人注意。最近手痒痒，不升级到新版就难受，另外考虑到

> 1. openwrt上还没有对vless协议有支持的客户端
> 2. caddy V2配置比V1复杂很多，而且效率低于Nginx
> 3. V2ray的server端配置更为复杂（我喜欢纯手动配置，不用一键脚本）

​    综上，我决定对家里全套扶墙设备进行更新，软路由上的客户端用openclash替代，服务端用trojan-go替代，而trojan-go只要不开启一些功能是兼容trojan的，所以在openwrt，Android，Linux平台上都能得到很好的兼容。

​    这篇文章只是第一篇，只讲服务端trojan-go的配置方法，后面第二篇再来写软路由上openclash的配置方法。

<br/>

<br/>

## 2. 签发HTTPS证书acme.sh
​    在我原来的方案中，前置代理使用的是caddy v1，使用这个软件的目的也很简单，配置简单，能自动签发HTTPS证书，这就免去了很多工作。

​    但一年多过去了，caddy v2发布，不仅配置文件更加复杂，并且我还看了很多和Nginx的效率对比视频，结果都是Nginx完胜，对于我这种速度本来就不快的小鸡，再损失速度就真的没法正常用了，最后还是下定决心，将caddy更换为nginx，所以签发证书的工作就要自己手动完成。

​    首先在VPS服务器上需要更新系统并安装socat程序

```bash
apt-get update
apt-get install socat
```

<br/>

​    然后需要提前为trojan-go创建一个配置目录，用于存放trojan-go的服务端配置，当然我还把证书文件也放到了这里，这个可以根据跟人喜好进行更换。

```bash
mkdir /etc/trojan-go/
```

<br/>

​    就后就是签发证书，使用的是acme.sh，四行代码就搞定。注意需要将`domain`替换为你真实的网址，如果你不上按照上面创建的目录，还需要将第三条命令的`/etc/trojan-go/`目录替换为你创建的目录。

```bash
curl  https://get.acme.sh | sh
```

````
~/.acme.sh/acme.sh --issue -d domain --standalone -k ec-256
````

````
~/.acme.sh/acme.sh --installcert -d domain --fullchainpath /etc/trojan-go/tls.crt --keypath /etc/trojan-go/tls.key --ecc
````

​    最后为生成好的证书文件加上其他用户的读和执行权限，到此证书就申请完成，而acme.sh也会为你在crontab上添加一条自动重申请的命令，之后也无需在为此操心。

```
chmod 664 /etc/trojan-go/tls*
```

<br/>

<br/>

## 安装配置Nginx
​    因为我使用的VPS服务器安装的是Debian 10版本，如果你用的不是Debian或者Ubuntu，那么你需要去网上搜索下安装命令和包名称。目前我的系统自带的Nginx版本是1.14，不需要编译，不需要自己再安装插件，开箱即用。唯一需要注意的是安装的时候要保证80端口是空闲的。
```bash
apt-get install nginx-full
```

<br/>

​    虽然不是必须的，但是安装完后我还是建议执行下

```bash
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
```

命令来备份下原始配置，接下来编辑该配置文件

`vim /etc/nginx/nginx.conf`

```ini
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        multi_accept on;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;


        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*.conf;
}
```

​    该配置文件就是通过简单修改原始配置文件得到的，需要注意的有两点

> 1. 我开启了TLSv1.3，你需要确认你的VPS服务器上openssl程序是否大于等于1.1.1版本，如果低于这个版本只能用TLSv1.1、TLSv1.2
> 2. 最后一行的`/etc/nginx/sites-enabled/`文件夹内有一个default文件，我没有删除，为了不匹配上这个文件，新建的文件都带上了`.conf`后缀，所以这里也要相应的加上

<br/>

​    接下来就要创建站点配置文件，使用

```bash
touch /etc/nginx/sites-enabled/site.conf
```

命令创建文件，然后编辑该文件填入如下配置

`vim /etc/nginx/sites-enabled/site.conf`

```ini
server {
      listen 80 default_server;
      listen [::]:80;

      server_name _;

      root /var/www/html/;
      index index.html;
      error_page 404 /404.html;

      location / {
              try_files $uri $uri/ =404;
      }
}

server {
    listen 23443 ssl default_server;
    listen [::]:23443 ssl;
    
    server_name _;
    
    ssl_certificate /etc/trojan-go/tls.crt;
    ssl_certificate_key /etc/trojan-go/tls.key;    

    return 400;
}
```

​    这段配置也有几点要说明注意的

> 1. 因为我有好几台VPS，为了配置通用，我将服务器域名写为`server_name _;`，如果你只有一台，还是建议写为`server_name example.com;`
> 2. 本地文件目录在`/var/www/html/`，不是`/var/www/`也不是`/var/www/example.com/`，当然这里可以根据自己的喜好修改
> 3. 证书文件在`/etc/trojan-go/`，也就是申请证书时填写的安装目录

​    上面的配置文件创建了2个站点，分别监听了IPv4和IPv6的80和23443端口，这里IPv6用不到可以去掉，23443这个fallback端口可以任意更改到一个未被占用的端口，甚至可以将第二段server配置去掉，不开启trojan-go的fallback功能。

<br/>

​    接下来还需要准备2个网页，一个首页一个404页面，其实404页面有没有无所谓，我这里就是将我的blog简单的拷贝下来存入nginx本地文件目录，你也可以网上随便找个模板放进去，只要保证服务和端口可以访问就可以，内容并不重要。

```bash
curl https://www.solarck.com/ -o /var/www/html/index.html
curl https://www.solarck.com/404.html -o /var/www/html/404.html
```

<br/>

​    最后开启nginx服务，如果严格按上面操作应该会一次成功，如果没有正确启动nginx服务，那么启动trojan-go的时候会报错。

```bash
systemctl start nginx.service
systemctl enable nginx.service
```

<br/>

​    最后的最后，如果你乐意，还可以在定时任务里添加一个任务，定时把要展示的网页拷贝下来。

```bash
35 3 * * 2 curl https://www.solarck.com/ -o /var/www/html/index.html
```

<br/>

<br/>

## 安装配置trojan-go
​	先做一些准内工作，创建一个目录，用来存放`trojan-go`使用的文件，最终这里只会存放`geoip.dat`和`geosite.dat`

```bash
mkdir /usr/share/trojan-go/
```

<br/>

​    trojan-go没有被收录到系统源里，所以要手动下载安装

```bash
wget https://github.com/p4gefau1t/trojan-go/releases/download/v0.8.2/trojan-go-linux-amd64.zip
```

<br/>

​    解压缩，这里会将压缩包里所有文件解压到一个名为`trojan-go`的文件夹内

```bash
unzip trojan-go-linux-amd64.zip -d trojan-go
```

<br/>

​    切换至目录内

````bash
cd trojan-go
````

<br/>

​	下面的代码是将`systemd`服务文件拷贝到指定目录

```bash
cp example/trojan-go.service example/trojan-go@.service /etc/systemd/system/
```

<br/>

​	将trojan-go的二进制执行文件拷贝到系统`$PATH`

```bash
cp trojan-go /usr/bin/
cp trojan-go /usr/local/bin/
```

<br/>

​	最后将`geoip.dat`和`geosite.dat`拷贝到刚才创建好的目录内存放，至此安装就结束了

```
cp geo* /usr/share/trojan-go/
```
<br/>

​	安装完成就需要修改配置文件，首先是切换到`trojan-go`配置文件目录内并创建一个空文件

```bash
cd /etc/trojan-go/
touch config.json
```

<br/>

然后修改该文件，将下面的配置拷贝进去

`vim config.json`

```json
{
    "run_type": "server",
    "local_addr": "0.0.0.0",
    "local_port": 443,
    "remote_addr": "127.0.0.1",
    "remote_port": 80,
    "password": [
        "your_password"
    ],
    "ssl": {
        "cert": "/etc/trojan-go/tls.crt",
        "key": "/etc/trojan-go/tls.key",
        "fallback_addr": "127.0.0.1",
        "fallback_port": 23443
    },
    "router": {
        "enabled": true,
        "block": [
            "geoip:private"
        ],
        "geoip": "/usr/share/trojan-go/geoip.dat",
        "geosite": "/usr/share/trojan-go/geosite.dat"
    }
}
```
trojan-go的配置文件也有几点需要注意的地方

> 1. 80端口和23443端口要和Nginx开启的server对应上，如果Nginx只开了80端口，那么就把这里和fallback相关的两行配置删除掉
> 2. 配置中your_password需要替换为你自己的密码
> 3. 证书的目录和文件名要和第一步证书签发那里对应上
> 4. router是trojan-go的特有配置，和trojan不兼容，但是在服务端开启并不会影响你在客户端使用trojan的兼容性，如果不想在服务端开启也可以整体删除掉。

<br/>

​	完成上面所有步骤就意味着大功告成，我先来测试下，如果看到相同的回显信息，证明所有配置都已正确，trojan-go也正常启动了

`trojan-go -config ./config.json`

```
[INFO]  2020/10/12 12:13:42 trojan-go v0.8.2 initializing
```

<br/>

最后一步启动trojan-go，并加入到开机自启

```bash
systemctl start trojan-go.service 
systemctl enable trojan-go.service 
```

<br/><br/>

## 接下来

​	配置完服务端，你已经可以在手机上使用`V2rayNg`、`Igniter`等软件连接，亦或是在PC端使用`Qv2ray`、`V2rayA`进行连接。在openwrt上连接相对前面两个平台还是略微麻烦了一些，所以我准备在接下来的一篇文章里再把我配置的流程简单梳理一遍。

​	希望这篇文章能对看到的朋友有所帮助。


