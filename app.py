#!/bin/env python3
import logging
from markupsafe import Markup, escape
from flask import Flask, render_template, json, request, redirect, flash, url_for
from flask_mysqldb import MySQL
import os
import database.db_connector as db
from datetime import date, datetime, timedelta
import asyncio
import pprint as pp

# local imports
from app.openmeteo_ecmwf_query import query_ecmwf
from app.openmeteo_gfs_query import query_gfs
from app.holfuy_query import fetch, gather_data
from app.data import KeyTranslation

# Configuration
app = Flask(__name__)
app.secret_key = 'mc)kNIk4cbIZQ,@jUve-Q}2^T3em$p'
db_connection = db.connect_to_database()
logger = logging.getLogger('werkzeug')
keys = KeyTranslation()
entities_list = ['models', 'locations', 'sensors', 'forecasts', 'readings', ] 
valid_models_list = ['HRRR', 'ECMWF', 'MBLUE', 'GFS', 'NAM', 'ICON', ]
current_supported_model_list = ['ECMWF', 'GFS']
current_supported_sensor_list = ['1',]
info_dict = dict()
DEBUG = True

############
# Routes
############

@app.route("/index")
def plain_index():
    return redirect("/")

@app.route("/index.html")
def dot_index():
    return redirect("/")

@app.route('/', methods=["POST", "GET"])
def root():
    '''View for the website index'''

    today = date.today()
    if request.method == "GET":
        sensors_query = "SELECT * FROM Sensors;"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        return render_template("pages/index.html", sensors=sensors_results, today=str(today))
    elif request.method == "POST":
        if DEBUG:
            logger.info(f"today: {today}, fromdate: {request.form['fromdate']}, todate: {request.form['todate']}")
        to_date_obj = datetime.strptime(request.form['todate'], '%Y-%m-%d').date()
        from_date_obj = datetime.strptime(request.form['fromdate'], '%Y-%m-%d').date()
        # validation 1) fromdate needs to be before todate
        if to_date_obj > today:
            flash("The To Date cannot be in the future!")
            return redirect("/")
        # validation 2) todate can't be later than today
        elif from_date_obj > to_date_obj:
            flash("The From Date cannot be greater than the To Date!")
            return redirect("/")
        # validation 3) from and to dates cannot be equal
        elif from_date_obj == to_date_obj:
            flash("The From Date cannot be equal to the To Date!")
            return redirect("/")
        sensors_query = f"SELECT sensorName FROM Sensors\n WHERE sensorID='{request.form['sensorlist']}';"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        info_dict['fromdate'] = request.form['fromdate']
        info_dict['todate'] = request.form['todate']
        info_dict['sensorlist'] = request.form['sensorlist']
        info_dict['sensorName'] = sensors_results[0]['sensorName']
        logger.info("found info dict: " + str(info_dict))
        return redirect("/results")

@app.route('/results', methods=["GET"])
def results():
    if DEBUG:
        logger.info("results info_dict: " + str(info_dict))
    if len(info_dict) == 0:
        logger.error("results info_dict was not created when resource was requested")
        return redirect("/")
    forecasts_query = f"SELECT forecastID, forecastForDateTime, forecastDateID, forecastTemperature2m, forecastPrecipitation, forecastWeatherCode, forecastPressureMSL, forecastWindSpeed10m, forecastWindDirection10m, forecastCape FROM Forecasts\nJOIN Models ON Forecasts.forecastModelID = Models.modelID\nJOIN Locations ON Forecasts.forecastLocationID = Locations.locationID\nWHERE ( forecastForDateTime BETWEEN '{info_dict['fromdate']}' AND '{info_dict['todate']}' ) AND ( Locations.locationID='{info_dict['sensorlist']}' );"
    if DEBUG:
        logger.info("results forecasts query: " + forecasts_query)
    forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()
    readings_query = f"SELECT readingID, readingSensorID, readingDateID, readingWindSpeed, readingWindGust, readingWindMin, readingWindDirection, readingTemperature FROM Readings\nJOIN Sensors ON Readings.readingSensorID = Sensors.sensorID\nJOIN Dates ON Readings.readingDateID = Dates.dateID\nWHERE ( dateDateTime BETWEEN '{info_dict['fromdate']}' AND '{info_dict['todate']}' ) AND ( Sensors.sensorLocationID='{info_dict['sensorlist']}' );"
    if DEBUG:
        logger.info("results readings query: " + readings_query)
    readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

    return render_template("results.html", forecasts=forecasts_results, readings=readings_results, info_dict=info_dict, key_dict=keys.key_dict)

