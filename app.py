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

# Configuration
app = Flask(__name__)
app.secret_key = 'mc)kNIk4cbIZQ,@jUve-Q}2^T3em$p'
db_connection = db.connect_to_database()
logger = logging.getLogger('werkzeug')
entities_list = ['models', 'locations', 'sensors', 'forecasts', 'readings', ] 
valid_models_list = ['HRRR', 'ECMWF', 'MBLUE', 'GFS', 'NAM', 'ICON', ]
current_supported_model_list = ['ECMWF', 'GFS']
current_supported_sensor_list = ['1',]
info_dict = dict()
DEBUG = True

# Routes 
@app.route("/index")
def plain_index():
    return redirect("/")

@app.route("/index.html")
def dot_index():
    return redirect("/")

@app.route('/', methods=["POST", "GET"])
def root():
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

    return render_template("results.html", forecasts=forecasts_results, readings=readings_results, info_dict=info_dict)

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
        return render_template("library.html", sensors=sensor_results, models=model_results, locations=locations_results)
    elif request.method == "POST":
        return redirect("/")

############
# Create
############

@app.route('/add/forecast', methods=["POST", "GET"])
def add_forecast():
    '''API Route to add a forecast'''

    # Need to get Model, Location, Date for dropdowns
    if request.method == "GET":
        sensors_query = "SELECT * FROM Sensors;"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        models_query = "SELECT * FROM Models;"
        models_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()
        return render_template("add/forecast.html", sensors=sensors_results, models=models_results)
    
    elif request.method == "POST":
        if DEBUG:
            logger.info(str(request.form))
        use_sensorID = request.form['sensorlist']
        use_modelID = request.form['modellist']
        if DEBUG:
            logger.info("add forecast post for sensor: " + use_sensorID + " and model: " + use_modelID)
        model_query = f"SELECT * from Models\n WHERE modelID='{use_modelID}';"
        model_results = db.execute_query(db_connection=db_connection, query=model_query).fetchall()
        if DEBUG:
            logger.info("add forecast post model results: " + str(model_results))
        sensor_query = f"SELECT * from Sensors\nJOIN Locations ON Sensors.sensorLocationID = Locations.locationID\n WHERE sensorID='{use_sensorID}';"
        sensor_results = db.execute_query(db_connection=db_connection, query=sensor_query).fetchall()
        if DEBUG:
            logger.info("add forecast post sensor results: " + str(sensor_results))
        if model_results[0]['modelName'] not in current_supported_model_list:
            flash(f"This model is not currently supported!")
            return redirect("/add/forecast")
        elif model_results[0]['modelName'] == "ECMWF":
            ecmwf = query_ecmwf(sensor_results[0]['locationLatitude'], sensor_results[0]['locationLongitude'])
            forecast_query = f"INSERT INTO Forecasts (`forecastDateID`, `forecastTemperature2m`, `forecastPrecipitation`, `forecastWeatherCode`, `forecastPressureMSL`, `forecastWindSpeed10m`, `forecastWindDirection10m`, `forecastCape`, `forecastModelID`, `forecastLocationID`, `forecastForDateTime`)\n VALUES "
            row_count = len(ecmwf.index)
            for index,row in ecmwf.iterrows():
                logger.info(f"index: {index}, row: {row}, values: {row['date']}")
                date_check_query = f"SELECT `dateID`\nFROM Dates\nWHERE `dateDateTime`='{row['date']}';"
                date_results = db.execute_query(db_connection=db_connection, query=date_check_query).fetchall()
                if len(date_results) == 0:
                    date_create_id = f"INSERT INTO Dates (`dateDateTime`)\n VALUES ('{row['date']}');"
                    date_id = db.execute_query(db_connection=db_connection, query=date_create_id)
                    date_results = db.execute_query(db_connection=db_connection, query=date_check_query).fetchall()
                forecast_query += f"\n('{date_results[0]['dateID']}', '{row['temperature_2m']}', '{row['precipitation']}', '{row['weather_code']}', '{row['pressure_msl']}', '{row['wind_speed_10m']}', '{row['wind_direction_10m']}', '{row['cape']}', '{model_results[0]['modelID']}', '{sensor_results[0]['locationID']}', '{row['date']}')"
                if index != row_count-1:
                    forecast_query += ","
            forecast_query += ";"
            forecast_obj = db.execute_query(db_connection=db_connection, query=forecast_query)

        elif model_results[0]['modelName'] == "GFS":
            gfs = query_gfs(sensor_results[0]['locationLatitude'], sensor_results[0]['locationLongitude'])
            forecast_query = f"INSERT INTO Forecasts (`forecastDateID`, `forecastTemperature2m`, `forecastPrecipitation`, `forecastWeatherCode`, `forecastPressureMSL`, `forecastWindSpeed10m`, `forecastWindDirection10m`, `forecastCape`, `forecastModelID`, `forecastLocationID`, `forecastForDateTime`)\n VALUES "
            row_count = len(gfs.index)
            for index,row in gfs.iterrows():
                logger.info(f"index: {index}, row: {row}, values: {row['date']}")
                date_check_query = f"SELECT `dateID`\nFROM Dates\nWHERE `dateDateTime`='{row['date']}';"
                date_results = db.execute_query(db_connection=db_connection, query=date_check_query).fetchall()
                if len(date_results) == 0:
                    date_create_id = f"INSERT INTO Dates (`dateDateTime`)\n VALUES ('{row['date']}');"
                    date_id = db.execute_query(db_connection=db_connection, query=date_create_id)
                    date_results = db.execute_query(db_connection=db_connection, query=date_check_query).fetchall()
                forecast_query += f"\n('{date_results[0]['dateID']}', '{row['temperature_2m']}', '{row['precipitation']}', '{row['weather_code']}', '{row['pressure_msl']}', '{row['wind_speed_10m']}', '{row['wind_direction_10m']}', '{row['cape']}', '{model_results[0]['modelID']}', '{sensor_results[0]['locationID']}', '{row['date']}')"
                if index != row_count-1:
                    forecast_query += ","
            forecast_query += ";"
            forecast_obj = db.execute_query(db_connection=db_connection, query=forecast_query)
        now = datetime.now()
        date_format = "%Y-%m-%d %H:%M:%S"
        datetime_str = now.strftime(date_format)
        old_date = now - timedelta(hours=1)
        new_date = now + timedelta(days=7)
        new_date_str = new_date.strftime(date_format)
        old_date_str = old_date.strftime(date_format)
        info_dict['fromdate'] = old_date_str
        info_dict['todate'] = new_date_str
        info_dict['sensorlist'] = request.form['sensorlist']
        info_dict['sensorName'] = sensor_results[0]['sensorName']
        forecasts_query = f"SELECT forecastID, forecastForDateTime, forecastDateID, forecastTemperature2m, forecastPrecipitation, forecastWeatherCode, forecastPressureMSL, forecastWindSpeed10m, forecastWindDirection10m, forecastCape FROM Forecasts\nJOIN Models ON Forecasts.forecastModelID = Models.modelID\nJOIN Locations ON Forecasts.forecastLocationID = Locations.locationID\nWHERE ( forecastForDateTime BETWEEN '{info_dict['fromdate']}' AND '{info_dict['todate']}' ) AND ( Locations.locationID='{info_dict['sensorlist']}' );"
        if DEBUG:
            logger.info("results forecasts query: " + forecasts_query)
        forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()
        readings_query = f"SELECT readingID, readingSensorID, readingDateID, readingWindSpeed, readingWindGust, readingWindMin, readingWindDirection, readingTemperature FROM Readings\nJOIN Sensors ON Readings.readingSensorID = Sensors.sensorID\nJOIN Dates ON Readings.readingDateID = Dates.dateID\nWHERE ( dateDateTime BETWEEN '{info_dict['fromdate']}' AND '{info_dict['todate']}' ) AND ( Sensors.sensorLocationID='{info_dict['sensorlist']}' );"
        if DEBUG:
            logger.info("results readings query: " + readings_query)
        readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

        return render_template("results.html", forecasts=forecasts_results, readings=readings_results, info_dict=info_dict)
    
