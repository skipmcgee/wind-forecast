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
editsensor = dict()

# Routes 
@app.route("/index")
def plain_index():
    return redirect("/")

@app.route("/index.html")
def dot_index():
    return redirect("/")

@app.route('/', methods=["POST", "GET"])
def root():
    if request.method == "GET":
        sensors_query = "SELECT * FROM Sensors;"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        return render_template("index.html", sensors=sensors_results,)
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

    return render_template("results.html", forecasts=forecasts_results, readings=readings_results)

@app.route('/library', methods=["POST", "GET"])
def library():
    if request.method == "GET":
        edit_sensor_query = f"SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationAltitude FROM Sensors\n JOIN Locations ON Sensors.sensorLocationID = Locations.locationID\n ORDER BY sensorName DESC;"
        edit_sensor_obj = db.execute_query(db_connection=db_connection, query=edit_sensor_query)
        edit_sensor_results = edit_sensor_obj.fetchall()
        print(edit_sensor_results)
        return render_template("library.html", sensors=edit_sensor_results)
    elif request.method == "POST":
        # sql commands to update or add
        return redirect("/")

@app.route("/delete/<int:sensorID>", methods=["POST",])
def delete(sensorID):
    sensor_query = f"DELETE FROM Sensors\nWHERE sensorID={sensorID};"
    query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)

    return redirect("/library")

@app.route("/edit/<int:sensorID>", methods=["POST", "GET"])
def sensoredit(sensorID):
    if request.method == "GET":
        sensor_query = f"SELECT * FROM Sensors\nJOIN Locations ON Sensors.sensorLocationID = Locations.locationID\nWHERE Sensors.sensorID = {sensorID};"
        query_results = db.execute_query(db_connection=db_connection, query=sensor_query).fetchall()
        logger.info(query_results)
        return render_template("edit.html", specific_sensor=query_results)
    
    elif request.method == "Post":
        logger.info(sensorID)
        logger.info(str(editsensor))
        sensor_query = f"UPDATE Sensors\nSET `sensorName` = {editsensor['sensorName']}, `sensorAPIKey` = {editsensor['sensorAPIKey']}, `sensorNumber` = {editsensor['sensorNumber']}, `sensorLocationID` = {editsensor['sensorLocationID']},\nWHERE `sensorID` = {sensorID};"
        query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        location_query = f"UPDATE Locations\nSET `locationName`={editsensor['locationName']}, `locationLatitude`={editsensor['locationLatitude']}, `locationLongitude`={editsensor['locationLongitude']}, `locationAltitude`={editsensor['locationAltitude']},\nWHERE `locationID`=_locationID;"
        location_obj = db.execute_query(db_connection=db_connection, query=location_query)

        return redirect("/library")

@app.route("/add", methods=["POST", "GET",])
def addsensor():
    if request.method == "GET":
        return render_template("add.html")

    elif request.method == "POST":
        logger.info(str(request.form))
        location_query = f"INSERT INTO Locations (`locationName`, `locationLatitude`, `locationLongitude`, `locationAltitude`,)\nVALUES ({request.form['locationName']}, {request.form['locationLatitude']}, {request.form['locationLongitude']}, {request.form['locationAltitude']},);"
        location_obj = db.execute_query(db_connection=db_connection, query=location_query)
        sensor_query = f"INSERT INTO Sensors (`sensorName`, `sensorAPIKey`, `sensorNumber`, `sensorLocationID`,)\nVALUES ({request.form['sensorName']}, {request.form['sensorAPIKey']}, {request.form['sensorNumber']}, {request.form['sensorLocationID']},);"
        query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        return redirect("/library")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)