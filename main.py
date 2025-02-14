import os
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

def generate_stars():
    return '⭐' * random.randint(1, 5)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "今日の運勢は？":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=generate_stars())
        )

# Renderではgunicornで起動するので、ここは不要
# if __name__ == "__main__":
#     app.run()
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