@app.route('/library', methods=["POST", "GET"])
def library():
    if request.method == "GET":
        sensor_query = f"SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationName FROM Sensors\n JOIN Locations ON Sensors.sensorLocationID = Locations.locationID\n ORDER BY sensorName DESC;"
        sensor_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        sensor_results = sensor_obj.fetchall()
        if DEBUG:
            logger.info(sensor_results)
        model_query = f"SELECT * FROM Models\n ORDER BY modelName DESC;"
        model_obj = db.execute_query(db_connection=db_connection, query=model_query)
        model_results = model_obj.fetchall()
        if DEBUG:
            logger.info(model_results)
        locations_query = f"SELECT * FROM Locations\n ORDER BY locationName DESC;"
        locations_obj = db.execute_query(db_connection=db_connection, query=locations_query)
        locations_results = locations_obj.fetchall()
        if DEBUG:
            logger.info(locations_results)
        return render_template("library.html", sensors=sensor_results, models=model_results, locations=locations_results, key_dict=keys.key_dict)
    elif request.method == "POST":
        return redirect("/")

############
# Create
############

@app.route('/add/forecast', methods=['POST', 'GET'])
def add_forecast():
    '''API Route to add a forecast'''

    if request.method == 'GET':

        models_query = '''
        SELECT
            modelID, 
            modelName
        FROM
            Models;
        '''
        models_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()

        locations_query = '''
        SELECT
            locationID, 
            locationName
        FROM
            Locations;
        '''
        locations_results = db.execute_query(db_connection=db_connection, query=locations_query).fetchall()

        dates_query = '''
        SELECT
            dateID, 
            dateDateTime
        FROM
            Dates;
        '''
        dates_results = db.execute_query(db_connection=db_connection, query=dates_query).fetchall()

        return render_template('add/addforecast.html', models=models_results, locations=locations_results, dates=dates_results)
    
    elif request.method == 'POST':

        query_params = {
            'forecastForDateTime': request.form.get('forecastForDateTime'), 
            'forecastDateID': request.form.get('dateID'), 
            'forecastTemperature2m': request.form.get('forecastTemperature'), 
            'forecastPrecipitation': request.form.get('forecastPrecipitation'), 
            'forecastWeatherCode': request.form.get('forecastWeatherCode'), 
            'forecastPressureMSL': request.form.get('forecastPressureMSL'), 
            'forecastWindSpeed10m': request.form.get('forecastWindSpeed'), 
            'forecastWindDirection10m': request.form.get('forecastWindDirection'), 
            'forecastCape': request.form.get('forecastCape'), 
            'forecastLocationID': request.form.get('locationID'),
            'forecastModelID': request.form.get('modelID')
        }

        # Check for Null modelID
        if request.form.get('modelID') is None:
            print('ModelID is None')
            forecasts_query = '''
                INSERT INTO 
                    `Forecasts` (
                        forecastForDateTime, 
                        forecastDateID, 
                        forecastTemperature2m, 
                        forecastPrecipitation, 
                        forecastWeatherCode, 
                        forecastPressureMSL, 
                        forecastWindSpeed10m, 
                        forecastWindDirection10m, 
                        forecastCape, 
                        forecastLocationID
                    )
                VALUES 
                    (
                        %(forecastForDateTime)s, 
                        %(forecastDateID)s, 
                        %(forecastTemperature2m)s, 
                        %(forecastPrecipitation)s, 
                        %(forecastWeatherCode)s, 
                        %(forecastPressureMSL)s, 
                        %(forecastWindSpeed10m)s, 
                        %(forecastWindDirection10m)s, 
                        %(forecastCape)s, 
                        %(forecastLocationID)s
                    );
            '''

            db.execute_query(db_connection=db_connection, query=forecasts_query, query_params=query_params)
        
        else:
            forecasts_query = '''
                INSERT INTO 
                    `Forecasts` (
                        forecastForDateTime, 
                        forecastDateID, 
                        forecastTemperature2m, 
                        forecastPrecipitation, 
                        forecastWeatherCode, 
                        forecastPressureMSL, 
                        forecastWindSpeed10m, 
                        forecastWindDirection10m, 
                        forecastCape, 
                        forecastLocationID,
                        forecastModelID
                    )
                VALUES 
                    (
                        %(forecastForDateTime)s, 
                        %(forecastDateID)s, 
                        %(forecastTemperature2m)s, 
                        %(forecastPrecipitation)s, 
                        %(forecastWeatherCode)s, 
                        %(forecastPressureMSL)s, 
                        %(forecastWindSpeed10m)s, 
                        %(forecastWindDirection10m)s, 
                        %(forecastCape)s, 
                        %(forecastLocationID)s,
                        %(forecastModelID)s
                    );
                '''
            db.execute_query(db_connection=db_connection, query=forecasts_query, query_params=query_params)

        return redirect('/forecasts')