@app.route("/add/sensor", methods=["POST", "GET",])
def add_sensor():
    '''API Route to add a sensor'''

    if request.method == "GET":
        return render_template("add/sensor.html")

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
        return render_template("add/model.html")
    
    elif request.method == "POST":
        if DEBUG:
            logger.info("add model post: " + request.form['modelName'].upper())
        if request.form['modelName'].upper() not in valid_models_list:
            flash("Not a recognized Weather Model!")
            return render_template("add/addmodel.html")
        model_update = f"INSERT INTO `Models` (modelName)\n VALUES ('{request.form['modelName'].upper()}');"
        if DEBUG:
            logger.info("add model post query: " + model_update)
        model_obj = db.execute_query(db_connection=db_connection, query=model_update)
        return redirect("/library")

@app.route('/add/reading', methods=["POST", "GET"])
def add_reading():
    '''API Route to add a reading'''

    if request.method == "GET":
        sensors_query = "SELECT * FROM Sensors;"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        return render_template("add/reading.html", sensors=sensors_results)
    
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

@app.route("/add/location", methods=["POST", "GET",])
def add_location():
    '''API Route to add a location'''

    if request.method == "GET":
        return render_template("add/location.html")

    elif request.method == "POST":
        if DEBUG:
            logger.info(str(request.form))
        location_query = f"INSERT INTO Locations (`locationName`, `locationLatitude`, `locationLongitude`, `locationAltitude`,)\nVALUES ({request.form['locationName']}, {request.form['locationLatitude']}, {request.form['locationLongitude']}, {request.form['locationAltitude']},);"
        if DEBUG: 
            logger.info("add sensor post first query: " + location_query)
        location_obj = db.execute_query(db_connection=db_connection, query=location_query)
        return redirect("/library")
    
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
        return redirect("/library")


