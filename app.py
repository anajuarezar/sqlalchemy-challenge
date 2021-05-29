#################################################
# Step 2 - Climate App
#################################################

# We import our dependancies 

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

# We use reflect to automap the tables
Base = automap_base()

Base.prepare(engine, reflect=True)

# Save the tables
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

# Our first route is the home page, where we will display the available routes
@app.route("/")
def home():
    """Here you can find al the available routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Our second route is precipitation
# We begin this route with the standard code of naming the route
# We proceed with opening the session and creating our query

@app.route("/api/v1.0/precipitation")
def precipitations():
    # Create our session so we can query out DB
    session = Session(engine)
    prec = session.query(Measurement.prcp, Measurement.date).group_by(Measurement.date).all()

    # We create an empty dictionary where we will append the result of the loop
    precip_dict = {}
    for prcp, date in prec:
        precip_dict[date] = prcp

   # We close the session. 
    session.close()

    # We jsonify the results so we can display it. 
    return jsonify(precip_dict)


    

# The next app follows a similar code. 
@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session again.
    session = Session(engine)

    # Query all passengers
    results = session.query(Station.name).all()

    #We create a dictionary from the row data and append to a list
    station_names = []
    for stations in results:
        station_names.append(stations[0])
    
    
    # We append the list to the dictionary
    station_dict = {'name': station_names}


    #We close our session so we can continue working with it
    session.close()

    #We use jsonify so we can show the result of our query
    return jsonify(station_dict)


# We follow the same initial steps.
@app.route("/api/v1.0/tobs")
def tobs():
    
    #We create our session. 
    session = Session(engine)

    results_tobs = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date>"2016-08-23").\
        group_by(Measurement.date).all()

    #We follow a similar procedure with the dictionary
    tobs_dict = []
    for  each in results_tobs:
        tobs_dict.append(each[0])

    session.close()

    return jsonify(tobs_dict)



#We follow the same initial code
@app.route("/api/v1.0/<start>")
def start(start):
    # We create the session and query
    session = Session(engine)

    # Here we save all the functions we are goint to use using FUNC
    request = [Measurement.date, func.min(Measurement.tobs),
    func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    # We query using the functions we saved.
    results_min = session.query(*request).\
        filter(Measurement.date>start).all()

    # We create the list that will cointain a dictinary with the results of the query
    compilation = []
    for each in results_min:
        compilation.append({'date': each[0], 'TMIN': each[1], 'TMAX': each[2], 'TAVG': each[3]})

    session.close()

    return jsonify(compilation)


# Here we use a similar procedure, except we have two parameters. 
@app.route("/api/v1.0/<start>/<end>")
def between(first=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    end_start_req = [Measurement.date, func.min(Measurement.tobs),
    func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    results_between = session.query(*end_start_req).\
        filter(Measurement.date >= first, Measurement.date <= end).all()

    compilation_end = []
    for each in results_between:
        compilation_end.append({'date': each[0], 'TMIN': each[1], 'TMAX': each[2], 'TAVG': each[3]})

    session.close()

    return jsonify(compilation_end)




    


#################################################
# Debug
#################################################

# We use debug to prevent the app from stop in case
# of an error or bug
if __name__ == '__main__':
    app.run(debug=True)