@app.route("/add/location", methods=["POST", "GET",])
def add_location():
    '''API Route to add a location'''

    if request.method == "GET":
        return render_template("add/addlocation.html")

    elif request.method == "POST":
        if DEBUG:
            logger.info(str(request.form))
        location_query = f"INSERT INTO Locations (`locationName`, `locationLatitude`, `locationLongitude`, `locationAltitude`,)\nVALUES ({request.form['locationName']}, {request.form['locationLatitude']}, {request.form['locationLongitude']}, {request.form['locationAltitude']},);"
        if DEBUG: 
            logger.info("add sensor post first query: " + location_query)
        location_obj = db.execute_query(db_connection=db_connection, query=location_query)
        return redirect("/locations")


@app.route("/add/sensor", methods=["POST", "GET",])
def add_sensor():
    '''API Route to add a sensor'''

    if request.method == "GET":
        return render_template("add/addsensor.html")

    elif request.method == "POST":

        if DEBUG:
            logger.info(str(request.form))

        location_query = f"INSERT INTO Locations (`locationName`, `locationLatitude`, `locationLongitude`, `locationAltitude`,)\nVALUES ({request.form['locationName']}, {request.form['locationLatitude']}, {request.form['locationLongitude']}, {request.form['locationAltitude']},);"
        
        if DEBUG: 
            logger.info("add sensor post first query: " + location_query)

        db.execute_query(db_connection=db_connection, query=location_query)
        sensor_query = f"INSERT INTO Sensors (`sensorName`, `sensorAPIKey`, `sensorNumber`, `sensorLocationID`,)\nVALUES ({request.form['sensorName']}, {request.form['sensorAPIKey']}, {request.form['sensorNumber']}, {request.form['sensorLocationID']},);"
        
        if DEBUG:
            logger.info("add sensor post second query: " + sensor_query)

        db.execute_query(db_connection=db_connection, query=sensor_query)

        return redirect("/sensors")

@app.route("/add/model", methods=["POST", "GET",])
def add_model():
    '''API Route to add a model'''

    if request.method == "GET":
        return render_template("add/addmodel.html")
    
    elif request.method == "POST":
        if DEBUG:
            logger.info("add model post: " + request.form['modelName'].upper())
        if request.form['modelName'].upper() not in valid_models_list:
            flash("Not a recognized Weather Model!")
            return render_template("add/model.html")
        model_update = f"INSERT INTO `Models` (modelName)\n VALUES ('{request.form['modelName'].upper()}');"
        if DEBUG:
            logger.info("add model post query: " + model_update)
        model_obj = db.execute_query(db_connection=db_connection, query=model_update)
        return redirect("/models")
    
@app.route("/add/date", methods=["POST", "GET",])
def add_date():
    '''API Route to add a date'''

    if request.method == "GET":
        return render_template("add/date.html")

    elif request.method == "POST":
        if DEBUG:
            logger.info(str(request.form))
        date_query = f"INSERT INTO Dates (`dateDateTime`)\n VALUES ('{request.form['dateDateTime']}');"
        if DEBUG: 
            logger.info("add date post first query: " + date_query)
        date_obj = db.execute_query(db_connection=db_connection, query=date_query)
        return redirect("/dates")

