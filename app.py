import requests
import os
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 運勢メッセージ
fortune_messages = [
    "🌟 大吉：今日は素晴らしい一日になりそうやで！",
    "🌸 中吉：穏やかに過ごせる日になりそうやで。",
    "🎋 小吉：落ち着いて行動すればええ日になるで！",
    "💀 凶：慎重に行動するのが吉やな。"
]

# URL短縮関数
def shorten_url(long_url):
    bitly_token = os.environ.get("BITLY_ACCESS_TOKEN")
    headers = {
        "Authorization": f"Bearer {bitly_token}",
        "Content-Type": "application/json"
    }
    payload = {"long_url": long_url}
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("link")
    else:
        return f"エラー: {response.status_code}"

# Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.json
    for e in event["events"]:
        if e["type"] == "message" and e["message"]["type"] == "text":
            reply_token = e["replyToken"]
            user_message = e["message"]["text"]

            # URL短縮機能
            if user_message.startswith("URL短縮"):
                url_to_shorten = user_message.split(" ", 1)[-1]
                short_url = shorten_url(url_to_shorten)
                reply_message(reply_token, f"短縮URL: {short_url}")

            # 占い機能（運勢、金運、恋愛、ラッキーカラー）
            elif any(keyword in user_message for keyword in ["今日の運勢", "運勢", "金運", "恋愛", "ラッキーカラー"]):
                fortune = random.choice(fortune_messages)
                reply_message(reply_token, fortune)

            else:
                reply_message(reply_token, "🤖 すんまへん、その質問には答えられへんわ。")

    return jsonify(status=200)

# LINEメッセージ返信関数
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
    requests.post("https