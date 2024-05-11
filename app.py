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
        return redirect("/results", info_dict=info_dict)

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
        sensor_query = f"SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationAltitude FROM Sensors\n JOIN Locations ON Sensors.sensorLocationID = Locations.locationID\n ORDER BY sensorName DESC;"
        sensor_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        sensor_results = sensor_obj.fetchall()
        #print(edit_sensor_results)
        model_query = f"SELECT * FROM Models\n ORDER BY modelName DESC;"
        model_obj = db.execute_query(db_connection=db_connection, query=model_query)
        model_results = model_obj.fetchall()
        return render_template("library.html", sensors=sensor_results, models=model_results)
    elif request.method == "POST":
        # sql commands to update or add
        return redirect("/")

@app.route("/delete/sensor/<int:sensorID>", methods=["POST", "GET"])
def deletesensor(sensorID):
    sensor_query = f"DELETE FROM Sensors\nWHERE sensorID={sensorID};"
    query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)

    return redirect("/library")

@app.route("/delete/model/<int:modelID>", methods=["POST", "GET"])
def deletemodel(modelID):
    logger.info(modelID)
    model_query = f"DELETE FROM Models\nWHERE modelID={modelID};"
    query_obj = db.execute_query(db_connection=db_connection, query=model_query)

    return redirect("/library")

@app.route("/edit/sensor/<int:sensorID>", methods=["POST", "GET"])
def sensoredit(sensorID):
    if request.method == "GET":
        sensor_query = f"SELECT * FROM Sensors\nJOIN Locations ON Sensors.sensorLocationID = Locations.locationID\nWHERE Sensors.sensorID = {sensorID};"
        query_results = db.execute_query(db_connection=db_connection, query=sensor_query).fetchall()
        logger.info(query_results)
        return render_template("editsensor.html", specific_sensor=query_results)
    
    elif request.method == "POST":
        logger.info(sensorID)
        logger.info(str(request.form))
        sensor_query = f"UPDATE Sensors\nSET `sensorName`='{request.form['sensorName']}', `sensorAPIKey`='{request.form['sensorAPIKey']}', `sensorNumber`='{request.form['sensorNumber']}', `sensorLocationID`='{request.form['sensorLocationID']}',\nWHERE Sensors.sensorID = {sensorID};"
        query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        id_sensor_query = f"SELECT sensorLocationID FROM Sensors\n WHERE Sensors.sensorID = {sensorID};"
        _sensorLocationID = db.execute_query(db_connection=db_connection, query=sensor_query).fetchall()
        location_query = f"UPDATE Locations\nSET `locationName`='{request.form['locationName']}', `locationLatitude`='{request.form['locationLatitude']}', `locationLongitude`='{request.form['locationLongitude']}', `locationAltitude`='{request.form['locationAltitude']}',\nWHERE Locations.locationID = {_sensorLocationID};"
        location_obj = db.execute_query(db_connection=db_connection, query=location_query)

        return redirect("/library")

@app.route("/edit/model/<int:modelID>", methods=["POST", "GET"])
def modeledit(modelID):
    if request.method == "GET":
        models_query = f"SELECT * FROM Models\nWHERE Models.modelID = {modelID};"
        query_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()
        logger.info(query_results)
        return render_template("editmodel.html", specific_model=query_results)
    
    elif request.method == "POST":
        logger.info(f"updating name for {request.form['modelID']} to: {request.form['modelName']}")
        model_query = f"UPDATE Models\nSET `modelName`='{request.form['modelName']}'\nWHERE Models.modelID = {modelID};"
        query_obj = db.execute_query(db_connection=db_connection, query=model_query)

        return redirect("/library")

@app.route("/add/sensor", methods=["POST", "GET",])
def addsensor():
    if request.method == "GET":
        return render_template("addsensor.html")

    elif request.method == "POST":
        logger.info(str(request.form))
        location_query = f"INSERT INTO Locations (`locationName`, `locationLatitude`, `locationLongitude`, `locationAltitude`,)\nVALUES ({request.form['locationName']}, {request.form['locationLatitude']}, {request.form['locationLongitude']}, {request.form['locationAltitude']},);"
        location_obj = db.execute_query(db_connection=db_connection, query=location_query)
        sensor_query = f"INSERT INTO Sensors (`sensorName`, `sensorAPIKey`, `sensorNumber`, `sensorLocationID`,)\nVALUES ({request.form['sensorName']}, {request.form['sensorAPIKey']}, {request.form['sensorNumber']}, {request.form['sensorLocationID']},);"
        query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        return redirect("/library")

@app.route("/add/model", methods=["POST", "GET",])
def addmodel():
    if request.method == "GET":
        return render_template("addmodel.html")
    elif request.method == "POST":
        logger.info(str(request.form))
        model_update = f"INSERT INTO `Models` (modelName)\n VALUES ('{request.form['modelName'].upper()}');"
        model_obj = db.execute_query(db_connection=db_connection, query=model_update)
        return redirect("/library")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)