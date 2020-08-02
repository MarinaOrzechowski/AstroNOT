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
df = df[['Name', 'age', 'Gender', 'Year', 'Status', 'Birth Date', 'Birth Place',
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
            message_astronaut = 'We found an astronaut who went to space at your age!'
        else:
            message_astronaut = 'Did you know that the youngest US astronaut who went to space was '
            astronaut = df.iloc[0]
        a_name = astronaut.iloc[0]['Name']
        a_year_went_to_space = astronaut.iloc[0]['Year']
        a_birth_date = astronaut.iloc[0]['Birth Date']
        a_birth_place = astronaut.iloc[0]['Birth Place']
        a_college = astronaut.iloc[0]['Alma Mater']
        a_major_b = astronaut.iloc[0]['Undergraduate Major']
        a_major_g = astronaut.iloc[0]['Graduate Major']
        a_flights = astronaut.iloc[0]['Space Flights']
        a_flights_hr = astronaut.iloc[0]['Space Flight (hr)']
        a_walks = astronaut.iloc[0]['Space Walks']
        a_walks_hr = astronaut.iloc[0]['Space Walks (hr)']
        a_alive = astronaut.iloc[0]['Status']
        print(a_name, a_year_went_to_space, a_birth_date, a_birth_place, a_college,
              a_major_b, a_major_g, a_flights, a_flights_hr, a_walks, a_walks_hr, a_alive)

    return render_template("result.html", planet_result=planet, weight_result=new_weight, a_name=a_name, a_year_went_to_space=a_year_went_to_space, a_birth_date=a_birth_date, a_birth_place=a_birth_place, a_college=a_college, a_major_b=a_major_b, a_major_g=a_major_g, a_flights=a_flights, a_flights_hr=a_flights_hr, a_walks=a_walks, a_walks_hr=a_walks_hr, a_alive=a_alive, message_astronaut=message_astronaut)


if __name__ == '__main__':
    app.debug = True
    app.run()
