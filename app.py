import pymongo
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os

app = Flask(__name__)
line_bot_api = LineBotApi(
    'f3DH5PI/pP+u+KQbqDCXr9G3ydwq6GVEsDQOMuilVh6/geI1j+MrPnRdxoLcSH+LEBcMmhAGTptPg7moP2rZx9Dxg1MMGbOGyqwhm3FutumcNDFkvcnYr/amps46hhmV6KUW/vLuHSCXT2KKEEJ9hwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ac24d1d12114ff7d1da90f2864516da0')

####### 資料庫 ######
DB_URL = os.getenv('MONGOLAB_URI')
myclient = pymongo.MongoClient(DB_URL)
mydb = myclient['Line']


###### 規則 ######


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


def save_link(category, link):
    mycol = mydb[category]
    mydict = {'name': category, 'link': link}
    x = mycol.insert_one(mydict)
    return '資料儲存成功！'


def del_link():
    pass


def find_link(category):
    mycol = mydb[category]
    link = ''
    for index, value in enumerate(mycol.find()):
        link = link + value['link'] + '\n'
    return link

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

    if "fmega" in event.message.text:
        text = event.message.text.split(" ")
        category = text[1]
        link = text[2]
        try:
            content = category + link
        except:
            content = '凹嗚>< 好像出錯囉'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if "find" in event.message.text:
        text = event.message.text.split(" ")
        category = text[1]
        try:
            content = find_link(category)
        except:
            content = '凹嗚>< 好像出錯囉'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
