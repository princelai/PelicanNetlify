Title:
Date: 2018-07-24 12:30
Category: IT笔记, 金融笔记
Tags:
Slug:
Authors: Kevin Chen
Status: draft





```
curl https://getcaddy.com | bash -s personal
ulimit -n 8192
```



```
example.top {
    tls princelailai@gmail.com
    root /var/www/
    log /var/caddy/log
    timeouts none
    gzip

    proxy /h2ray localhost:10010 {
        header_upstream Host "example.top"
        header_upstream X-Forwarded-Proto "https"
    }
    
    proxy /wsray localhost:10086 {
        websocket
        header_upstream -Origin
    }
}
```



```
mkdir /etc/Caddy
nano /etc/Caddy/CaddyFile

systemctl stop v2ray@mKcp-server.service 
systemctl start v2ray@TCP-TLS-server.service   

mkdir /var/log/caddy/
caddy -conf /etc/Caddy/CaddyFile

nohup caddy -conf /etc/Caddy/CaddyFile &
systemctl stop v2ray@H2-TLS-server
systemctl start v2ray@H2-TLS-server
```

