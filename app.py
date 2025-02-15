import os
import requests
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 運勢メッセージリスト
fortune_messages = [
    "🌟 大吉：今日は素晴らしい一日になる予感！",
    "🌸 中吉：穏やかに過ごせる日です。",
    "🌿 吉：安定した運気が流れています。",
    "☁️ 凶：慎重に行動するのが吉。"
]

# Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        event = request.json
        print("🚀 Webhook受信:", event)  # デバッグ用ログ
        
        for e in event.get("events", []):
            if e.get("type") == "message" and e.get("message", {}).get("type") == "text":
                reply_token = e.get("replyToken")
                user_message = e.get("message", {}).get("text")
                
                if "今日の運勢" in user_message:
                    fortune = random.choice(fortune_messages)
                    reply_message(reply_token, fortune)
                    print(f"🔮 送信メッセージ: {fortune}")  # デバッグログ
                else:
                    reply_message(reply_token, "🤖 すみません、その質問には答えられません。")
        return jsonify(status=200)

    except Exception as e:
        print(f"⚠️ エラー発生: {e}")
        return jsonify(status=500, error=str(e))

# LINEメッセージ送信関数
def reply_message(reply_token, message):
    line_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
    if not line_token:
        print("❌ CHANNEL_ACCESS_TOKENが設定されていません！")
        return
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_token}"
    }

    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }

    response = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)
    print(f"📡 LINE APIレスポンス: {response.status_code}, {response.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)