from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    stars = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    fortune = random.choice(stars)  # ランダムに星を選ぶ
    return jsonify({"fortune": fortune}), 200  # ensure_ascii=Falseは不要

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
