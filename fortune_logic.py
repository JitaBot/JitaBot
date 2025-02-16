from datetime import datetime
import random

# 運勢メッセージテンプレート
fortune_templates = [
    "今日はエネルギッシュな一日！自分の直感を信じて行動しよう。",
    "静かに自分と向き合う時間を作ると、新たな発見があるかも。",
    "今日は思いがけない幸運が訪れるかも！オープンな心で過ごそう。",
    "人間関係が活性化する日。気軽な会話からチャンスが生まれるよ。",
    "努力が報われる兆しあり！粘り強く挑戦を続けよう。",
    "未知の挑戦に飛び込む勇気が運を呼び寄せる日。",
    "過去の経験がヒントをくれる日。振り返りが鍵となる。",
    "人のために動けば、それが自分に返ってくる日。",
    "自然の中でリラックスすると心がリセットされるよ。",
    "今日は笑顔が幸運の引き金に。ポジティブな態度を忘れずに！"
]

def generate_fortune():
    today = datetime.now().strftime("%Y-%m-%d")
    fortune = random.choice(fortune_templates)
    lucky_color = random.choice(["青", "赤", "緑", "黄色", "紫", "ピンク", "オレンジ", "白", "黒"])
    lucky_number = random.randint(1, 99)
    return {
        "date": today,
        "fortune": fortune,
        "lucky_color": lucky_color,
        "lucky_number": lucky_number
    }