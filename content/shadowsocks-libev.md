Title: VPS 搭梯子指南——shadowsocks+BBR+obfs
Date: 2017-11-13 15:55
Modified: 2018-06-05 13:01
Category: 玩电脑
Tags: shadowsocks
Authors: Kevin Chen
Slug: shadowsocks-libev

近期开会导致墙越来越高，迫不得已升级自建的 ss 服务，由于 shadowsocks 原版已经停更，shadowsocksR 也已经删库，所以就锁定 libev 版本。
**_注：以下服务器端内容请切换到 root 操作_**

### 1. 升级 Debian

在升级之前，我需要先把服务器从 Debian 8 升级到 Debian 9，如果不是 Debian 用户，或者不想升级的可以跳过，这一步不影响后续操作，但是部分代码可能需要修改。

首先要把 Debian 8 升级到最新版本

```bash
apt update
apt upgrade
```

备份源列表

```bash
cp /etc/apt/sources.list /etc/apt/sources.list-jessie
```

修改源列表，把 jessie 替换为 stretch

```bash
vim /etc/apt/sources.list
:s/jessie/stretch/g
```

再次更新升级

```bash
 apt update
 apt upgrade
 apt dist-upgrade
 apt autoremove
```

### 2. 开启 BBR

使用一键脚本安装并开启 bbr，此步除 OpenVZ 以外的服务器都可以开启，跳过不影响后续内容。

```
wget --no-check-certificate https://raw.githubusercontent.com/princelai/across/master/bbr.sh
chmod +x bbr.sh
./bbr.sh
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p
lsmod | grep bbr
```

### 3. 安装 shadowsocks-libev 和 simple-obfs 混淆

需要从 stretch-backports 库中安装，非 Debian 9 用户请参考[文档][1]

```bash
sh -c 'printf "deb http://deb.debian.org/debian stretch-backports main" > /etc/apt/sources.list.d/stretch-backports.list'
apt update
apt -t stretch-backports install shadowsocks-libev simple-obfs
```

### 4. 优化 TCP 网络

编辑 sysctl 文件，把下面的内容复制过去，
如果第二步中没有开启 bbr，那么请删除前两行。

`vim /etc/sysctl.conf`

```ini
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_fastopen = 3
fs.file-max = 1024000
net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.rmem_default = 65536
net.core.wmem_default = 65536
net.core.netdev_max_backlog = 4096
net.core.somaxconn = 4096
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.ip_local_port_range = 10000 65000
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_mtu_probing = 1
net.ipv4.ip_forward = 1
```

更改保存后执行

```
sysctl -p
```

### 5. 配置服务端

**修改配置**

编辑配置文件，填上自己的密码，端口建议使用 443，别的端口封杀的太严重。
关于加密方式，现在新版都支持 AEAD 加密方式，详细内容请点[这里][2]。

`vim /etc/shadowsocks-libev/config.json`

```json
{
  "server": "0.0.0.0",
  "server_port": 443,
  "local_port": 1080,
  "password": "",
  "timeout": 100,
  "method": "chacha20-ietf-poly1305",
  "mode": "tcp_and_udp",
  "fast_open": true,
  "plugin": "obfs-server",
  "plugin_opts": "obfs=tls"
}
```

**启动服务器端服务**

如果已经按照上面编辑好配置文件，那么就可以直接用文件模式启动服务。

```bash
ss-server -c config.json #测试模式
systemctl start shadowsocks-libev #后台启动
systemctl enable shadowsocks-libev #开机启动
```

### 6. 配置客户端

**Windows**

