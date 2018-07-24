Title: git 和 github 主要使用方法
Date: 2018-05-25 17:19
Category: IT 笔记
Tags: git, github
Slug: git-and-github
Authors: Kevin Chen

### ssh 和密钥

`ssh-keygen -t rsa -b 4096 -C "princelailai@gmail.com"`：生成密钥

`cat ~/.ssh/id_rsa.pub`：查看密钥

`ssh -T git@github.com`：测试密钥是否可以正常登录

### 设置

`git config --list`：列出当前 repo 所有设置

`git config --global user.name "princelai"`：设置用户名

`git config --global user.email "princelailai@gmail.com"`：设置 E-mail

`echo "# mydotfiles" > README.md`：

### 基本操作

`git init`：初始化，创建.git 文件夹

`git status`：查看当前工作区/缓存区状态

### 添加和提交

`git add <文件>`：添加文件至缓存区

`git commit -m "说明"`：从缓存区提交至仓库

`git commit -am "说明"`：前面两种的合并版

`git commit --amend "说明"`：替换掉上一次的提交

### 删除文件

`git rm <文件>`：从 repo 中删除文件

`git rm --cached <文件>`：

### 恢复

`git checkout -- <文件>`：撤销文件工作区的修改

`git reset HEAD <文件>`：撤销文件暂存区的修改，放回工作区

`git reset --hard ad93b89`：所有文件退回至指定版本

### 版本和日志

`git log --oneline`:简版 log

`git log --graph`：带合并图形版 log

### 远程仓库

`git remote show origin`：查看远程仓库详情

`git clone git-url`：从远程仓库克隆至本地

`git remote add origin git-url`：关联远程和本地仓库

### 远程仓库的提交和拉取

`git pull origin master`：把远程仓库拉取到本地仓库

`git push origin master`：本地仓库推送至远程仓库，-u 用于第一次关联

### 分支

`git branch`：列出本地分支

`git branch -r`：列出远程分支

`git branch -a`：列出所有分支

`git branch <分支>`：创建分支

`git branch -d <分支>`：删除分支

`git branch --set-upstream-to=origin/分支 分支`：本地和远程分支关联

### checkout

`git checkout 分支`：切换到指定分支

`git checkout -b 分支`：创建并切换到分支

### 合并

`git merge 分支`：把指定分支合并到当前分支

`git merge --no-ff -m "说明" 分支`：禁止 Fast forward 模式，创建新的 commit

### 参考

1.  [简书](https://www.jianshu.com/p/e4e29c9c3bd9)
2.  [廖雪峰](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
3.  [阮一峰](http://www.ruanyifeng.com/blog/2014/06/git_remote.html)
