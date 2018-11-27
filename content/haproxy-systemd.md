Title: 解决 Haproxy 用 Systemd 启动失败的问题
Date: 2018-07-13 12:35
Category: 玩电脑
Tags: haproxy, systemd
Slug: systemd-wait-network-online
Authors: Kevin Chen

# 问题描述

配置好 Haproxy 的配置文件，手动可以无错误开启，但是`Systemctl enable haproxy.service`开机启动每次都报错，系统启动后，手动开启还是没有问题。

# 分析原因

### haproxy 配置问题

`/etc/haproxy.cfg`是配置文件，因为手动指定配合文件可以启动，而且测试配置文件也没有报错或警报，所以首先排除是配置的问题。

### systemd 服务配置问题

`haproxy.service`是 systemd 用来启动服务的配置文件，第一眼看配置后，以为是创建 PID 没有权限，增加`User=root`字段，但是重启后依然报错。原版配置只有`After=network.target`，手动添加`Wants=network.target`重启后，依然报错。

### 查看日志

正要灰心的时候，决定最后一搏，查看 systemd 启动日志，看看能不能找到点线索。

查看最近一次启动中 haproxy 的日志

`journalctl -b -0 -u haproxy`

```bash
Jul 13 10:32:20 kevin-pc systemd[1]: haproxy.service: Main process exited, code=exited, status=1/FAILURE
Jul 13 10:32:20 kevin-pc systemd[1]: haproxy.service: Failed with result 'exit-code'.
Jul 13 10:32:20 kevin-pc systemd[1]: Failed to start HAProxy Load Balancer.
Jul 13 10:32:20 kevin-pc systemd[1]: haproxy.service: Service RestartSec=100ms expired, scheduling restart.
Jul 13 10:32:20 kevin-pc systemd[1]: haproxy.service: Scheduled restart job, restart counter is at 1.
Jul 13 10:32:20 kevin-pc systemd[1]: Stopped HAProxy Load Balancer.
Jul 13 10:32:20 kevin-pc systemd[1]: Starting HAProxy Load Balancer...
Jul 13 10:32:20 kevin-pc haproxy[554]: [ALERT] 193/103220 (554) : parsing [/etc/haproxy/haproxy.cfg:36] : 'server server1' : could not resolve address 'xxxx.com'.
Jul 13 10:32:20 kevin-pc haproxy[554]: [ALERT] 193/103220 (554) : parsing [/etc/haproxy/haproxy.cfg:37] : 'server server2' : could not resolve address 'xxxx.com'.
Jul 13 10:32:20 kevin-pc haproxy[554]: [ALERT] 193/103220 (554) : parsing [/etc/haproxy/haproxy.cfg:38] : 'server server3' : could not resolve address 'xxxx.com'.
```

原因找到了，原来是我在 haproxy 配置文件的 backend 段中，使用了域名而不是 IP，导致解析失败。但是明明我已经指定了 haproxy 的启动在 network 之后了，为什么还是会这个样子呢？

答案只能从 network 的服务中找

`journalctl -b -0 -u NetworkManager`

```bash
Jul 13 10:32:22 kevin-pc NetworkManager[493]: <info>  [1531449142.2279] dhcp4 (enp0s25): activation: beginning transaction (timeout in 45 seconds)
Jul 13 10:32:22 kevin-pc NetworkManager[493]: <info>  [1531449142.2566] dhcp4 (enp0s25):   address 172.168.201.33
Jul 13 10:32:22 kevin-pc NetworkManager[493]: <info>  [1531449142.2566] dhcp4 (enp0s25):   plen 24
Jul 13 10:32:22 kevin-pc NetworkManager[493]: <info>  [1531449142.2566] dhcp4 (enp0s25):   expires in 86400 seconds
Jul 13 10:32:22 kevin-pc NetworkManager[493]: <info>  [1531449142.2567] dhcp4 (enp0s25):   nameserver '172.168.13.100'
Jul 13 10:32:22 kevin-pc NetworkManager[493]: <info>  [1531449142.2567] dhcp4 (enp0s25):   nameserver '202.106.0.20'
Jul 13 10:32:22 kevin-pc NetworkManager[493]: <info>  [1531449142.2567] dhcp4 (enp0s25):   gateway 172.168.201.1
```

对比两段日志的时间，原来虽然 haproxy 启动在 network 之后，但是 network 刚刚启动 haproxy 就开始启动，而 network 的启动内容比较多，还有很多网络通信，可能完全启动完需要一点时间。haproxy 的启动时间比 dhcp 启动要早了 2 秒，这时无法进行 DNS 解析，所以就会造成启动失败，之前的所有问题也都说的通了。

# 解决方法

知道了问题的原因，那么就要解决它。只要让 haproxy 在 network 完全启动后再启动，就应该可以正常启动了。那么如何做呢？

首先要替换`haproxy.service`中的`After`和`Wants`字段，用`network-online.target`替换`network.target`

```ini
After=network-online.target
Wants=network-online.target
```

然后启动一个自带的网络等待服务

```bash
sudo systemctl enable NetworkManager-wait-online.service
```

如果你是使用`systemd-network`来管理网络服务，那么需要启动另外一个服务

```bash
sudo systemctl enable systemd-networkd-wait-online.service
```

重启后，一切问题都解决了。

# 参考

[Running Services After the Network is up](https://www.freedesktop.org/wiki/Software/systemd/NetworkTarget/)
