import os
import requests
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 運勢メッセージリスト
fortune_messages = [
    "🌟 大吉：今日は素晴らしい一日になる予感！",
    "💫 中吉：良いことがありそう！",
    "🌸 小吉：穏やかに過ごせる日です。",
    "⚖️ 吉：安定した運気が流れています。",
    "🌑 凶：慎重に行動するのが吉。"
]

# Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.json
    for e in event["events"]:
        if e["type"] == "message" and e["message"]["type"] == "text":
            reply_token = e["replyToken"]
            user_message = e["message"]["text"]

            # 今日の運勢リクエストに応答
            if "今日の運勢" in user_message.strip():
                fortune = random.choice(fortune_messages)
                reply_message(reply_token, fortune)

    return jsonify(status=200)

# LINEメッセージ送信関数
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
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)