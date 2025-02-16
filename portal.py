from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fortune')
def fortune():
    return render_template('fortune.html')

@app.route('/love')
def love():
    return render_template('love.html')

@app.route('/money')
def money():
    return render_template('money.html')

@app.route('/luck-color')
def luck_color():
    return render_template('luck-color.html')

@app.route('/subscription')
def subscription():
    return render_template('subscription.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)