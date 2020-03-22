import pymongo
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from flask import Flask

app = Flask(__name__)
line_bot_api = LineBotApi(
    'oPYz4BpH7Ku0wwnpHvneWmHdCrCpY3Vy6LPYRBnHJNIME0MY1YC2KLmgQT3b/XwG2M0+g3tteIDxVeVZQoRaZIKA2+eadmvRlbM0uiAotkFC6yek811Ayl87eeHa0RYwIp3CJfYHYoGp36+nYWeeSgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('05f3de3f167958ca435d64a6032558f2')


####### 資料庫 ######

myclient = pymongo.MongoClient("mongodb+srv://a6a18:Aa19950501@cluster0-8ingu.mongodb.net/test?retryWrites=true&w=majority")


###### 規則 ######

def save_link(category, link):
    mydb = myclient['Line']
    mycol = mydb[category]
    mydict = {'name': category, 'link': link}
    x = mycol.insert_one(mydict)
    if 'pymongo.results.InsertOneResult' in x:
        return '儲存成功'
    else:
        return '儲存失敗'


####### 關鍵字code #####


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)

    if "save" in event.message.text:
        text = event.message.text.split(" ")
        category = text[1]
        link = text[2]
        try:
            content = save_link(category, link)
        except:
            content = '凹嗚>< 好像出錯囉'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
