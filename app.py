from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import os
import json

app = Flask(__name__)

# チャネルシークレットを環境変数から取得
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

def verify_signature(request):
    # LINEからのリクエスト署名を検証
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    hash = hmac.new(CHANNEL_SECRET.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    expected_signature = base64.b64encode(hash).decode('utf-8')
    return hmac.compare_digest(signature, expected_signature)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Webhookリクエストの署名を検証
    if not verify_signature(request):
        return "Signature verification failed", 403

    data = request.get_json()
    if not data.get("events"):
        return "No events", 200

    # イベントを解析して応答
    for event in data["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            if "運勢" in user_message or "今日の運勢" in user_message:
                fortune = generate_fortune()
                response_text = (
                    f"🔮 今日の運勢 🔮\n"
                    f"📆 日付: {fortune['date']}\n"
                    f"💬 メッセージ: {fortune['fortune']}\n"
                    f"🎨 ラッキーカラー: {fortune['lucky_color']}\n"
                    f"🔢 ラッキーナンバー: {fortune['lucky_number']}"
                )
                reply_message(reply_token, response_text)

    return "OK", 200

def reply_message(reply_token, message):
    # LINE APIへの応答
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('CHANNEL_ACCESS_TOKEN')}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, headers=headers, data=json.dumps(payload))

# 運勢生成関数
def generate_fortune():
    from datetime import datetime
    import random
    today = datetime.now().strftime("%Y-%m-%d")
    fortune_templates = [
        "今日はエネルギッシュな一日！自分の直感を信じて行動しよう。",
        "静かに自分と向き合う時間を作ると、新たな発見があるかも。",
        "今日は思いがけない幸運が訪れるかも！オープンな心で過ごそう。",
        "人間関係が活性化する日。気軽な会話からチャンスが生まれるよ。",
        "努力が報われる兆しあり！粘り強く挑戦を続けよう。"
    ]
    lucky_color = random.choice(["青", "赤", "緑", "黄色", "紫"])
    lucky_number = random.randint(1, 99)
    return {
        "date": today,
        "fortune": random.choice(fortune_templates),
        "lucky_color": lucky_color,
        "lucky_number": lucky_number
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)