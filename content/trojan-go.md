Title: trojan-go服务端部署
Date: 2020-10-12 11:18
Category: 玩电脑
Tags:
Slug: trojan-go-server
Authors: Kevin Chen
Status: draft



## acme.sh

```bash
apt-get update
apt-get install socat

curl  https://get.acme.sh | sh
```



## Nginx

```bash
apt-get install nginx-full
```



```bash
# curl https://www.solarck.com/ -o /usr/share/nginx/html/index.html
curl https://www.solarck.com/ -o /var/www/html/index.html
curl https://www.solarck.com/404.html -o /var/www/html/404.html
```



## trojan-go

1

[acme](https://www.solarck.com/v2ray-quick-config.html)