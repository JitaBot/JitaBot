from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    return jsonify({"message": "OK"}), 200  # JSONで返す

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
