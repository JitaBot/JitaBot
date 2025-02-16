from datetime import datetime
import random

fortune_templates = [
    "今日はエネルギッシュな一日！自分の直感を信じて行動しよう。",
    "静かに自分と向き合う時間を作ると、新たな発見があるかも。",
    "今日は思いがけない幸運が訪れるかも！オープンな心で過ごそう。",
    "人間関係が活性化する日。気軽な会話からチャンスが生まれるよ。",
    "努力が報われる兆しあり！粘り強く挑戦を続けよう。"
]

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