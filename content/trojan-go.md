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

mkdir /etc/trojan-go/

curl  https://get.acme.sh | sh
~/.acme.sh/acme.sh --issue -d domain --standalone -k ec-256
~/.acme.sh/acme.sh --installcert -d domain --fullchainpath /etc/trojan-go/tls.crt --keypath /etc/trojan-go/tls.key --ecc
chmod 664 /etc/trojan-go/tls*
```



## Nginx

```bash
apt-get install nginx-full
```



```bash
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
vim /etc/nginx/nginx.conf

touch /etc/nginx/sites-enabled/site.conf
vim /etc/nginx/sites-enabled/site.conf

# curl https://www.solarck.com/ -o /usr/share/nginx/html/index.html
curl https://www.solarck.com/ -o /var/www/html/index.html
curl https://www.solarck.com/404.html -o /var/www/html/404.html

systemctl start nginx.service
systemctl enable nginx.service

35 3 * * 2 curl https://www.solarck.com/ -o /var/www/html/index.html
```



## trojan-go

```
wget https://github.com/p4gefau1t/trojan-go/releases/download/v0.8.2/trojan-go-linux-amd64.zip

unzip trojan-go-linux-amd64.zip -d trojan-go

cd trojan-go

cp example/trojan-go.service example/trojan-go@.service /etc/systemd/system/

cp trojan-go /usr/bin/
cp trojan-go /usr/local/bin/
mkdir /usr/share/trojan-go/
cp geo* /usr/share/trojan-go/

cd /etc/trojan-go/
touch config.json
vim config.json
```

```
trojan-go -config ./config.json

[INFO]  2020/10/12 12:13:42 trojan-go v0.8.2 initializing
[WARN]  2020/10/12 12:13:42 empty tls fallback port

systemctl start trojan-go.service 
systemctl enable trojan-go.service 
```





## 启动

```

```



[acme](https://www.solarck.com/v2ray-quick-config.html)