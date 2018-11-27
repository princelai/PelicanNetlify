Title: Mongo常用命令记录
Date: 2018-11-20 10:53
Category: 玩电脑
Tags: mongo
Slug: my-frequency-mongo-command
Authors: Kevin Chen
Status: draft





`mongoexport -d db_mongo -c event -o /root/event.dat`

> 2018-11-20T10:54:00.806+0800    connected to: localhost
> 2018-11-20T10:54:00.811+0800    exported 24 records



`mongoimport -d db_mongo -c event --upsert -j 2 event.dat `

> 2018-11-20T11:14:42.313+0800    connected to: localhost
> 2018-11-20T11:14:42.620+0800    imported 24 documents



`tar -czf enevtimg.tar.gz -C /data/archives/ eventimg`



`tar -xf eventimg.tar.gz `







参考

1. [mongodb 备份、还原、导入、导出简单操作](https://segmentfault.com/a/1190000006236494)