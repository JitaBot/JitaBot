from flask import Flask, render_template, request
from datetime import datetime
import random

app = Flask(__name__)

# 運勢メッセージテンプレート
fortune_templates = [
    "今日はエネルギッシュな一日！自分の直感を信じて行動しよう。",
    "静かに自分と向き合う時間を作ると、新たな発見があるかも。",
    "今日は思いがけない幸運が訪れるかも！オープンな心で過ごそう。",
    "人間関係が活性化する日。気軽な会話からチャンスが生まれるよ。",
    "努力が報われる兆しあり！粘り強く挑戦を続けよう。"
]

# 運勢データ生成
def generate_fortune():
    today = datetime.now().strftime("%Y-%m-%d")
    fortune = random.choice(fortune_templates)
    lucky_color = random.choice(["青", "赤", "緑", "黄色", "紫"])
    lucky_number = random.randint(1, 99)
    return {
        "date": today,
        "fortune": fortune,
        "lucky_color": lucky_color,
        "lucky_number": lucky_number
    }

@app.route("/fortune/<user_id>")
def fortune_page(user_id):
    user_fortune = generate_fortune()
    return render_template("fortune.html", user_id=user_id, fortune=user_fortune)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)