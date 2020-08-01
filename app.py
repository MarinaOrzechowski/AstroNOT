from flask import Flask, render_template, request

app = Flask(__name__)

gravity_dict = {'Mercury': 0.38, 'Venus': 0.91, 'Mars': 0.38,
                "Jupiter": 2.34, 'Saturn': 0.93, 'Uranus': 0.92, 'Neptune': 1.12}


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("land.html")


@app.route("/data", methods=['GET', 'POST'])
def data():
    return render_template("data.html")


@app.route("/result", methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # extract user input
        image = request.files.get('img_name')
        age = request.form.get('age')
        weight = request.form.get('weight')
        planet = request.form.get('planet_dropdown')
        print(age, weight, planet)
        new_weight = weight*gravity_dict[planet]

    return render_template("result.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
