Title: CentOS6 数据库服务器配置
Date: 2018-06-11 16:52
Category: IT 笔记
Tags: centos, ssh, linux
Slug: centos6-datebase-server
Authors: Kevin Chen

本文章仅用于记录在公司服务器上通过 yum repo 来安装官方提供的数据库程序，而非通过编译方式来安装。通过官方仓库来安装有很多好处，比如升级、打补丁都很方便，不用编译浪费时间，更不需要安装多个版本的 gcc 来满足各种不同软件的要求。

### Mysql

#### **下载安装 mysql repo**

`rpm -Uvh https://repo.mysql.com//mysql80-community-release-el6-1.noarch.rpm`

#### **升级至 57 版本**

`yum --disablerepo=mysql80-community --enablerepo=mysql57-community upgrade`

当前默认是 80 版本，如果未来需要升级，如果未来一直要维持在 57 版本，那么建议修改配置文件，以免每次都带上两个参数

`vim /etc/yum.repos.d/mysql-community.repo`

```ini
# Enable to use MySQL 5.7
[mysql57-community]
name=MySQL 5.7 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/6/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

[mysql80-community]
name=MySQL 8.0 Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/6/$basearch/
enabled=0
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
```

#### **安装 mysql-server**

`yum install mysql-community-server`

#### **开启服务**

`service mysqld start`

当然这时候还未配置 mysql，开启服务可能会失败。默认配置文件在`/etc/my.cnf`。

更多安装细节可以参照[mysql 官方指南](https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/)。

### Mongo

#### **创建 repo 文件**

`vim /etc/yum.repos.d/mongodb-org-3.6.repo`

```ini
[mongodb-org-3.6]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.6/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc
```

#### **安装 mongo 组件合集**

`yum install -y mongodb-org`

mongo-org 是一个合集，如果想精简安装各个组件，请参照下表。

| Package Name         | Description                                                                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mongodb-org`        | A metapackage that will automatically install the four component packages listed below.                                                           |
| `mongodb-org-server` | Contains the mongod daemon and associated configuration and init scripts.                                                                         |
| `mongodb-org-mongos` | Contains the mongos daemon.                                                                                                                       |
| `mongodb-org-shell`  | Contains the mongo shell.                                                                                                                         |
| `mongodb-org-tools`  | Contains the following MongoDB tools: mongoimport bsondump, mongodump, mongoexport, mongofiles, mongoperf, mongorestore, mongostat, and mongotop. |

#### **启动服务**

`mongod -f /etc/mongod.conf`

mongo 默认不加载 conf 文件，所以用 service 方法是无法正常启动的，暂时使用自带方法开启服务。

更多安装细节可以参照[mongo 官方指南](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/)。

###　 Nginx

#### **创建 repo 文件**

`vim /etc/yum.repos.d/nginx.repo`

```ini
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=0
enabled=1
```

#### **安装和开启服务**

```
yum install -y nginx
service nginx start
```

service 方法启动 nginx 默认会加载`/etc/nginx/nginx.conf`配置。

### 查看系统安装路径

使用仓库安装有一点不是很清晰，那就是安装目录并非自己指定，有时需要修改一些文件时找不到文件在哪里，我们可以通过如下方法找到软件的所有文件目录。

`rpm -qa |grep mongodb`

```
mongodb-org-mongos-3.6.5-1.el6.x86_64
mongodb-org-server-3.6.5-1.el6.x86_64
mongodb-org-tools-3.6.5-1.el6.x86_64
mongodb-org-3.6.5-1.el6.x86_64
mongodb-org-shell-3.6.5-1.el6.x86_64
```

例如我们要查看 server 的所有文件目录，则执行

`rpm -ql mongodb-org-server-3.6.5-1.el6.x86_64`

```
/etc/init.d/mongod
/etc/mongod.conf
/etc/sysconfig/mongod
/usr/bin/mongod
/usr/share/doc/mongodb-org-server-3.6.5
/usr/share/doc/mongodb-org-server-3.6.5/GNU-AGPL-3.0
/usr/share/doc/mongodb-org-server-3.6.5/MPL-2
/usr/share/doc/mongodb-org-server-3.6.5/README
/usr/share/doc/mongodb-org-server-3.6.5/THIRD-PARTY-NOTICES
/usr/share/man/man1/mongod.1
/var/lib/mongo
/var/log/mongodb
/var/log/mongodb/mongod.log
/var/run/mongodb
```

### SSH 免密登录服务器

Linux 上免密登录通常用 RSA 公钥和密钥实现，本地生成钥匙后，公钥上传至服务器，之后便可以免密登录了。

#### **本地生成公钥密钥**

`ssh-keygen -t rsa -b 4096`

默认公钥会存储在`~/.ssh/id_rsa.pub`，备用。

#### **修改服务器 sshd 配置**

`vim /etc/ssh/sshd_config`

```
PubkeyAuthentication yes #解开注释
AuthorizedKeysFile .ssh/authorized_keys #解开注释
```

#### **上传本地公钥至服务器**

`ssh-copy-id -i .ssh/id_rsa.pub -p port user@ip`

修改上面的端口、用户名和 ip，再在本地`.bashrc`或`.zshrc`新建一条 alias 就可以非常方便快捷的登录了。