############
# Read
############

@app.route('/sensors', methods=["GET"])
def sensors():
    '''View for the Sensors Admin Page'''
    
    sensor_dict = dict()
    sensor_dict['sensorID'] = 'ID'
    sensor_dict['sensorName'] = 'Name'
    sensor_dict['sensorAPIKEY'] = 'API Key' 
    sensor_dict['sensorNumber'] = 'Number'
    sensor_dict['locationLatitude'] = 'Latitude'
    sensor_dict['locationLongitude'] = 'Longitude'
    sensor_dict['locationAltitude'] = 'Altitude'

    query = '''
    SELECT
        sensorID, 
        sensorName, 
        sensorAPIKEY, 
        sensorNumber, 
        locationLatitude, 
        locationLongitude, 
        locationAltitude
    FROM 
        Sensors
    JOIN Locations ON Sensors.sensorLocationID = Locations.locationID
    ORDER BY
        sensorName DESC;
    '''

    results = db.execute_query(db_connection=db_connection, query=query).fetchall()

    if DEBUG:
        logger.info(results)

    return render_template("pages/sensors.html", sensors=results, sensor_dict=sensor_dict)
    
@app.route('/models', methods=["GET"])
def models():
    '''View for the Models Admin Page'''

    model_dict = dict()
    model_dict['modelID'] = 'ID' 
    model_dict['modelName'] = 'Model Name'

    query = '''
    SELECT 
        modelID, 
        modelName
    FROM 
        Models
    ORDER BY 
        modelName DESC;
    '''

    results = db.execute_query(db_connection=db_connection, query=query).fetchall()

    if DEBUG:
        logger.info(results)

    return render_template("pages/models.html", models=results, model_dict=model_dict)
    
@app.route('/forecasts', methods=["GET"])
def forecasts():
    '''View for the Forecasts Admin Page'''

    #TODO
    # Add join(s) to view relevant data from other tables
    forecast_dict = dict()
    forecast_dict['forecastID'] = 'ID'
    forecast_dict['forecastDateID'] = 'Date'
    forecast_dict['forecastTemperature2m'] = 'Temperature'
    forecast_dict['forecastPrecipitation'] = 'Precipitation'
    forecast_dict['forecastWeatherCode'] = 'Weather Code'
    forecast_dict['forecastPressureMSL'] = 'Pressure MSL'
    forecast_dict['forecastWindSpeed10m'] = 'Wind Speed'
    forecast_dict['forecastWindDirection10m'] = 'Wind Direction'
    forecast_dict['forecastCape'] = 'Cape'
    forecast_dict['forecastModelID'] = 'Model'
    forecast_dict['forecastLocationID'] = 'Location'
    forecast_dict['forecastForDateTime'] = 'Date/Time'

    query = '''
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
        Forecasts;
    '''

    results = db.execute_query(db_connection=db_connection, query=query).fetchall()

    if DEBUG:
        logger.info(results)

    return render_template("pages/forecasts.html", forecasts=results, forecast_dict=forecast_dict)

