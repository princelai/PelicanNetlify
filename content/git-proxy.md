Title: Git设置代理
Date: 2019-05-10 16:59
Category: 玩电脑
Tags: git, proxy, sock5, ssh
Slug: git-proxy
Authors: Kevin Chen



## 查看git连接方式

使用下面命令查看连接方式

```shell
$ git remote -v
origin  git@github.com:username/reponame.git (fetch)
origin  git@github.com:username/reponame.git (push)
```

像上面这种就是SSH方式





## http代理

如果你是使用http/https方式连接git那么就要用这种方式设置代理，

编辑用户目录下的`.gitconfig`文件，添加http代理信息

`vim ~/.gitconfig `

```ini
[http]
        proxy = socks5://IP:PORT
[https]
        proxy = socks5://IP:PORT
```

需要说明一点，据说git是不认https代理的，所以只需要添加http代理即可，但是加上也没有问题。





## sock5代理

如果是使用SSH方式连接git，那么就要通过设置SSH配置文件来达到目的

首先确定系统里有没有`nc`命令，如果没有的话要安装`openbsd-netcat`，这里注意不要安装`gnu-netcat`

```shell
yaourt -S openbsd-netcat
```



安装好后，编辑SSH配置文件`~/.ssh/config`（没有就新建一个）

`vim ~/.ssh/config`

```ini
Host github.com
    ProxyCommand nc -X 5 -x IP:PORT %h %p
```

配置好后，每次连接github的时候就会通过SSH走代理，如果你有国内的git托管服务，则不受影响。



## 参考

1. [git 设置和取消代理](<https://gist.github.com/laispace/666dd7b27e9116faece6>)

2. [HTTP tunneling](<https://wiki.archlinux.org/index.php/HTTP_tunneling>)