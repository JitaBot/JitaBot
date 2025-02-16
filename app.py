from flask import Flask, request
import json
import requests
import random
from datetime import datetime
import os
from fortune_logic import generate_fortune

app = Flask(__name__)

# LINEメッセージを返信する関数
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
    response = requests.post("https://api.line.me/v2/bot/message/reply",
                              headers=headers, data=json.dumps(body))
    if response.status_code != 200:
        print(f"LINE送信エラー: {response.status_code}, {response.text}")

# Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        if not data or "events" not in data or len(data["events"]) == 0:
            return "No events", 200

        event = data["events"][0]
        reply_token = event["replyToken"]
        user_message = event["message"]["text"]

        # ユーザー入力に基づいて応答を選択
        if "運勢" in user_message or "今日の運勢" in user_message:
            fortune = generate_fortune()
            response_text = (
                f"🔮 今日の運勢 🔮\n"
                f"📅 日付: {fortune['date']}\n"
                f"💬 メッセージ: {fortune['fortune']}\n"
                f"🎨 ラッキーカラー: {fortune['lucky_color']}\n"
                f"🔢 ラッキーナンバー: {fortune['lucky_number']}"
            )
            reply_message(reply_token, response_text)

        elif "金運" in user_message:
            reply_message(reply_token, "💰 金運ガイド: 財運を高めるには財布の整理が吉！")

        elif "恋愛" in user_message:
            reply_message(reply_token, "💞 恋愛ガイド: 素直な気持ちを伝えることが大切やで！")

        elif "ラッキーカラー" in user_message:
            colors = ["赤", "青", "緑", "黄", "紫", "ピンク", "オレンジ", "白", "黒"]
            color = random.choice(colors)
            reply_message(reply_token, f"🎨 今日のラッキーカラーは「{color}」やで！")

        else:
            reply_message(reply_token, "🤖 すまん、その質問にはまだ答えられへんわ…")

        return "OK", 200

    except Exception as e:
        print(f"エラー発生: {e}")
        return "Internal Server Error", 500

# Render環境用ポート設定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)