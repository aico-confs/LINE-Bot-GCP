import os

from flask import Flask, abort, request
from message import *

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


def create_app():

    app = Flask(__name__)

    line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
    handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

    @app.route("/", methods=["GET", "POST"])
    def callback():

        if request.method == "GET":
            return "Hello GCP"
        if request.method == "POST":
            signature = request.headers["X-Line-Signature"]
            body = request.get_data(as_text=True)

            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                abort(400)

            return "OK"


    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        cities = ['大林鎮', '溪口鄉', '阿里山鄉', '梅山鄉', '新港鄉', '民雄鄉', '六腳鄉', '竹崎鄉', '東石鄉', '太保市', '番路鄉', '朴子市', '水上鄉', '中埔鄉', '布袋鎮', '鹿草鄉', '義竹鄉', '大埔鄉']    
        reply_token = event.reply_token
        message = event.message.text
        to = event.source.user_id
        
        if (message.strip() in cities):
            line_bot_api.push_message(to, TextSendMessage(text=message+'的天氣預報如下：'))
            line_bot_api.push_message(to, weather_predict(message))
        if(message == '嘉義縣各地區氣象查詢'):
            line_bot_api.push_message(to, TextSendMessage(text='請點擊您想查詢的區域~'))
            line_bot_api.reply_message(reply_token, all_town())

        
    return app
