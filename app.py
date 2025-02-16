import os
import json
import random
import requests
from flask import Flask, request, render_template
from fortune_logic import generate_fortune

app = Flask(__name__)

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
    response = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, data=json.dumps(body))
    if response.status_code != 200:
        print(f"LINE送信エラー: {response.status_code}, {response.text}")

# LINE Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        reply_token = data["events"][0]["replyToken"]
        user_message = data["events"][0]["message"]["text"]

        # ユーザー入力による応答分岐
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
            reply_message(reply_token, "💰 金運ガイド：金運は星の巡りにも関係してるで！財布の紐は締める時や！")

        elif "恋愛" in user_message:
            reply_message(reply_token, "💖 恋愛ガイド：恋の行方が気になるんか？チャンスを逃さんように！")

        elif "ラッキーカラー" in user_message:
            colors = ["赤", "青", "緑", "黄", "紫", "ピンク", "オレンジ", "白", "黒"]
            color = random.choice(colors)
            reply_message(reply_token, f"🎨 今日のラッキーカラーは『{color}』やで！")

        else:
            reply_message(reply_token, "🤖 すんまへん、その質問にはまだ答えられへんねん…。")

        return "OK"

    except Exception as e:
        print(f"エラー発生: {e}")
        return "Internal Server Error", 500

# 運勢ページの表示
@app.route("/fortune/<user_id>")
def fortune_page(user_id):
    user_fortune = generate_fortune()
    return render_template("fortune.html", user_id=user_id, fortune=user_fortune)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)