@app.route('/add/reading', methods=["POST", "GET"])
def add_reading():
    '''API Route to add a reading'''

    if request.method == "GET":
        sensors_query = "SELECT * FROM Sensors;"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        return render_template("add/addreading.html", sensors=sensors_results)
    
    elif request.method == "POST":
        use_sensorID = request.form['sensorlist']
        if DEBUG:
            logger.info("add reading post for sensor: " + use_sensorID)
        if use_sensorID not in current_supported_sensor_list:
            flash("This sensor is not currently supported for MVP!")
            return redirect("/add/reading")
        valid_obj_list,error_obj_list = asyncio.run(gather_data())
        if DEBUG:
            for sensor_obj in valid_obj_list:
                pp.pprint(sensor_obj)
            for error_obj in error_obj_list:
                pp.pprint(error_obj)
        # check for errors
        for sensor_obj in valid_obj_list:
            if "error" in sensor_obj.keys():
                flash("Error accessing Holfuy API")
                return redirect("/")
        now = datetime.now()
        date_format = "%Y-%m-%d %H:%M:%S"
        datetime_str = now.strftime(date_format)
        old_date = now - timedelta(hours=1)
        new_date = now + timedelta(hours=1)
        new_date_str = new_date.strftime(date_format)
        old_date_str = old_date.strftime(date_format)
        date_insert = f"INSERT INTO Dates (`dateDateTime`)\n VALUES ('{datetime_str}');"
        date_results = db.execute_query(db_connection=db_connection, query=date_insert).fetchall()
        date_get_id = f"SELECT `dateID` FROM Dates\n WHERE `dateDateTime`='{datetime_str}';"
        date_id_results = db.execute_query(db_connection=db_connection, query=date_get_id).fetchall()
        if DEBUG:
            logger.info("date results: " + str(date_id_results))
        add_reading_query = f"INSERT INTO Readings (`readingSensorID`, `readingWindSpeed`, `readingWindGust`, `readingWindMin`, `readingWindDirection`, `readingTemperature`, `readingDateID`)\n VALUES "
        for sensor_obj in valid_obj_list:
            add_reading_query += f"\n('{use_sensorID}', '{sensor_obj['wind']['speed']}', '{sensor_obj['wind']['gust']}', '{sensor_obj['wind']['min']}', '{sensor_obj['wind']['direction']}', '{sensor_obj['temperature']}', '{date_id_results[0]['dateID']}')"
        add_reading_query += ";"
        reading_obj = db.execute_query(db_connection=db_connection, query=add_reading_query)
        info_dict['fromdate'] = old_date_str
        info_dict['todate'] = new_date_str
        info_dict['sensorlist'] = request.form['sensorlist']
        sensors_query = f"SELECT sensorName FROM Sensors\n WHERE sensorID='{request.form['sensorlist']}';"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        info_dict['sensorName'] = sensors_results[0]['sensorName']
        
        forecasts_query = f"SELECT forecastID, forecastForDateTime, forecastDateID, forecastTemperature2m, forecastPrecipitation, forecastWeatherCode, forecastPressureMSL, forecastWindSpeed10m, forecastWindDirection10m, forecastCape FROM Forecasts\nJOIN Models ON Forecasts.forecastModelID = Models.modelID\nJOIN Locations ON Forecasts.forecastLocationID = Locations.locationID\nWHERE ( forecastForDateTime BETWEEN '{info_dict['fromdate']}' AND '{info_dict['todate']}' ) AND ( Locations.locationID='{info_dict['sensorlist']}' );"
        if DEBUG:
            logger.info("results forecasts query: " + forecasts_query)
        forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()
        readings_query = f"SELECT readingID, readingSensorID, readingDateID, readingWindSpeed, readingWindGust, readingWindMin, readingWindDirection, readingTemperature FROM Readings\nJOIN Sensors ON Readings.readingSensorID = Sensors.sensorID\nJOIN Dates ON Readings.readingDateID = Dates.dateID\nWHERE ( dateDateTime BETWEEN '{info_dict['fromdate']}' AND '{info_dict['todate']}' ) AND ( Sensors.sensorLocationID='{info_dict['sensorlist']}' );"
        if DEBUG:
            logger.info("results readings query: " + readings_query)
        readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

        return render_template("results.html", forecasts=forecasts_results, readings=readings_results, info_dict=info_dict)

############
# Read
############

@app.route('/forecasts', methods=['GET'])
def forecasts():
    '''View for the Forecasts Admin Page'''

    forecasts_query = '''
    SELECT 
        Forecasts.forecastID,
        Dates.dateDateTime,
        Forecasts.forecastTemperature2m,
        Forecasts.forecastPrecipitation,
        Forecasts.forecastWeatherCode,
        Forecasts.forecastPressureMSL,
        Forecasts.forecastWindSpeed10m,
        Forecasts.forecastWindDirection10m,
        Forecasts.forecastCape,
        Models.modelName,
        Locations.locationName,
        Forecasts.forecastForDateTime
    FROM 
        Forecasts
    LEFT JOIN 
        Models ON Forecasts.forecastModelID = Models.modelID
    JOIN 
        Locations ON Forecasts.forecastLocationID = Locations.locationID
    JOIN 
        Dates ON Forecasts.forecastDateID = Dates.dateID;
    '''

    forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()

    if DEBUG:
        logger.info(forecasts_results)

    return render_template('pages/forecasts.html', forecasts=forecasts_results, forecast_dict=keys.key_dict)

