import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
from sqlalchemy import or_
from sqlalchemy import and_
from dateutil.relativedelta import *

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
    return render_template('index.html',json_content={'Welcome!': 'Contents will be displayed here'}, message_type="Success", message_content="Welcome!")

@app.route("/api/v1.0/precipitation/<type>", methods=['GET', 'POST'])
def precipitation(type):
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
        
    if type != "raw":
        return render_template('index.html', json_content=all_measurements, message_type="Success", message_content="Success! Returning Precipitation data")
    else:
        return jsonify(all_measurements)

@app.route("/api/v1.0/stations/<type>", methods=['GET', 'POST'])
def stations(type):
    session = Session(engine)
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    all_stations = []
    # format into JSON
    for id, station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['ID'] = id
        station_dict['Station'] = station
        station_dict['Name'] = name
        station_dict['Latitude'] = latitude
        station_dict['Longitude'] = longitude
        station_dict['Elevation'] = elevation
        all_stations.append(station_dict)
    
    if type != "raw":
        return render_template('index.html', json_content=all_stations, message_type="Success", message_content="Success! Returning Stations data")
    else:
        return jsonify(all_stations)


@app.route("/api/v1.0/tobs/<type>", methods=['GET', 'POST'])
def tobs(type):
    session = Session(engine)
    max_date = session.query(func.max(Measurement.date)).first()
    maxdate = dt.datetime.strptime(str(max_date[0]), "%Y-%m-%d")
    #Use relative data to get the last 12 months from the date of the max date
    last_12_months = maxdate + relativedelta(months=-12)
    results = session.query(Measurement.date, Measurement.tobs).filter(and_(Measurement.date>=last_12_months, Measurement.date <= maxdate)).all()
    # results = session.query(Measurement.date, Measurement.tobs).limit(10).all()
    session.close()
    all_measurements = []
    # format into JSON
    for date, tobs in results:
        measurement_dict = {}
        measurement_dict['Date'] = date
        measurement_dict['Precipitation'] = tobs
        all_measurements.append(measurement_dict)
    
    if type != "raw":
        return render_template('index.html', json_content=all_measurements, message_type="Success", message_content="Success! Returning the last 12 months Total Observed Temperature data")
    else:
        return jsonify(all_measurements)


if __name__ == "__main__":
    app.run(debug=True)
# end flask app