import os
import requests
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 運勢メッセージリスト（関西弁）
fortune_messages = [
    "🌟 大吉：今日は最高や！ええこと起こる予感やで！",
    "🌸 中吉：ええ感じやで〜。穏やかに過ごせる一日になるわ！",
    "🏯 小吉：ぼちぼちええ感じやけど、油断は禁物やで。",
    "🌊 吉：波はあるけど、まぁまぁええ一日やと思うわ。",
    "🌪️ 凶：ちょっと気ぃつけなあかん日やな。慎重にな！"
]

# ラッキーカラー・ナンバー
lucky_colors = ["赤", "青", "緑", "黄色", "紫", "ピンク", "オレンジ"]
lucky_numbers = [random.randint(1, 99) for _ in range(5)]

# Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.json
    for e in event["events"]:
        if e["type"] == "message" and e["message"]["type"] == "text":
            reply_token = e["replyToken"]
            user_message = e["message"]["text"]

            # キーワード判定＆返答
            if any(word in user_message for word in ["運勢", "今日の運勢", "明日の運勢"]):
                fortune = random.choice(fortune_messages)
                reply_message(reply_token, fortune)

            elif "金運" in user_message:
                fortune = random.choice(fortune_messages) + " ほな、財布の紐、締めるかどうかは自分次第やで！"
                reply_message(reply_token, fortune)

            elif "恋愛運" in user_message:
                fortune = random.choice(fortune_messages) + " 恋の星がええ感じに回っとるで！"
                reply_message(reply_token, fortune)

            elif "仕事運" in user_message:
                fortune = random.choice(fortune_messages) + " 今日は仕事がサクサク進むかもしれへんで！"
                reply_message(reply_token, fortune)

            elif "健康運" in user_message:
                fortune = random.choice(fortune_messages) + " 今日は無理せんと、ぼちぼちいこか！"
                reply_message(reply_token, fortune)

            elif "ラッキーカラー" in user_message:
                color = random.choice(lucky_colors)
                reply_message(reply_token, f"🎨 今日のラッキーカラーは「{color}」やで！")

            elif "ラッキーナンバー" in user_message:
                number = random.choice(lucky_numbers)
                reply_message(reply_token, f"🔢 今日のラッキーナンバーは「{number}」やで！")

            elif "占い" in user_message or "占って" in user_message or "星占い" in user_message:
                reply_message(reply_token, "🔮 ほな、どんなこと占って欲しいんか教えてな？『運勢』『金運』『恋愛運』とかやで！")

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