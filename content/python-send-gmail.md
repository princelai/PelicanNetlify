Title: 使用 Python 发送 Gmail
Date: 2018-06-11 14:20
Category: IT 笔记
Tags: python, gmail
Slug: python-send-gmail
Authors: Kevin Chen

本文基于一个真实的项目，使用 python3.6 和最新官方 smtplib 接口。项目的目的是爬取网站，然后通过邮件给自己发送邮件提醒新文章。最后使用 linux 系统的 crond 服务定时执行。

### 发邮件方法

在定义发邮件方法之前，我们还定义了一个类和类中的爬虫，单拿出来发邮件来说，代码如下：

```python
    def sent_email(self):
        fromaddr = 'princelailai@gmail.com'
        toaddrs  = ['princelailai@gmail.com']
        subject = "{}{}".format(datetime.now().strftime('%Y年%m月%d日'),'共有产权房信息')
        msg = ''.join(['日期:\t{}\n标题:\t{}\n地址:\t{}\n\n'.format(v[0],v[1],k) for k,v in self.result.items()])
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header(fromaddr, 'utf-8')
        message['To'] =  Header(','.join(toaddrs), 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        #message = f"From: {fromaddr}\nTo: {','.join(toaddrs)}\nSubject: {subject}\n\n{msg}"
        username = 'princelailai@gmail.com'
        password = 'app password'
        try:
            server = smtplib.SMTP('smtp.gmail.com','587')
            server.ehlo()
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, message.as_string())
            server.quit()
            logging.info('Send Email Successful.')
        except:
            logging.info('Send Email Failed.')
```

需要注意的有几点：

1.  邮件正文需要是 MIMEText 格式的
2.  发信人、收信人、主题要用 Header 添加
3.  如果你的 Google 账号开启了两步验证，那么你的邮箱密码就不是登录密码，而是 app 密码，关于 app 密码怎么生成可以查看这篇文章[Sign in using App Passwords](https://support.google.com/accounts/answer/185833#generate)
4.  其他关于 smtp 地址和端口的问题，可以查看这篇文章[Use IMAP to check Gmail on other email clients](https://support.google.com/mail/answer/7126229?visit_id=1-636642850165284125-2014875658&hl=en&rd=1)

### 定时启动

创建一个文本文件，用于创建单一用户的 crond 文件

```bash
0 6 */3 * * /root/miniconda3/bin/python /root/monitor_house_info/monitor_house_info.py
```

关于 crond 配置，网上教程很多，或者`man 5 crontab`就可以看到详细的用法。

最后输入`crontab file`导入文件，就可以坐等收邮件了。

### 全部代码

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from requests_html import HTMLSession
import smtplib
import os
import json
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class monitor_house_info:

    def __init__(self):
        self.realpath = os.path.split(os.path.realpath(__file__))[0]
        self.realdb = os.path.join(self.realpath,'db.json')
        self.result = {}
        self.url = ['http://cpzjw.bjchp.gov.cn/cpzjw/336693/index.html',
                    'http://cpzjw.bjchp.gov.cn/cpzjw/336551/336554/index.html']

    def read_json(self):
        if not os.path.exists(self.realdb):
            self.db = {}
        else:
            with open(self.realdb) as f:
                self.db = json.loads(f.read())
        logging.info('Readed json db.')

    def get_news(self,url):
        session = HTMLSession()
        resp = session.get(url)
        element_date = resp.html.find('div.easysite-article-content > ul > li > span.date04')
        date = [i.text[1:-1] for i in element_date]
        element_content = resp.html.find('div.easysite-article-content > ul > li > span.title04')
        content = [i.text.strip() for i in element_content]
        link = [list(i.absolute_links)[0] for i in element_content]
        for l,d,c in zip(link,date,content):
            self.result[l] = [d,c]
        logging.info('geted web content.')

    def valid_news(self):
        for k in self.result.keys():
            if k in self.db:
                self.result.pop(k)
        with open(self.realdb,'w') as fp:
            self.db.update(self.result)
            fp.write(json.dumps(self.db,ensure_ascii=False))
        logging.info('valided news.')


    def sent_email(self):
        fromaddr = 'princelailai@gmail.com'
        toaddrs  = ['princelailai@gmail.com']
        subject = "{}{}".format(datetime.now().strftime('%Y年%m月%d日'),'共有产权房信息')
        msg = ''.join(['日期:\t{}\n标题:\t{}\n地址:\t{}\n\n'.format(v[0],v[1],k) for k,v in self.result.items()])
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header(fromaddr, 'utf-8')
        message['To'] =  Header(','.join(toaddrs), 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        username = 'princelailai@gmail.com'
        password = 'app password'
        try:
            server = smtplib.SMTP('smtp.gmail.com','587')
            server.ehlo()
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, message.as_string())
            server.quit()
            logging.info('Send Email Successful.')
        except:
            logging.info('Send Email Failed.')

    def run(self):
        self.read_json()
        for u in self.url:
            self.get_news(u)
        self.valid_news()
        if len(self.result) != 0:
            self.sent_email()

if __name__ == '__main__':
    moni = monitor_house_info()
    moni.run()
```