下载[shadowsocks-windows][3]解压缩，
下载[simple-obfs][4]中的 obfs-local.exe 和 msys-2.0.dll 放到 shadowsocks-windows 目录中,obfs-host 随意写一个中国可以访问的网站。
![shadowsocks-windows](http://kevinstuchuang.qiniudn.com/blog-pic/shadowsocks-windows.png)

**Linux**

安装客户端和 obfs

```bash
sudo pacman -Syu
sudo pacman -S shadowsocks-libev simple-obfs
```

开启本地服务

```
nohup ss-local -c config.json --plugin obfs-local --plugin-opts "obfs=tls;obfs-host=cn.bing.com"
```

开机启动，编辑启动文件 ，添加 obfs 混淆

`vim /usr/lib/systemd/system/shadowsocks-libev@.service`

```ini
[Unit]
Description=Shadowsocks-Libev Client Service
After=network.target

[Service]
Type=simple
User=nobody
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
ExecStart=/usr/bin/ss-local -c /etc/shadowsocks/%i.json --plugin obfs-local --plugin-opts "obfs=tls;obfs-host=cn.bing.com"

[Install]
WantedBy=multi-user.target
```

编辑配置文件
`vim /etc/shadowsocks/libev.json`

```json
{
  "server": "你的服务器IP",
  "server_port": 443,
  "local_address": "127.0.0.1",
  "local_port": 65509,
  "password": "你的密码",
  "timeout": 300,
  "method": "chacha20-ietf-poly1305",
  "fast_open": true,
  "workers": 1,
  "prefer_ipv6": false
}
```

开启服务，@后面要和 json 文件同名

```bash
sudo systemctl start shadowsocks-libev@libev
sudo systemctl enable  shadowsocks-libev@libev
```

其他内容请参考[Archlinux Wiki][5]
shadowsocks-qt5 目前功能严重缺失，不建议使用，Linux 平台最好是命令行模式

[SwitchyOmega][6]是目前 Chome 最好的代理插件，可以在[官网][7]下载最新版本安装。

### 7.Android 客户端配置

如果 Android 手机可以访问 Google Play，则可以直接在上面搜 shadowsocks 和 obfs 分别安装后再配置即可。

如果当前手机不能访问 Play，可以在 github releases 上分别下载[shadowsocks-android][8]和[simple-obfs-android][9]，安装后再配置自己的服务端信息。

### 8.socks5 转 http/https

实际使用中，经常会遇到命令行终端或本地程序需要代理，但是他们只支持 http 或 https 协议，所以就需要把 socks5 协议的代理转换协议，以 Archlinux 为例，方法也很简单。

安装 privoxy

```bash
sudo pacman -S privoxy
```

修改配置，找到如下两行打开注释，注意 listen 后的端口是未来我们要使用的端口，默认为 8118，forward 后的端口是 shadowsocks 使用的本地端口，这个依据自己的配置修改，不要忘了最后的"."。
`sudo vim /etc/privoxy/config`

```bash
listen-address  127.0.0.1:8118
forward-socks5t   /   127.0.0.1:65509 .
```

保存配置后，启动或重启服务

```bash
sudo systemctl start privoxy
sudo systemctl restart privoxy
```

以后需要使用时，修改两个本地变量即可

```bash
echo https_proxy=127.0.0.1:8118
echo http_proxy=127.0.0.1:8118
```

### 9. 服务器端常用的命令

```bash
#测试ss+obfs是否正常启动
ss-server -c config.json --plugin obfs-server --plugin-opts "obfs=http"
#查看obfs的进程编号
ps ax|grep obfs
#查看ss的进程编号
ps ax|grep ss-server
#查看ss监听端口
netstat -nlp |grep ss-server
```

[1]: https://github.com/shadowsocks/shadowsocks-libev#pre-build-configure-guide
[2]: https://shadowsocks.org/en/spec/AEAD-Ciphers.html
[3]: https://github.com/shadowsocks/shadowsocks-windows/releases
[4]: https://github.com/imgk/simple-obfs-Cygwin/releases
[5]: https://wiki.archlinux.org/index.php/Shadowsocks_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#.E5.91.BD.E4.BB.A4.E8.A1.8C
[6]: https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=zh-CN
[7]: https://www.switchyomega.com/download.html
[8]: https://github.com/shadowsocks/shadowsocks-android/releases
[9]: https://github.com/shadowsocks/simple-obfs-android/releases
