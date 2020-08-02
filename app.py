from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

gravity_dict = {'Mercury': 0.38, 'Venus': 0.91, 'Mars': 0.38,
                "Jupiter": 2.34, 'Saturn': 0.93, 'Uranus': 0.92, 'Neptune': 1.12}

# read astronaut data into pandas dataframe
df = pd.read_csv(
    'https://raw.githubusercontent.com/MarinaOrzechowski/AstroNOT/master/static/US_astronauts.csv')
df = df[pd.notnull(df['Year'])]
df['birth_year'] = df['Birth Date'].astype('str').str[-4:].astype(int)
df['age'] = df['Year'] - df['birth_year']
df = df[['Name', 'age', 'Year', 'Status', 'Birth Date', 'Birth Place',
         'Alma Mater', 'Undergraduate Major', 'Graduate Major',
         'Space Flights',
         'Space Flight (hr)', 'Space Walks', 'Space Walks (hr)']]
df = df.sort_values(by='age')


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
        if '.' in weight:
            weight = float(weight)
        else:
            weight = int(weight)
        new_weight = weight*gravity_dict[planet]

        # find an astronaut of similar age
        astronauts = df[df['age'].astype(int) == int(age)]
        if len(astronauts.index) > 0:
            astronaut = astronauts.sample()  # randomly choose one astronaut's info to output
            is_astronaut_found = True
        else:
            is_astronaut_found = False
            astronaut = df.iloc[0]

    return render_template("result.html", planet_result=planet, weight_result=new_weight)


if __name__ == '__main__':
    app.debug = True
    app.run()
