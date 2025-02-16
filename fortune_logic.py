from datetime import datetime
import random

# 運勢メッセージのテンプレート
fortune_templates = [
    "今日はエネルギッシュな一日！直感を信じて行動しよう！",
    "静かに自分と向き合う時間を作ると、新たな発見があるかも。",
    "思いがけない幸運が訪れるかも！オープンな心で過ごそう。",
    "人間関係が活性化する日。気軽な会話がチャンスを呼ぶ。",
    "努力が報われる兆しあり！粘り強くチャレンジを続けよう！"
]

# 運勢を生成する関数
def generate_fortune():
    today = datetime.now().strftime("%Y-%m-%d")
    fortune = random.choice(fortune_templates)
    lucky_color = random.choice(["青", "赤", "緑", "黄", "紫", "ピンク", "白", "黒"])
    lucky_number = random.randint(1, 99)

    return {
        "date": today,
        "fortune": fortune,
        "lucky_color": lucky_color,
        "lucky_number": lucky_number
    }