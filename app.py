#################################################
# Step 2 - Climate App
#################################################

# We import our dependancies 
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# We create our engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

# We create our app using __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# We create our routes 
@app.route("/")
def home():
    """Here you can find al the available routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prec = session.query(Measurement.prcp, Measurement.date).group_by(Measurement.date).all()

    precip_dict = {}

    for prcp, date in prec:
        precip_dict[date] = prcp

    session.close()

    return jsonify(precip_dict)


    


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Station.station).all()

    #We create a dictionary from the row data and append to a list
    station_names = []
    for stations in results:
        station_names.append(stations[0])
    
    
    # We append the list to the dictionary
    station_dict = {'name': station_names}

    #We use jsonify so we can show the result of our query
    

    #We close our session so we can continue working with it

    session.close()

    return jsonify(station_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #We follow a similar procedure with the dictionary
    tobs = []

    session.close()



#################################################
# Debug
#################################################

# We use debug to prevent the app from stop in case
# of an error or bug
if __name__ == '__main__':
    app.run(debug=True)