@app.route('/locations', methods=["GET"])
def locations():
    '''View for the Locations Admin Page'''

    locations_query = '''
    SELECT
        locationID,
        locationName,
        locationLatitude,
        locationLongitude,
        locationAltitude
    FROM
        Locations;
    '''

    locations_results = db.execute_query(db_connection=db_connection, query=locations_query).fetchall()

    if DEBUG:
        logger.info(locations_results)

    return render_template("pages/locations.html", locations=locations_results, location_dict=keys.key_dict)

@app.route('/sensors', methods=["GET"])
def sensors():
    '''View for the Sensors Admin Page'''

    sensor_query = '''
    SELECT 
        Sensors.sensorID,
        Sensors.sensorName,
        Sensors.sensorAPIKEY,
        Sensors.sensorNumber,
        Locations.locationLatitude,
        Locations.locationLongitude,
        Locations.locationAltitude
    FROM
        Sensors
    JOIN
        Locations ON Sensors.sensorLocationID = Locations.locationID;
    '''

    sensor_results = db.execute_query(db_connection=db_connection, query=sensor_query).fetchall()

    if DEBUG:
        logger.info(sensor_results)

    return render_template("pages/sensors.html", sensors=sensor_results, sensor_dict=keys.key_dict)
    
@app.route('/models', methods=["GET"])
def models():
    '''View for the Models Admin Page'''

    models_query = '''
    SELECT 
        modelID, 
        modelName
    FROM 
        Models
    ORDER BY 
        modelName DESC;
    '''

    models_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()

    if DEBUG:
        logger.info(models_results)

    return render_template("pages/models.html", models=models_results, model_dict=keys.key_dict)

@app.route('/dates', methods=["GET"])
def dates():
    '''View for the Dates Admin Page'''

    dates_query = '''
    SELECT
        dateID,
        dateDateTime
    FROM
        Dates;
    '''

    dates_results = db.execute_query(db_connection=db_connection, query=dates_query).fetchall()

    if DEBUG:
        logger.info(dates_results)
    return render_template("pages/dates.html", dates=dates_results, date_dict=keys.key_dict)

@app.route('/readings', methods=["GET"])
def readings():
    '''View for the Readings Admin Page'''

    readings_query = '''
    SELECT 
        Readings.readingID,
        Sensors.sensorName,
        Sensors.sensorNumber,
        Readings.readingWindSpeed,
        Readings.readingWindGust,
        Readings.readingWindMin,
        Readings.readingWindDirection,
        Readings.readingTemperature,
        Dates.dateDateTime
    FROM
        Readings
    JOIN 
        Sensors ON Readings.readingSensorID = Sensors.sensorID
    JOIN 
        Dates ON Readings.readingDateID = Dates.dateID;
    '''

    readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

    if DEBUG:
        logger.info(readings_results)

    return render_template("pages/readings.html", readings=readings_results, reading_dict=keys.key_dict)

############
# Update
############

