Title: 微信和telegram机器人入门
Date: 2018-11-20 14:39
Category: 玩电脑
Tags: 微信,telegram,机器人
Slug: introduction-wx-telegram-bot
Authors: Kevin Chen
Status: draft



`wechat_bot.py`

```
from flask import Flask, make_response, request
import itchat
from itchat.content import TEXT, NOTE, SYSTEM
import re

app = Flask(__name__)


class LastMessage:
    code = None
    text = None


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@itchat.msg_register([TEXT, NOTE, SYSTEM], isMpChat=True)
def get_code(msg):
    vericode = None
    print(dir(msg))
    try:
        vericode = re.search("\d{4}", msg.text).group()
    except AttributeError:
        pass
    except TypeError:
        pass
    finally:
        LastMessage.code = vericode
        # msg.user.send("收到验证码：{}".format(vericode))
        itchat.send("类型：{}， 原始信息：{}， 收到验证码：{}".format(msg.type, msg.text, vericode))


@app.route('/')
def main():
    middle_varible, LastMessage.code = LastMessage.code, None
    if middle_varible:
        return make_response(middle_varible)
    else:
        return make_response("")


if __name__ == "__main__":
    itchat.auto_login(enableCmdQR=2)
    itchat.run(blockThread=False)
    try:
        app.run()
    except KeyboardInterrupt:
        itchat.logout()
        shutdown_server()

```





`telegram_bot.py`

```
import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = "762561287:AAGx2cStFozY4NQ9voWe0dw5yP8_zkRy-f4"


class LastMessage:
    mes = None
    bot = None


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    LastMessage.mes = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    LastMessage.bot = bot
    # print(dir(bot))
    print("Message is:{}".format(LastMessage.mes))


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()


```

