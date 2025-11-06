from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn,
                            CarouselTemplate, MessageAction, URIAction, ImageCarouselColumn, ImageCarouselTemplate,
                            ImageSendMessage, ButtonsTemplate, ConfirmTemplate)
import os
import html  # 使用標準庫的 escape 函數

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        if event.message.text.lower() == "test":
            reply_message = "第32行的reply_message=改成自己想傳送的訊息"
            line_bot_api.reply_message(event.reply_token,reply_message)
            
        if event.message.text == "confirm":
            confirm_template = TemplateSendMessage(
                alt_text = "confirm template",
                template = ConfirmTemplate(
                    text = 'drink coffee?',
                    actions = [
                        MessageAction(label='yes',text='yes'),
                        MessageAction(label='no',text='no')
                        
                        ]
                    )
                
                )
            line_bot_api.reply_message(event.reply_token,confirm_template)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,text=str(e))
        
        
    
if __name__ == "__main__":
    app.run()
