from flask import Flask, request

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    print("Received a request on /callback")  # ログ出力用
    return "OK", 200

@app.route("/")
def home():
    return "Hello, this is JitaBot!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
