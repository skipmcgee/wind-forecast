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
    forecasts_query = "SELECT * FROM Forecasts;"
    readings_query = "SELECT * FROM Readings;"

    models_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()
    locations_results = db.execute_query(db_connection=db_connection, query=locations_query).fetchall()
    sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
    forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()
    readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

    return render_template("main.j2", models=models_results, locations=locations_results, sensors=sensors_results, forecasts=forecasts_results, readings=readings_results)
'''
@app.route('/edit')
def edit(model_string):
    edit_query = f"SELECT * FROM {model_string};"
    edit_results = db.execute_query(db_connection=db_connection, query=edit_query).fetchall()
    return render_template("edit.j2", model_string=edit_results)

@app.route('/update')
def update():
#    edit_query = f"SELECT * FROM {model_string};"
#    edit_results = db.execute_query(db_connection=db_connection, query=edit_query).fetchall()
    return render_template("update.j2")

@app.route('/add')
def add():
#    edit_query = f"SELECT * FROM {model_string};"
#    edit_results = db.execute_query(db_connection=db_connection, query=edit_query).fetchall()
    return render_template("add.j2")
'''
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)