@app.route('/edit/forecast/<int:forecastID>', methods=['POST', 'GET'])
def update_forecast(forecastID):
    '''API Route to update a forecast'''

    if request.method == 'GET':

        forecasts_query = '''
        SELECT 
            forecastID,
            forecastDateID,
            forecastTemperature2m,
            forecastPrecipitation,
            forecastWeatherCode,
            forecastPressureMSL,
            forecastWindSpeed10m,
            forecastWindDirection10m,
            forecastCape,
            forecastModelID,
            forecastLocationID,
            forecastForDateTime
        FROM 
            Forecasts
        WHERE
            forecastID = %(forecastID)s;
        '''
        
        forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query, query_params={'forecastID': forecastID}).fetchone()

        models_query = '''
        SELECT
            modelID, 
            modelName
        FROM
            Models;
        '''
        models_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()

        locations_query = '''
        SELECT
            locationID, 
            locationName
        FROM
            Locations;
        '''
        locations_results = db.execute_query(db_connection=db_connection, query=locations_query).fetchall()

        dates_query = '''
        SELECT
            dateID, 
            dateDateTime
        FROM
            Dates;
        '''
        dates_results = db.execute_query(db_connection=db_connection, query=dates_query).fetchall()

        return render_template('edit/editforecast.html', specific_forecast=forecasts_results, models=models_results, locations=locations_results, dates=dates_results)

    elif request.method == 'POST':

        model_id = request.form.get('modelID') or None

        query_params = {
            'forecastID': forecastID,
            'forecastForDateTime': request.form.get('forecastForDateTime'), 
            'forecastDateID': request.form.get('dateID'), 
            'forecastTemperature2m': request.form.get('forecastTemperature'), 
            'forecastPrecipitation': request.form.get('forecastPrecipitation'), 
            'forecastWeatherCode': request.form.get('forecastWeatherCode'), 
            'forecastPressureMSL': request.form.get('forecastPressureMSL'), 
            'forecastWindSpeed10m': request.form.get('forecastWindSpeed'), 
            'forecastWindDirection10m': request.form.get('forecastWindDirection'), 
            'forecastCape': request.form.get('forecastCape'), 
            'forecastLocationID': request.form.get('locationID'),
            'forecastModelID': model_id
        }

        # Check for Null modelID
        if model_id is None:
            forecasts_query = '''
                UPDATE 
                    `Forecasts`
                SET 
                    forecastForDateTime = %(forecastForDateTime)s,
                    forecastDateID = %(forecastDateID)s,
                    forecastTemperature2m = %(forecastTemperature2m)s,
                    forecastPrecipitation = %(forecastPrecipitation)s,
                    forecastWeatherCode = %(forecastWeatherCode)s,
                    forecastPressureMSL = %(forecastPressureMSL)s,
                    forecastWindSpeed10m = %(forecastWindSpeed10m)s,
                    forecastWindDirection10m = %(forecastWindDirection10m)s,
                    forecastCape = %(forecastCape)s,
                    forecastLocationID = %(forecastLocationID)s,
                    forecastModelID = %(forecastModelID)s
                WHERE 
                    forecastID = %(forecastID)s;
            '''

            db.execute_query(db_connection=db_connection, query=forecasts_query, query_params=query_params)
        
        else:
            forecasts_query = '''
                UPDATE 
                    `Forecasts`
                SET 
                    forecastForDateTime = %(forecastForDateTime)s,
                    forecastDateID = %(forecastDateID)s,
                    forecastTemperature2m = %(forecastTemperature2m)s,
                    forecastPrecipitation = %(forecastPrecipitation)s,
                    forecastWeatherCode = %(forecastWeatherCode)s,
                    forecastPressureMSL = %(forecastPressureMSL)s,
                    forecastWindSpeed10m = %(forecastWindSpeed10m)s,
                    forecastWindDirection10m = %(forecastWindDirection10m)s,
                    forecastCape = %(forecastCape)s,
                    forecastLocationID = %(forecastLocationID)s,
                    forecastModelID = %(forecastModelID)s
                WHERE 
                    forecastID = %(forecastID)s;
            '''
            db.execute_query(db_connection=db_connection, query=forecasts_query, query_params=query_params)

        return redirect('/forecasts')

@app.route("/edit/reading/<int:readingID>", methods=["POST", "GET"])
def readingedit(readingID):
    '''API Route to update a reading'''

    readingID = escape(readingID)
    if request.method == "GET":
        readings_query = f"SELECT * FROM Readings\nWHERE Readings.readingID = {readingID};"
        query_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchone()
        if DEBUG:
            logger.info("edit reading get: " + str(query_results))

        dates_query = '''
        SELECT
            dateID, 
            dateDateTime
        FROM
            Dates;
        '''
        dates_results = db.execute_query(db_connection=db_connection, query=dates_query).fetchall()

        sensors_query = '''
        SELECT
            sensorID,
            sensorName
        FROM
            Sensors;
        '''
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        print(str(sensors_results))
        return render_template("edit/editreading.html", specific_reading=query_results, dates=dates_results, sensors=sensors_results)

    elif request.method == "POST":
        if DEBUG:
            logger.info(f"updating reading for {request.form['readingID']}")
        print(str(request.form))
        reading_query = f"""
        UPDATE Readings
        SET `readingSensorID`='{request.form['readingSensorID']}', `readingWindSpeed`='{request.form['readingWindSpeed']}', `readingWindGust`='{request.form['readingWindGust']}', `readingWindMin`='{request.form['readingWindMin']}', `readingWindDirection`='{request.form['readingWindDirection']}', `readingTemperature`='{request.form['readingTemperature']}', `readingDateID`='{request.form['readingDateID']}'
        WHERE Readings.readingID = {readingID}
        """
        if DEBUG:
            logger.info("edit reading post: " + reading_query)
        query_obj = db.execute_query(db_connection=db_connection, query=reading_query)

        return redirect("/readings")

