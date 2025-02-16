from fortune_logic import generate_fortune
from flask import Flask, request
import json
from fortune_logic import generate_fortune
import requests
import os

app = Flask(__name__)

def reply_message(reply_token, message):
    line_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_token}"
    }
    body = {
        "replyToken": reply_token,
        "   messages": [{"type": "text", "text": message}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, data=json.dumps(body))
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data:
            return "No data", 400

        reply_token = data["events"][0]["replyToken"]
        user_message = data["events"][0]["message"]["text"]

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
        else:
            reply_message(reply_token, "🤖 わからんわ…もうちょっと具体的に頼むわ！")

        return "OK", 200

    except Exception as e:
        print(f"エラー発生: {e}")
        return "Internal Server Error", 500
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)