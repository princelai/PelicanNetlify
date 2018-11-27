Title: 快速配置V2ray
Date: 2018-07-13 10:08
Category: 玩电脑
Tags: v2ray,acme.sh,tls
Slug: v2ray-quick-config
Authors: Kevin Chen

# 服务器端配置

服务器系统使用的是Debian 9 x86_64，Ubuntu大部分操作都通用。如果是CentOS的话，该文章仅作为参考。

### 优化网络

主要涉及bbr的安装配置，需要VPS是KVM架构，具体可以参照[之前的文章](https://www.solarck.com/shadowsocks-libev.html)。

### 安装V2ray

官方提供了安装脚本，需要系统使用systemd管理系统

```bash
wget https://install.direct/go.sh
bash go.sh
```

安装好后，主要文件如下：

> `/etc/systemd/system/v2ray.service`：启动服务
>
> `/etc/v2ray/config.json`：配置文件
>
> `/usr/bin/v2ray/v2ray`：主程序

### TLS域名证书

因为最终配置要用到TLS链接，在这步之前，你需要一个域名，免费的也无所谓。

工具使用[acme.sh](https://github.com/Neilpang/acme.sh/wiki)，这是用来签发[Let's Encrypt](https://letsencrypt.org/)免费证书的脚本，非常好用。

#### _安装acme_

安装依赖工具

`apt-get install -y socat netcat`

安装acme.sh脚本

```bash
curl  https://get.acme.sh | sh
```

默认是安装在`～/.acme.sh/`

#### _签发证书_

我使用的是ecc证书，需要把domain换成自己的域名

```bash
~/.acme.sh/acme.sh --issue -d domain --standalone -k ec-256
```

#### _安装证书_

证书会被安装到`/etc/v2ray`目录下

```bash
~/.acme.sh/acme.sh --installcert -d domain --fullchainpath /etc/v2ray/v2ray.crt --keypath /etc/v2ray/v2ray.key --ecc
```

#### _证书续期_

执行完签发命令后，系统已经加上了crond自动签发，如果你想手动签发，可以执行下面的命令。

```bash
~/.acme.sh/acme.sh --renew -d domain --force --ecc
```

# 本地配置

### 安装

因为我使用的是Manjaro，一个基于Archlinux的Linux版本，所有安装只要一条命令

```bash
yaourt -Sy v2ray
```

如果你用的是其他系统，可以参考服务器的安装脚本。

# 配置文件

### 配置说明

我当前使用的连接方式是TCP+TLS这种，根据官方和网上收集的信息，据说当前最好的配置是WebSocket+WEB+TLS+CDN，我没有选择这种连接方式有以下几点原因：

1.  Websocket效率低于TCP
2.  多层转发导致速度可能会变慢
3.  配置较麻烦

如果你的ISP没有QOS，没有TCP阻断，你连接服务器的流量没有很大的话，是没有必要折腾这种连接方式的。当然我在写这篇文章之前还使用过H2+TLS的连接方式，但是不知是服务器没有加Caddy转发还是H2方式不稳定，断流严重，换成TCP+TLS后，连接稳定，速度尚可，未出现断流。

每个人每个地区的ISP情况不尽相同，所以多试才能找到最适合你的配置，更多配置可以参考[配置模板](https://github.com/KiriKira/vTemplate)。

### TCP+TLS配置

#### **配置说明**

我有三台性能较弱的VPS，所以三台分别安装并部署了服务端的配置，而在本地客户端的outbound中连接三个服务器，v2ray可以进行简单的轮寻进行负载均衡。

为了简化操作，UUID设置为相同，当然不嫌麻烦的话可以设置为不同，但要和每台服务器的UUID相对应。

因为我认为vmess协议加密已经足够强壮，所以每台就没有再设置内容加密，如果不放心，可以使用auto或者AEAD方式加密。另外根据官方的测试，貌似`aes-256-gcm` 和`chacha20-ietf-poly1305`两种加密方式传输效率比不加密的效率还要高，可能与硬件加密有关系吧。

所有配置的详细内容都可以在官方文档或白话文教程里找到，其实配置v2ray并没有那么复杂。

最后贴上我的自用配置，生成UUID可以使用[UUID Generator](https://www.uuidgenerator.net/)这个网站，或者Linux用户可以使用下面命令`cat /proc/sys/kernel/random/uuid`生成。

#### **服务端**

```json
{
  "log": {
    "loglevel": "warning",
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log"
  },
  "inbound": {
    "port": 443,
    "protocol": "vmess",
    "settings": {
      "clients": [
        {
          "id": "xxxxxxxxx-xxxxxxxxxxx-xxxxxx",
          "alterId": 32,
          "security": "none",
          "udp": true
        }
      ]
    },
    "streamSettings": {
      "network": "tcp",
      "security": "tls",
      "tlsSettings": {
        "certificates": [
          {
            "certificateFile": "/etc/v2ray/v2ray.crt",
            "keyFile": "/etc/v2ray/v2ray.key"
          }
        ]
      }
    }
  },
  "outbound": {
    "protocol": "freedom",
    "settings": {}
  },
  "outboundDetour": [
    {
      "protocol": "blackhole",
      "settings": {},
      "tag": "blocked"
    }
  ],
  "routing": {
    "strategy": "rules",
    "settings": {
      "rules": [
        {
          "type": "field",
          "ip": [
            "geoip:private"
          ],
          "outboundTag": "blocked"
        }
      ]
    }
  }
}
```

#### **客户端**

```json
{
  "log": {
    "loglevel": "warning",
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log"
  },
  "inbound": {
    "port": 1080,
    "protocol": "socks",
    "domainOverride": [
      "tls",
      "http"
    ],
    "settings": {
      "auth": "noauth",
      "udp": true
    }
  },
  "outbound": {
    "protocol": "vmess",
    "settings": {
      "vnext": [
      {
          "address": "domain.com",
          "port": 443,
          "users": [
            {
              "id": "xxxxxxxxx-xxxxxxxxxxx-xxxxxx",
              "alterId": 32,
              "security": "none"
            }
          ]
        },
      {
          "address": "domain.com",
          "port": 443,
          "users": [
            {
              "id": "xxxxxxxxx-xxxxxxxxxxx-xxxxxx",
              "alterId": 32,
              "security": "none"
            }
          ]
        },
      {
          "address": "domain.com",
          "port": 443,
          "users": [
            {
              "id": "xxxxxxxxx-xxxxxxxxxxx-xxxxxx",
              "alterId": 32,
              "security": "none"
            }
          ]
        }
      ]
    },
    "streamSettings": {
      "network": "tcp",
      "security": "tls"
    }
  },
  "outboundDetour": [
    {
      "protocol": "freedom",
      "settings": {},
      "tag": "direct"
    }
  ],
  "dns": {
    "servers": [
      "101.6.6.6",
      "101.132.183.99",
      "193.112.15.186",
      "8.8.8.8"
    ]
  },
  "routing": {
    "strategy": "rules",
    "settings": {
      "domainStrategy": "IPIfNonMatch",
      "rules": [
        {
         "type": "field",
         "port": 53,
         "network": "udp",
         "outboundTag": "direct"
        },
        {
          "type": "field",
          "ip": [
            "geoip:cn",
            "geoip:private",
            "172.168.0.0/16"
          ],
          "port": "0-10000",
          "network": "tcp,udp",
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "domain": [
            "geosite:cn"
          ],
          "port": "0-10000",
          "network": "tcp,udp",
          "outboundTag": "direct"
        }
      ]
    }
  }
}
```

# 参考

[v2ray官方文档](https://www.v2ray.com/)

[v2ray白话文教程](https://toutyrater.github.io)

[acme.sh wiki](https://github.com/Neilpang/acme.sh/wiki)
