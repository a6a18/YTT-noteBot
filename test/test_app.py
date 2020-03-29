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
    'AS7KCSMyZ2gvSEGssLGA9sZg7EwAs3RCkT6qGPhvKsPSbQCMX1lG7kw92jmOGBVCUfki1JWjXlINJ4ZBuAoyrXYiwFik3DrT81ziBjg/c4xwQ/WKsbfJQ2lGuulhQLpzTbEgyfI+ANivUb8llZVeEwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1e3daba5ee10753eb11ce13f3df7ab51')

####### 資料庫 ######
#DB_URL = os.getenv('MONGOLAB_URI')
myclient = pymongo.MongoClient("mongodb+srv://a6a18:Aa19950501@cluster0-8ingu.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient['Line']

###### 規則 ######

@app.route('/')
def index():
    return 'Hello World!'


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


def find_category():
    pass



def find_link(category):
    mycol = mydb[category]
    link = ''
    for index, value in enumerate(mycol.find()):
        link = link + str(index+1) + ". " + value['link'] + '\n'
    return link
#content = content + str(index+1) + ". " + collection + '\n'

####### 關鍵字code #####


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)

    if "save" in event.message.text:
        text = event.message.text.split("\n")
        category = text[1]
        link = text[2]
        if " " in link:
            link = link.replace(" ", "\n")
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

    if "目錄" in event.message.text:
        content = ''
        list_collection = mydb.list_collection_names()
        for index, collection in enumerate(list_collection):
            content = content + str(index+1) + ". " + collection + '\n'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0


if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5000)