@app.route('/locations', methods=["GET"])
def locations():
    '''View for the Locations Admin Page'''

    location_dict = dict()
    location_dict['locationID'] = 'ID'
    location_dict['locationName'] = 'Location Name'
    location_dict['locationLatitude'] = 'Latitude'
    location_dict['locationLongitude'] = 'Longitude'
    location_dict['locationAltitude'] = 'Altitude'

    query = '''
    SELECT
        locationID,
        locationName,
        locationLatitude,
        locationLongitude,
        locationAltitude
    FROM
        Locations;
    '''

    results = db.execute_query(db_connection=db_connection, query=query).fetchall()

    if DEBUG:
        logger.info(results)

    return render_template("pages/locations.html", locations=results, location_dict=location_dict)

@app.route('/dates', methods=["GET"])
def dates():
    '''View for the Dates Admin Page'''
    date_dict = dict()
    date_dict['dateID'] = 'ID'
    date_dict['dateDateTime'] = 'Date/Time'

    query = '''
    SELECT
        dateID,
        dateDateTime
    FROM
        Dates;
    '''

    results = db.execute_query(db_connection=db_connection, query=query).fetchall()

    if DEBUG:
        logger.info(results)
    return render_template("pages/dates.html", dates=results, date_dict=date_dict)

@app.route('/readings', methods=["GET"])
def readings():
    '''View for the Readings Admin Page'''

    reading_dict = dict()
    reading_dict['readingID'] = 'ID'
    reading_dict['readingSensorID'] = 'Sensor'
    reading_dict['readingWindSpeed'] = 'Average Wind Speed'
    reading_dict['readingWindGust'] = 'Wind Gust'
    reading_dict['readingWindMin'] = 'Wind Minimum Speed'
    reading_dict['readingWindDirection'] = 'Wind Direction'
    reading_dict['readingTemperature'] = 'Temperature'
    reading_dict['readingDateID'] = 'Date ID'

    query = '''
    SELECT readingID, 
        readingSensorID,
        readingWindSpeed,
        readingWindGust,
        readingWindMin,
        readingWindDirection,
        readingTemperature,
        readingDateID
    FROM
        Readings;
    '''

    results = db.execute_query(db_connection=db_connection, query=query).fetchall()

    if DEBUG:
        logger.info(results)

    return render_template("pages/readings.html", readings=results, reading_dict=reading_dict)

############
# Update
############

@app.route("/edit/sensor/<int:sensorID>", methods=["POST", "GET"])
def update_sensor(sensorID):
    '''API Route to update a sensor'''

    sensorID = escape(sensorID)

    if DEBUG:
        logger.info(f"Edit sensor post: {sensorID}")

    if request.method == "GET":
        query = '''
        SELECT 
            * 
        FROM 
            Sensors
        INNER JOIN 
            Locations ON Sensors.sensorLocationID = Locations.locationID
        WHERE 
            Sensors.sensorID = %(sensorID)s;
        '''
        results = db.execute_query(db_connection=db_connection, query=query, query_params={'sensorID': sensorID}).fetchall()

        if DEBUG:
            logger.info(f"edit sensor get: {results}")

        return render_template("edit/sensor.html", specific_sensor=results)
    
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
            return redirect(f"/edit/model/{request.form['modelID']}")
        if DEBUG:
            logger.info(f"updating name for {request.form['modelID']} to: {request.form['modelName']}")
        model_query = f"UPDATE Models\nSET `modelName`='{request.form['modelName']}'\nWHERE Models.modelID = {modelID};"
        if DEBUG:
            logger.info("edit model post: " + model_query)
        query_obj = db.execute_query(db_connection=db_connection, query=model_query)

        return redirect("/library")

############
# DELETE
############

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

@app.route("/delete/forecast/<int:forecastID>", methods=["GET"])
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
    
    flash(f"Successfully deleted forecast!")

    return redirect("/forecasts")

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