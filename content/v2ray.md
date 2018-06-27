Title: V2ray
Date: 2018-06-26 13:08
Category: IT笔记
Tags:
Slug:
Authors: Kevin Chen
Status: draft



```
wget https://install.direct/go.sh
bash go.sh
```

`/etc/systemd/system/v2ray.service `,`/etc/v2ray/config.json `

`curl  https://get.acme.sh | sh   `

for standalone

`apt-get install -y socat netcat `

`~/.acme.sh/acme.sh --issue -d solarck.top --standalone -k ec-256`

renew

`~/.acme.sh/acme.sh --renew -d solarck.top --force --ecc`

`~/.acme.sh/acme.sh --installcert -d solarck.top --fullchainpath /etc/v2ray/v2ray.crt --keypath /etc/v2ray/v2ray.key --ecc`



# 配置文件

### 随机端口

#### **服务端**

```json
{
  "log": {
    "loglevel": "warning",
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log"
  },
  "inbound": {
    "port": 4433,
    "protocol": "vmess",
    "settings": {
      "clients": [
        {
          "id": "998c1fa3-962a-4682-a56d-ad262f7f184e",
          "alterId": 64,
          "security": "chacha20-poly1305"
        }
      ],
      "detour": {
        "to": "dynamicPort"
      }
    }
  },
  "inboundDetour": [
    {
      "protocol": "vmess",
      "port": "10000-20000",
      "tag": "dynamicPort",
      "settings": {
        "default": {
          "level": 1,
          "alterId": 32
        }
      },
      "allocate": {
        "strategy": "random",
        "concurrency": 3,
        "refresh": 5
      }
    }
  ],
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
            "0.0.0.0/8",
            "10.0.0.0/8",
            "100.64.0.0/10",
            "127.0.0.0/8",
            "169.254.0.0/16",
            "172.16.0.0/12",
            "172.168.0.0/16",
            "192.0.0.0/24",
            "192.0.2.0/24",
            "192.168.0.0/16",
            "198.18.0.0/15",
            "198.51.100.0/24",
            "203.0.113.0/24",
            "::1/128",
            "fc00::/7",
            "fe80::/10"
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
          "address": "solarck.top",
          "port": 4433,
          "users": [
            {
              "id": "998c1fa3-962a-4682-a56d-ad262f7f184e",
              "alterId": 64,
              "security": "chacha20-poly1305"
            }
          ]
        }
      ]
    },
    "mux": {
      "enabled": true
    }
  },
  "outboundDetour": [
    {
      "protocol": "freedom",
      "settings": {},
      "mux": {
        "enabled": true
      },
      "tag": "direct"
    }
  ],
  "routing": {
    "strategy": "rules",
    "settings": {
      "domainStrategy": "IPIfNonMatch",
      "rules": [
        {
          "type": "field",
          "ip": [
            "0.0.0.0/8",
            "10.0.0.0/8",
            "100.64.0.0/10",
            "127.0.0.0/8",
            "169.254.0.0/16",
            "172.16.0.0/12",
            "172.168.0.0/16",
            "192.0.0.0/24",
            "192.0.2.0/24",
            "192.168.0.0/16",
            "198.18.0.0/15",
            "198.51.100.0/24",
            "203.0.113.0/24",
            "::1/128",
            "fc00::/7",
            "fe80::/10"
          ],
          "outboundTag": "direct"
        },
        {
          "type": "chinasites",
          "outboundTag": "direct"
        },
        {
          "type": "chinaip",
          "outboundTag": "direct"
        }
      ]
    }
  }
}
```



### http2-TLS

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
          "id": "998c1fa3-962a-4682-a56d-ad262f7f184e",
          "alterId": 64,
          "security": "chacha20-poly1305"
        }
      ]
    },
    "streamSettings": {
      "network": "h2",
      "security": "tls",
      "httpSettings": {
        "path": "/ray"
      },
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
            "0.0.0.0/8",
            "10.0.0.0/8",
            "100.64.0.0/10",
            "127.0.0.0/8",
            "169.254.0.0/16",
            "172.16.0.0/12",
            "172.168.0.0/16",
            "192.0.0.0/24",
            "192.0.2.0/24",
            "192.168.0.0/16",
            "198.18.0.0/15",
            "198.51.100.0/24",
            "203.0.113.0/24",
            "::1/128",
            "fc00::/7",
            "fe80::/10"
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
    "listen": "127.0.0.1",
    "port": 1080,
    "protocol": "socks",
    "domainOverride": [
      "tls",
      "http"
    ],
    "settings": {
      "auth": "noauth",
      "udp": false
    }
  },
  "outbound": {
    "protocol": "vmess",
    "settings": {
      "vnext": [
        {
          "address": "solarck.top",
          "port": 443,
          "users": [
            {
              "id": "998c1fa3-962a-4682-a56d-ad262f7f184e",
              "alterId": 64,
              "security": "chacha20-poly1305"
            }
          ]
        }
      ]
    },
    "streamSettings": {
      "network": "h2",
      "security": "tls",
      "httpSettings": {
        "path": "/ray"
      }
    },
    "mux": {
      "enabled": true
    }
  },
  "outboundDetour": [
    {
      "protocol": "freedom",
      "settings": {},
      "mux": {
        "enabled": true
      },
      "tag": "direct"
    }
  ],
  "routing": {
    "strategy": "rules",
    "settings": {
      "domainStrategy": "IPIfNonMatch",
      "rules": [
        {
          "type": "field",
          "ip": [
            "0.0.0.0/8",
            "10.0.0.0/8",
            "100.64.0.0/10",
            "127.0.0.0/8",
            "169.254.0.0/16",
            "172.16.0.0/12",
            "172.168.0.0/16",
            "192.0.0.0/24",
            "192.0.2.0/24",
            "192.168.0.0/16",
            "198.18.0.0/15",
            "198.51.100.0/24",
            "203.0.113.0/24",
            "::1/128",
            "fc00::/7",
            "fe80::/10"
          ],
          "outboundTag": "direct"
        },
        {
          "type": "chinasites",
          "outboundTag": "direct"
        },
        {
          "type": "chinaip",
          "outboundTag": "direct"
        }
      ]
    }
  }
}
```



参考

[v2ray](https://toutyrater.github.io/advanced/tls.html)