from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("land.html")


@app.route("/data", methods=['GET', 'POST'])
def data():
    return render_template("data.html")


@app.route("/result", methods=['POST', 'GET'])
def result():
    return render_template("result.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
