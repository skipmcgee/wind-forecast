from markupsafe import Markup
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

entities_list = ['models', 'locations', 'sensors', 'forecasts', 'readings', ] 

# Routes 
@app.route('/')
def root():
    models_query = "SELECT * FROM Models;"
    locations_query = "SELECT * FROM Locations;"
    sensors_query = "SELECT * FROM Sensors;"

    models_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()
    locations_results = db.execute_query(db_connection=db_connection, query=locations_query).fetchall()
    sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
    
    return render_template("main.j2", models=models_results, locations=locations_results, sensors=sensors_results,)

@app.route('/results')
def result_info(from_date, to_date, sensor):
    forecasts_query = "SELECT * FROM Forecasts;"
    readings_query = "SELECT * FROM Readings;"
    forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()
    readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

    return render_template("results.j2", forecasts=forecasts_results, readings=readings_results)

@app.route('/editsensors')
def edit_sensors():
    edit_sensor_query = f"SELECT * FROM Sensors;"
    edit_sensor_results = db.execute_query(db_connection=db_connection, query=edit_sensor_query).fetchall()
    return render_template("editsensors.j2", model_string=edit_sensor_results)

@app.route('/editlocations')
def edit_locations():
    edit_loc_query = f"SELECT * FROM Locations;"
    edit_loc_results = db.execute_query(db_connection=db_connection, query=edit_loc_query).fetchall()
    return render_template("editsensors.j2", model_string=edit_loc_results)

    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)