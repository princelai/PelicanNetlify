Title: V2ray
Date: 2018-06-26 13:08
Category: IT笔记
Tags: v2ray,acme
Slug:
Authors: Kevin Chen
Status: draft



# 服务器端配置

### 优化网络

主要涉及bbr的安装配置，需要VPS是KVM架构可以参照[之前的文章](https://www.solarck.com/shadowsocks-libev.html)。

### 安装V2ray

```
wget https://install.direct/go.sh
bash go.sh
```

`/etc/systemd/system/v2ray.service `,`/etc/v2ray/config.json `

### TLS域名证书

在这部之前，你需要一个域名，免费的也无所谓。



#### *安装acme*

`apt-get install -y socat netcat `

```bash
curl  https://get.acme.sh | sh
```



#### *签发证书*

我使用的是ecc证书，需要把domain换成自己的域名

```
~/.acme.sh/acme.sh --issue -d domain --standalone -k ec-256
```



#### *安装证书*

证书会被安装到`/etc/v2ray`下

```
~/.acme.sh/acme.sh --installcert -d domain --fullchainpath /etc/v2ray/v2ray.crt --keypath /etc/v2ray/v2ray.key --ecc
```



#### *证书续期*

`~/.acme.sh/acme.sh --renew -d domain --force --ecc`



`/etc/init.d/v2ray`

```bash
#!/bin/sh
#
# v2ray        Startup script for v2ray
#
# chkconfig: - 24 76
# processname: v2ray
# pidfile: /var/run/v2ray.pid
# description: V2Ray proxy services
#

### BEGIN INIT INFO
# Provides:          v2ray
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: V2Ray proxy services
# Description:       V2Ray proxy services
### END INIT INFO

DESC=v2ray
NAME=v2ray
DAEMON=/usr/bin/v2ray/v2ray
PIDFILE=/var/run/$NAME.pid
LOCKFILE=/var/lock/subsys/$NAME
SCRIPTNAME=/etc/init.d/$NAME
RETVAL=0

DAEMON_OPTS="-config /etc/v2ray/config.json"

# Exit if the package is not installed
[ -x $DAEMON ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Source function library.
. /etc/rc.d/init.d/functions

start() {
  local pids=$(pgrep -f $DAEMON)
  if [ -n "$pids" ]; then
    echo "$NAME (pid $pids) is already running"
    RETVAL=0
    return 0
  fi

  echo -n $"Starting $NAME: "

  mkdir -p /var/log/v2ray
  $DAEMON $DAEMON_OPTS 1>/dev/null 2>&1 &
  echo $! > $PIDFILE

  sleep 2
  pgrep -f $DAEMON >/dev/null 2>&1
  RETVAL=$?
  if [ $RETVAL -eq 0 ]; then
    success; echo
    touch $LOCKFILE
  else
    failure; echo
  fi
  return $RETVAL
}

stop() {
  local pids=$(pgrep -f $DAEMON)
  if [ -z "$pids" ]; then
    echo "$NAME is not running"
    RETVAL=0
    return 0
  fi

  echo -n $"Stopping $NAME: "
  killproc -p ${PIDFILE} ${NAME}
  RETVAL=$?
  echo
  [ $RETVAL = 0 ] && rm -f ${LOCKFILE} ${PIDFILE}
}

reload() {
  echo -n $"Reloading $NAME: "
  killproc -p ${PIDFILE} ${NAME} -HUP
  RETVAL=$?
  echo
}

rh_status() {
  status -p ${PIDFILE} ${DAEMON}
}

# See how we were called.
case "$1" in
  start)
    rh_status >/dev/null 2>&1 && exit 0
    start
    ;;
  stop)
    stop
    ;;
  status)
    rh_status
    RETVAL=$?
    ;;
  restart)
    stop
    start
    ;;
  reload)
    reload
  ;;
  *)
    echo "Usage: $SCRIPTNAME {start|stop|status|reload|restart}" >&2
    RETVAL=2
  ;;
esac
exit $RETVAL
```



# 本地配置



# 配置文件



### http2-TLS

#### **服务端**

```json

```



#### **客户端**

```json

```



# 参考

[v2ray](https://toutyrater.github.io/advanced/tls.html)

[init.d](https://github.com/v2ray/v2ray-core/issues/101)