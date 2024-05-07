from markupsafe import Markup
from flask import Flask, render_template, json, request, redirect
from flask_mysqldb import MySQL
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

entities_list = ['models', 'locations', 'sensors', 'forecasts', 'readings', ] 

# Routes 
@app.route('/', methods=["POST", "GET"])
def root():
    if request.method == "GET":
        models_query = "SELECT * FROM Models;"
        locations_query = "SELECT * FROM Locations;"
        sensors_query = "SELECT * FROM Sensors;"
        models_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()
        locations_results = db.execute_query(db_connection=db_connection, query=locations_query).fetchall()
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        
        return render_template("main.j2", models=models_results, locations=locations_results, sensors=sensors_results,)
    elif request.method == "POST":
        # set vars:
        from_date = ''
        to_date = ''
        sensor = ''
        return redirect("/results", from_date=from_date, to_date=to_date, sensor=sensor)

@app.route('/results', methods=["GET"])
def result_info(from_date, to_date, sensor):
    forecasts_query = "SELECT * FROM Forecasts;"
    readings_query = "SELECT * FROM Readings;"
    forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()
    readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

    return render_template("results.j2", forecasts=forecasts_results, readings=readings_results)

@app.route('/editsensors', methods=["POST", "GET"])
def edit_sensors():
    if request.method == "GET":
        edit_sensor_query = f"SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationAltitude FROM Sensors\n JOIN Locations ON Sensors.sensorLocationID = Locations.locationID\n ORDER BY sensorName DESC;"
        edit_sensor_obj = db.execute_query(db_connection=db_connection, query=edit_sensor_query)
        edit_sensor_results = edit_sensor_obj.fetchall()
        print(edit_sensor_results)
        return render_template("editsensors.j2", sensors=edit_sensor_results)
    elif request.method == "POST":
        # sql commands to update or add
        return redirect("/")
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)