@app.route("/edit/sensor/<int:sensorID>", methods=["POST", "GET"])
def update_sensor(sensorID):
    '''API Route to update a sensor'''

    sensorID = escape(sensorID)

    if DEBUG:
        logger.info(f"Edit sensor post: {sensorID}")

    if request.method == "GET":
        sensor_query = '''
        SELECT 
            * 
        FROM 
            Sensors
        INNER JOIN 
            Locations ON Sensors.sensorLocationID = Locations.locationID
        WHERE 
            Sensors.sensorID = %(sensorID)s;
        '''
        sensor_results = db.execute_query(db_connection=db_connection, query=sensor_query, query_params={'sensorID': sensorID}).fetchall()

        locations_query = '''
        SELECT
            locationID, locationName
        FROM
            Locations;
        '''
        locations_results = db.execute_query(db_connection=db_connection, query=locations_query).fetchall()

        if DEBUG:
            logger.info(f"edit sensor get: {sensor_results}")

        return render_template("edit/editsensor.html", specific_sensor=sensor_results, locations=locations_results)
    
    elif request.method == "POST":
        sensor_query = f"UPDATE Sensors\n SET `sensorName`='{request.form['sensorName']}', `sensorAPIKey`='{request.form['sensorAPIKey']}', `sensorNumber`='{request.form['sensorNumber']}' \n WHERE sensorID='{sensorID}';"
        if DEBUG:
            logger.info("edit sensor post first query: " + sensor_query)
        query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        id_sensor_query = f"SELECT sensorLocationID FROM Sensors\n WHERE Sensors.sensorID='{sensorID}';"
        if DEBUG:
            logger.info("edit sensor post second query: " + id_sensor_query)
        _sensorLocationID = db.execute_query(db_connection=db_connection, query=id_sensor_query).fetchall()
        if DEBUG:
            print(str(request.form))
            logger.info("identified the sensorLocationID as: " + str(_sensorLocationID[0]['sensorLocationID']))
        location_query = f"UPDATE Locations\nSET `locationName`='{request.form['locationName']}', `locationLatitude`='{request.form['locationLatitude']}', `locationLongitude`='{request.form['locationLongitude']}', `locationAltitude`='{request.form['locationAltitude']}' \nWHERE Locations.locationID='{_sensorLocationID[0]['sensorLocationID']}';"
        if DEBUG:
            logger.info("edit sensor post third query: " + location_query)
        location_obj = db.execute_query(db_connection=db_connection, query=location_query)

        return redirect("/sensors")

@app.route("/edit/model/<int:modelID>", methods=["POST", "GET"])
def modeledit(modelID):
    '''API Route to update a model'''

    modelID = escape(modelID)
    if request.method == "GET":
        models_query = f"SELECT * FROM Models\nWHERE Models.modelID = {modelID};"
        query_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()
        if DEBUG:
            logger.info("edit model get: " + str(query_results))
        return render_template("edit/editmodel.html", specific_model=query_results)
    
    elif request.method == "POST":
        if request.form['modelName'].upper() not in valid_models_list:
            flash("Not a recognized Weather Model!")
            return redirect(f"/edit/editmodel/{request.form['modelID']}")
        if DEBUG:
            logger.info(f"updating name for {request.form['modelID']} to: {request.form['modelName']}")
        model_query = f"UPDATE Models\nSET `modelName`='{request.form['modelName']}'\nWHERE Models.modelID = {modelID};"
        if DEBUG:
            logger.info("edit model post: " + model_query)
        query_obj = db.execute_query(db_connection=db_connection, query=model_query)

        return redirect("/library")

@app.route("/edit/date/<int:dateID>", methods=["POST", "GET"])
def dateedit(dateID):
    '''API Route to update a date'''

    dateID = escape(dateID)
    if request.method == "GET":
        dates_query = f"SELECT * FROM Dates\nWHERE Dates.dateID = {dateID};"
        query_results = db.execute_query(db_connection=db_connection, query=dates_query).fetchall()
        if DEBUG:
            logger.info("edit date get: " + str(query_results))
        return render_template("edit/editdate.html", specific_date=query_results)

    elif request.method == "POST":
        if DEBUG:
            logger.info(f"updating date for {request.form['dateID']}")
        date_query = f"""
        UPDATE Dates
        SET `dateDateTime`='{request.form['dateDateTime']}'
        WHERE Dates.dateID = {dateID};
        """
        if DEBUG:
            logger.info("edit date post: " + date_query)
        query_obj = db.execute_query(db_connection=db_connection, query=date_query)

        return redirect("/dates")

