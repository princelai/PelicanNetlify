Title: 在 LEDE/OpenWRT 上运行 V2ray
Date: 2018-07-12 11:16
Category: IT 笔记
Tags: lede,openwrt,v2ray
Slug: v2ray-run-in-lede
Authors: Kevin Chen
Status: draft

```
mkdir /var/log/v2ray/
nohup /usr/bin/v2ray/v2ray -config /etc/v2ray/LEDE-client.json &
nohup /usr/bin/v2ray/v2ray -config /etc/v2ray/LEDE-KCP-client.json &
/usr/bin/v2ray/update_iptables.sh

iptables -t nat -nvL V2RAY --line-numbers

/usr/bin/v2ray/gfwlist2dnsmasq.sh -d 8.8.8.8  -p 53 -o /tmp/gfwlist.overall
```

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

# 参考

[init.d](https://github.com/v2ray/v2ray-core/issues/101)

[利用 V2Ray + GFWList 实现路由器自动翻墙](https://cryptopunk.me/posts/27406/)

[网关服务器上设置 V2Ray+dnsmasq 透明代理](https://dakai.github.io/2017/11/27/v2ray.html)
