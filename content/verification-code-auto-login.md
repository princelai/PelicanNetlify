Title: 实现爬虫短信验证码自动登录
Date: 2018-11-20 14:53
Category: IT笔记
Tags:
Slug: crawler-sms-verification-code-auto-login
Authors: Kevin Chen
Status: draft



最近在学爬虫，遇到了一个只能使用短信验证码和微信扫码登录的网站，扫码是不可能做成全自动的，于是我全力攻克手机验证码登录，这期间我先后尝试过使用telegram bot，微信机器人进行转发，但是都遇到了一些问题，这个可以看我之前写的文章







`GetCode.py`

```python
import logging
from time import sleep

from requests_html import HTMLSession


def get_code():
    API = "http://lunarch.top:5000/Get/"
    max_try = 3
    with HTMLSession() as session:
        while max_try > 0:
            with session.get(API, timeout=10) as resp:
                try:
                    assert resp.status_code == 200
                except AssertionError:
                    max_try -= 1
                    logging.info("无法连接服务器，等待5秒......")
                    sleep(5)
                    continue
                else:
                    code = resp.text
                    if code == '':
                        max_try -= 1
                        logging.info("验证码还没来，等待5秒......")
                        sleep(5)
                        continue
                    else:
                        return code
        else:
            logging.info("手机未收到验证码或Tasker任务出现问题")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    get_code()

```





`PushMessage.py`

```python
import re
from collections import deque

from flask import Flask, request

q = deque(maxlen=1)
app = Flask(__name__)
pattern = re.compile("\d{4}", flags=re.DOTALL | re.MULTILINE)


@app.route('/')
def index():
    return 'index running'


@app.route('/Send')
def send():
    key = "text"
    content = request.args.get(key, '')
    q.append(content)
    return 'Send Success'


@app.route('/Get/')
def get_code():
    if len(q) != 0:
        message = q.pop()
        try:
            code = pattern.search(message).group()
        except AttributeError:
            return ""
        else:
            return code
    else:
        return ''


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```

