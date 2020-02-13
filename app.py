import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# start database setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
# ending database setup
# start flask app
app = Flask(__name__)

# @app.route("/")
# def index():
#     return (
#         "Available Routes:<br />"
#         "/api/v1.0/names<br />"
#         "/api/v1.0/measurements"
#     )

# @app.route("/api/v1.0/names")
# def names():
#     session = Session(engine)
#     results = session.query(Measurement.name).all()
#     session.close()
#     all_names = list(np.ravel(results))
#     return jsonify(all_names)

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