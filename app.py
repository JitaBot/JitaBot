import os
import requests
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 運勢メッセージリスト
fortune_messages = [
    "🌟 大吉：今日は素晴らしい一日になる予感！",
    "🌸 中吉：穏やかに過ごせる日です。",
    "🏔️ 吉：安定した運気が流れています。",
    "🌑 凶：慎重に行動するのが吉。",
]

# 恋愛メッセージリスト
love_messages = [
    "💞恋の行方が気になるんか？ええやん、ええやん！ほな、ワシが星に聞いたるわ！",
    "🌹恋愛運か？今日は星がええ感じに輝いとるで！チャンスには素直になってみるんやで！",
    "💔あらま…ちょっと慎重にいかなあかんかもしれへんな。焦らんと、ゆっくり様子見や！",
    "🔮今日はロマンチックな出会いの予感があるで！目ぇ離したらもったいないかもな！",
    "💡好きな人にひと言、勇気出して声かけるタイミングかもしれんで？星も応援しとるわ！",
]

# 金運メッセージリスト
money_messages = [
    "💰今日は金運ええ感じやで！財布の紐は締めつつ、ええタイミングで使ってみ？",
    "🌌金の流れは星の巡りにも関係しとるで！今日は臨時収入の予感がするわ！",
    "💸おっと、今日は財布の紐をしっかり締める日やな！油断は禁物やで！",
]

# ラッキーカラーメッセージリスト
lucky_colors = ["🔴赤", "🔵青", "🟢緑", "🟡黄", "🟣紫", "🟤茶", "⚪白", "⚫黒", "🟠オレンジ", "🌸ピンク"]

@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.json
    for e in event["events"]:
        if e["type"] == "message" and e["message"]["type"] == "text":
            reply_token = e["replyToken"]
            user_message = e["message"]["text"].lower()

            # メッセージ内容に応じて返信内容を決定
            if "今日の運勢" in user_message or "運勢" in user_message:
                fortune = random.choice(fortune_messages)
                reply_message(reply_token, fortune)

            elif any(word in user_message for word in ["恋愛", "好きな人", "片思い", "結婚", "恋"]):
                love = random.choice(love_messages)
                reply_message(reply_token, love)

            elif "金運" in user_message:
                money = random.choice(money_messages)
                reply_message(reply_token, money)

            elif "ラッキーカラー" in user_message:
                color = random.choice(lucky_colors)
                reply_message(reply_token, f"🎨今日のラッキーカラーは『{color}』やで！")

            else:
                reply_message(reply_token, "🤖 すんまへん、その質問には答えられへんみたいやわ。")

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