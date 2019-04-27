import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station= Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def dates_precipitation():
    """Return a list of dates and precipitation"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))

    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all passengers
    results2 = session.query(Station.station, Station.name).all()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))

    return jsonify(results2)

@app.route("/api/v1.0/tobs")
def temperatures():
    """Return a list of temperatures"""
    # Query all passengers
    results3 = session.query(Measurement.tobs).filter(Measurement.date>'2016-08-23').all()

    # Convert list of tuples into normal list
    all_temp = list(np.ravel(results3))

    return jsonify(all_temp)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def findtemperatures(start, end='2019-01-01'):
    """Return a list of temperatures based on dates"""
    # Query all passengers
    print(start)
    print(end)

    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    results4 = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results4))
    return jsonify(results4)




if __name__ == '__main__':
    app.run(debug=True)
