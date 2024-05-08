import logging
from markupsafe import Markup
from flask import Flask, render_template, json, request, redirect, flash
from flask_mysqldb import MySQL
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()
logger = logging.getLogger('werkzeug')
entities_list = ['models', 'locations', 'sensors', 'forecasts', 'readings', ] 
info_dict = dict()

# Routes 
@app.route('/', methods=["POST", "GET"])
def root():
    if request.method == "GET":
        sensors_query = "SELECT * FROM Sensors;"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        return render_template("index.j2", sensors=sensors_results,)
    elif request.method == "POST":
        info_dict['fromdate'] = request.form['fromdate']
        info_dict['todate'] = request.form['todate']
        info_dict['sensorlist'] = request.form['sensorlist']
        logger.info(str(info_dict))
        return redirect("/results", )

@app.route('/results', methods=["GET"])
def results():
    forecasts_query = f"SELECT * FROM Forecasts\nJOIN Models ON Forecasts.forecastModelID = Models.modelID\nJOIN Locations ON Forecasts.forecastLocationID = Locations.locationID\nWHERE\nforecastForDateTime BETWEEN {info_dict['todate']} AND {info_dict['fromdate']}\nAND\nLocations.locationID = {info_dict['sensorlist']};"
    readings_query = f"SELECT * FROM Readings\nJOIN Sensors ON Readings.readingSensorID = Sensors.sensorID\nJOIN Dates ON Readings.readingDateID = Dates.dateID\nWHERE \ndateDateTime BETWEEN {info_dict['todate']} AND {info_dict['fromdate']}\nAND\nsensorLocationID = {info_dict['sensorlist']};"
    forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()
    readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

    return render_template("results.j2", forecasts=forecasts_results, readings=readings_results)

@app.route('/library', methods=["POST", "GET"])
def library():
    if request.method == "GET":
        edit_sensor_query = f"SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationAltitude FROM Sensors\n JOIN Locations ON Sensors.sensorLocationID = Locations.locationID\n ORDER BY sensorName DESC;"
        edit_sensor_obj = db.execute_query(db_connection=db_connection, query=edit_sensor_query)
        edit_sensor_results = edit_sensor_obj.fetchall()
        print(edit_sensor_results)
        return render_template("library.j2", sensors=edit_sensor_results)
    elif request.method == "POST":
        # sql commands to update or add
        return redirect("/")
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)