import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
# start database setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# ending database setup
# start flask app
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/api/v1.0/precipitation", methods=['GET', 'POST'])
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).limit(10).all()
    session.close()
    all_measurements = []
    # format into JSON
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict['Date'] = date
        measurement_dict['Precipitation'] = prcp
        all_measurements.append(measurement_dict)
    

    # python_data = json.loads(json.dumps(all_measurements))
    return render_template('index.html', json_content=all_measurements)

    # all_names = list(np.ravel(results))
    # return jsonify(all_names)

# @app.route("/api/v1.0/measurements")
# def measurements():
#     session = Session(engine)
#     results = session.query(Measurement.name, Measurement.age, Measurement.sex).all()
#     session.close()
#     all_measurements = []
#     # format into JSON
#     for name, age, sex in results:
#         measurement_dict = {}
#         measurement_dict['name'] = name
#         measurement_dict['age'] = age
#         measurement_dict['sex'] = sex
#         all_measurements.append(measurement_dict)
#     return jsonify(all_measurements)

if __name__ == "__main__":
    app.run(debug=True)
# end flask app