import os
import json
import random
import requests
from flask import Flask, request
from shortener import shorten_url
from utils import get_random_fortune

app = Flask(__name__)

# LINEメッセージ返信
def reply_message(reply_token, message):
    line_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_token}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, data=json.dumps(body))
    if response.status_code != 200:
        print(f"LINE送信エラー: {response.status_code}, {response.text}")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        reply_token = data["events"][0]["replyToken"]
        user_message = data["events"][0]["message"]["text"]

        # ユーザー入力による応答分岐
        if "運勢" in user_message or "今日の運勢" in user_message:
            fortune = get_random_fortune(user_message)
            reply_message(reply_token, fortune)

        elif "金運" in user_message:
            reply_message(reply_token, "💰 金の流れは星の巡りにも関係しとるで！財布の紐は締めるべき時やで！")

        elif "恋愛" in user_message:
            reply_message(reply_token, "💞 恋の行方が気になるんか？チャンスを逃さんようにな！")

        elif "ラッキーカラー" in user_message:
            colors = ["赤", "青", "緑", "黄色", "紫", "ピンク", "オレンジ", "白", "黒"]
            color = random.choice(colors)
            reply_message(reply_token, f"🎨 今日のラッキーカラーは『{color}』やで！")

        elif "占星リンク" in user_message:
            long_url = "https://chapro.jp/prompt/67185"
            short_url = shorten_url(long_url)
            reply_message(reply_token, f"🔗 星占いの参考リンクやで！：{short_url}")

        else:
            reply_message(reply_token, "🤖 すんまへん、その質問にはまだ答えられへんねん…。")

        return "OK"
    except Exception as e:
        print(f"エラー発生: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)