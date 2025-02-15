from flask import Flask, request, jsonify
import random
import datetime
import os
import requests

app = Flask(__name__)

# 運勢メッセージリスト
fortune_messages = [
    "🌟 大吉：今日は素晴らしい1日になりそうやで！",
    "🌸 中吉：穏やかに過ごせる日やで〜。",
    "🎋 小吉：安定した運気が流れてるわ！",
    "💀 凶：慎重に行動するのが吉やな。"
]

# ユーザーごとの運勢を保存する辞書
user_fortunes = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.json
    for e in event["events"]:
        if e["type"] == "message" and e["message"]["type"] == "text":
            reply_token = e["replyToken"]
            user_message = e["message"]["text"]
            user_id = e["source"]["userId"]

            # 今日の日付を取得
            today = datetime.date.today().strftime("%Y-%m-%d")

            # ユーザーごとの運勢を1日1回だけ設定
            if user_id not in user_fortunes or user_fortunes[user_id]["date"] != today:
                user_fortunes[user_id] = {
                    "fortune": random.choice(fortune_messages),
                    "date": today
                }

            if "運勢" in user_message or "金運" in user_message or "恋愛" in user_message or "ラッキーカラー" in user_message:
                reply_message(reply_token, user_fortunes[user_id]["fortune"])

    return jsonify(status=200)


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