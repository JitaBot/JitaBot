import random

# 日替わり占い結果をユーザーごとに固定
user_fortune_cache = {}

def get_random_fortune(user_message):
    user_id = hash(user_message)  # ユーザーごとに一貫した結果を出すための仕組み
    if user_id not in user_fortune_cache:
        fortunes = [
            "🌟 大吉：今日は素晴らしい一日になる予感やで！",
            "🌸 中吉：ええ感じやで〜。穏やかに過ごせる日や！",
            "💫 小吉：ちょっと注意やで。けど努力は報われる！",
            "💀 凶：慎重に行動するんが吉やな。"
        ]
        user_fortune_cache[user_id] = random.choice(fortunes)
    return user_fortune_cache[user_id]