Title: Mongo常用命令记录
Date: 2018-12-06 11:53
Category: 玩电脑
Tags: mongo
Slug: my-frequency-mongo-command
Authors: Kevin Chen





## 导出

```bash
mongoexport -d db_mongo -c news -f title,date,contents,rawtag -o ~/news.json
```

导出使用mongo自带的`mongoexport`命令，参数解释如下：

> `-d`：数据库名称
>
> `-c`：集合名称
>
> `-f`：字段名，不指定则为全部
>
> `-o`：输出文件





## 导入

导出通常是在服务器上的操作，然后scp到本地，如果文件过大，首先要压缩一下

```bash
tar -czf news.tar.gz -C /home/kevin news.json
```

> `-c`：创建压缩文件
>
> `-z`：使用gzip压缩
>
> `-f`：使用文件归档
>
> `-C`：指定文件目录

通常创建压缩文件`-cf`或`-czf`是固定搭配。解压缩就不多说了，通常使用`-xf`参数就可以。



```bash
mongoimport -d db_mongo -c news --upsert -j 2 news.json
```

> `--upsert`：插入，如果内容存在则更新
>
> `-j`：指定并发数，如果文件过大，使用单线程容易卡死失败





## 去重

#### 方法一

1. 首先查看计数并删除集合

    `db.news.count()`

    > 13136

    `db.news.drop()`

    > true



2. 创建唯一索引

   `db.news.createIndex({title:1},{unique:true})`

   > {
   > ​        "createdCollectionAutomatically" : true,
   > ​        "numIndexesBefore" : 1,
   > ​        "numIndexesAfter" : 2,
   > ​        "ok" : 1
   > }

3. 导入

   还是按照上面的导入方法正常导入，完成后查看内容数量

   `db.news.count()`
   
   > 12552


#### 方法二

这个方法是从网上看到的，同样能得到预期的结果，具体的解释可以从参考链接跳转过去看

```
db.news.aggregate([
    {
        $group:{_id:{title:'$title'},count:{$sum:1},dups:{$addToSet:'$_id'}}
    },
    {
        $match:{count:{$gt:1}}
    }

    ]).forEach(function(it){

         it.dups.shift();
            db.Passages.remove({_id: {$in: it.dups}});

    });
```





## 正则表达式和排序

因为这两个命令都很简单，把这两个组合为一条命令

```mongo
db.news.find({title:{$regex:/p2p/i}},{title:1,date:1,_id:0}).sort({date:-1}).limit(10).pretty()
```

上面的查找命令的含义为：找出标题中含有P2P（不区分大小写）的文章，只展示标题和日期，按照日期降序排列，最后输出10条并格式化显示。





## 参考

1.  [mongodb 备份、还原、导入、导出简单操作](https://segmentfault.com/a/1190000006236494)
2. [mongoDB删除重复的数据 去重](https://www.jianshu.com/p/7685e6692ed6)