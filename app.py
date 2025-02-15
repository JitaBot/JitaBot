import os
import requests
from flask import Flask, request, jsonify
import random
import datetime

app = Flask(__name__)

# 占いメッセージ（関西弁）
fortune_messages = {
    "運勢": ["🌟 大吉：今日は素晴らしい1日になりそうやで！", 
              "🌸 中吉：穏やかでええ感じの日になるわ！", 
              "🌙 吉：安定した運気が流れとるで！", 
              "💀 凶：慎重に行動するのが吉やな。"],
    "金運": ["💴 今日は財布の紐、しっかり締めるんやで！", 
             "💰 思わぬ臨時収入があるかも知れへんで！", 
             "🌠 金の流れは星の巡りにも関係しとるで！"],
    "恋愛": ["💞 今日は運命の出会いがあるかもしれへんで！", 
             "💕 恋のチャンス、逃したらあかんで！", 
             "💔 今日は一歩引いて相手を見つめ直す日やな。"],
    "ラッキーカラー": ["🎨 今日のラッキーカラーは『ピンク』やで！", 
                        "🎨 今日のラッキーカラーは『ブルー』やで！", 
                        "🎨 今日のラッキーカラーは『ゴールド』やで！"]
}

# ユーザーごとのデータ管理（シンプル版）
user_data = {}

# Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.json
    for e in event["events"]:
        if e["type"] == "message" and e["message"]["type"] == "text":
            user_id = e["source"]["userId"]
            reply_token = e["replyToken"]
            user_message = e["message"]["text"]

            # ログ出力
            print(f"[{datetime.datetime.now()}] User: {user_id}, Message: {user_message}")

            # 今日の日付取得
            today = datetime.date.today().isoformat()

            # 1日1回の結果固定処理
            if user_id not in user_data or user_data[user_id].get("date") != today:
                user_data[user_id] = {"date": today, "results": {}}

            # キーワードに基づく応答
            response = None
            for keyword, messages in fortune_messages.items():
                if keyword in user_message:
                    # 1日1回固定結果取得
                    if keyword not in user_data[user_id]["results"]:
                        result = random.choice(messages)
                        user_data[user_id]["results"][keyword] = result
                    response = user_data[user_id]["results"][keyword]
                    break

            # 該当する応答がない場合のデフォルトメッセージ
            if not response:
                response = "🤖 すまんけど、その質問には答えられへんわ。"

            # LINEに返信
            reply_message(reply_token, response)

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
    response = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)
    print(f"LINE API Response: {response.status_code}, {response.text}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)