@app.route("/edit/location/<int:locationID>", methods=["POST", "GET"])
def locationedit(locationID):
    '''API Route to update a date'''

    locationID = escape(locationID)
    if request.method == "GET":
        locations_query = f"SELECT * FROM Locations\nWHERE Locations.locationID = {locationID};"
        query_results = db.execute_query(db_connection=db_connection, query=locations_query).fetchall()
        if DEBUG:
            logger.info("edit location get: " + str(query_results))
        return render_template("edit/editlocation.html", specific_location=query_results)

    elif request.method == "POST":
        if DEBUG:
            logger.info(f"updating location for {request.form['locationID']}")
        location_query = f"""
        UPDATE Locations
        SET `locationName`='{request.form['locationName']}', `locationLatitude`='{request.form['locationLatitude']}', `locationLongitude`='{request.form['locationLongitude']}', `locationAltitude`='{request.form['locationAltitude']}'
        WHERE Locations.locationID = {locationID};
        """
        if DEBUG:
            logger.info("edit location post: " + location_query)
        query_obj = db.execute_query(db_connection=db_connection, query=location_query)

        return redirect("/locations")

############
# DELETE
############

@app.route('/delete/forecast/<int:forecastID>', methods=['GET'])
def delete_forecast(forecastID):
    '''API Route to delete a forecast'''

    if DEBUG:
        logger.info(f'Delete forecast: {forecastID}')

    query = '''
    DELETE FROM 
        Forecasts
    WHERE
        forecastID = %(forecastID)s;
    '''

    db.execute_query(db_connection=db_connection, query=query, query_params={'forecastID': forecastID})
    
    flash(f'Successfully deleted forecast!')

    return redirect('/forecasts')

@app.route("/delete/sensor/<int:sensorID>", methods=["GET"])
def delete_sensor(sensorID):
    '''API Route to delete a sensor'''

    if DEBUG:
        logger.info(f'Delete sensor: {sensorID}')

    query = '''
    DELETE FROM
        Sensors
    WHERE
        sensorID = %(sensorID)s;
    '''

    db.execute_query(db_connection=db_connection, query=query, query_params={'sensorID': sensorID})

    flash(f"Successfully deleted sensor!")

    return redirect("/sensors")

@app.route("/delete/model/<int:modelID>", methods=["GET"])
def delete_model(modelID):
    '''API Route to delete a model'''

    if DEBUG:
        logger.info(f'Delete model: {modelID}')

    query = '''
    DELETE FROM 
        Models
    WHERE 
        modelID = %(modelID)s;
    '''

    db.execute_query(db_connection=db_connection, query=query, query_params={'modelID': modelID})

    flash(f"Successfully deleted model!")

    return redirect("/models")

@app.route("/delete/reading/<int:readingID>", methods=["GET"])
def delete_reading(readingID):
    '''API Route to delete a reading'''

    if DEBUG:
        logger.info(f'Delete reading: {readingID}')

    query = '''
    DELETE FROM
        Readings
    WHERE
        readingID = %(readingID)s;
    '''

    db.execute_query(db_connection=db_connection, query=query, query_params={'readingID': readingID})

    flash(f"Successfully deleted reading!")

    return redirect("/readings")

@app.route("/delete/location/<int:locationID>", methods=["GET"])
def delete_location(locationID):
    '''API Route to delete a location'''

    if DEBUG:
        logger.info(f'Delete location: {locationID}')

    query = '''
    DELETE FROM 
        Locations
    WHERE 
        locationID = %(locationID)s;
    '''

    db.execute_query(db_connection=db_connection, query=query, query_params={'locationID': locationID})

    flash(f"Successfully deleted location!")

    return redirect("/locations")

@app.route("/delete/date/<int:dateID>", methods=["GET"])
def delete_date(dateID):
    '''API Route to delete a date'''

    if DEBUG:
        logger.info(f'Delete date: {dateID}')

    query = '''
    DELETE FROM 
        Dates
    WHERE 
        dateID = %(dateID)s;
    '''

    db.execute_query(db_connection=db_connection, query=query, query_params={'dateID': dateID})

    flash(f"Successfully deleted date!")

    return redirect("/dates")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)