import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
from flask import abort
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html',json_content={ 'Error 404!' : 'Page not found!'}, message_type="Error", message_content="WHERE WERE YOU GOING? :/"), 404

@app.errorhandler(400)
def invalid_parameter(e):
    return render_template('index.html',json_content={ 'Error!' : 'Invalid parameter!'}, message_type="Error", message_content="Invalid parameter passed!"), 400


@app.route("/api/v1.0/precipitation/<type>", methods=['GET', 'POST'])
def precipitation(type):
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_measurements = []
    # format into JSON
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict['Date'] = date
        measurement_dict['Precipitation'] = prcp
        all_measurements.append(measurement_dict)

    if type == "inline":
        return render_template('index.html', json_content=all_measurements, message_type="Success", message_content="Success! Returning Precipitation data")
    elif type == "raw":
        return jsonify(all_measurements)
    else:
        abort(404)

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
    
    if type == "inline":
        return render_template('index.html', json_content=all_stations, message_type="Success", message_content="Success! Returning Stations data")
    elif type == "raw":
        return jsonify(all_stations)
    else:
        abort(404)

@app.route("/api/v1.0/tobs/<type>", methods=['GET', 'POST'])
def tobs(type):
    session = Session(engine)
    max_date = session.query(func.max(Measurement.date)).first()
    maxdate = dt.datetime.strptime(str(max_date[0]), "%Y-%m-%d")
    #Use relative data to get the last 12 months from the date of the max date
    last_12_months = maxdate + relativedelta(months=-12)
    results = session.query(Measurement.date, Measurement.tobs).filter(and_(Measurement.date>=last_12_months, Measurement.date <= maxdate)).all()
    session.close()
    all_measurements = []
    # format into JSON
    for date, tobs in results:
        measurement_dict = {}
        measurement_dict['Date'] = date
        measurement_dict['Precipitation'] = tobs
        all_measurements.append(measurement_dict)
    
    if type == "inline":
        return render_template('index.html', json_content=all_measurements, message_type="Success", message_content="Success! Returning the last 12 months Total Observed Temperature data")
    elif type == "raw":
        return jsonify(all_measurements)
    else:
        abort(404)

@app.route("/api/v1.0/<type>/<start>", methods=['GET', 'POST'])
def stats_start(type, start):
    session = Session(engine)
    try:
        start_date = dt.datetime.strptime(str(start), "%Y%m%d")
    except:
        abort(400)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start_date).all()
    session.close()
    all_measurements = {
                'Start Date' : start_date.strftime("%Y-%m-%d"),
                'Minimum Temperature' : results[0][0],
                'Average Temperature' : results[0][1],
                'Maximum Temperature' : results[0][2]
        }
    if type == "inline":
        return render_template('index.html', json_content=all_measurements, message_type="Success", message_content=f"Success! Returning the Temperature Observations since {start_date.strftime('%Y-%m-%d')}")
    elif type == "raw":
        return jsonify(all_measurements)
    else:
        abort(404)


@app.route("/api/v1.0/<type>/<start>/<end>", methods=['GET', 'POST'])
def stats_start_end(type, start, end):
    session = Session(engine)
    try:
        start_date = dt.datetime.strptime(str(start), "%Y%m%d")
        end_date = dt.datetime.strptime(str(end), "%Y%m%d")
    except:
        abort(400)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(and_(Measurement.date>=start_date, Measurement.date<=end_date)).all()
    session.close()
    all_measurements = {
                'Start Date' : start_date.strftime("%Y-%m-%d"),
                'End Date' : end_date.strftime("%Y-%m-%d"),
                'Minimum Temperature' : results[0][0],
                'Average Temperature' : results[0][1],
                'Maximum Temperature' : results[0][2]
        }
    if type == "inline":
        return render_template('index.html', json_content=all_measurements, message_type="Success", message_content=f"Success! Returning the Temperature Observations between the dates {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}")
    elif type == "raw":
        return jsonify(all_measurements)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)
# end flask app