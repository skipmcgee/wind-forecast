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
        return render_template("index.html", sensors=sensors_results, today=str(today))
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
    forecasts_query = f"SELECT forecastID, forecastForDateTime, forecastDateID, forecastTemperature2m, forecastPrecipitation, forecastWeatherCode, forecastPressureMSL, forecastWindSpeed10m, forecastWindGust, forecastWindDirection10m, forecastCape FROM Forecasts\nJOIN Models ON Forecasts.forecastModelID = Models.modelID\nJOIN Locations ON Forecasts.forecastLocationID = Locations.locationID\nWHERE ( forecastForDateTime BETWEEN '{info_dict['fromdate']}' AND '{info_dict['todate']}' ) AND ( Locations.locationID='{info_dict['sensorlist']}' );"
    if DEBUG:
        logger.info("results forecasts query: " + forecasts_query)
    forecasts_results = db.execute_query(db_connection=db_connection, query=forecasts_query).fetchall()
    readings_query = f"SELECT readingID, readingSensorID, readingDateID, readingWindSpeed, readingWindGust, readingWindMin, readingWindDirection, readingTemperature FROM Readings\nJOIN Sensors ON Readings.readingSensorID = Sensors.sensorID\nJOIN Dates ON Readings.readingDateID = Dates.dateID\nWHERE ( dateDateTime BETWEEN '{info_dict['fromdate']}' AND '{info_dict['todate']}' ) AND ( Sensors.sensorLocationID='{info_dict['sensorlist']}' );"
    if DEBUG:
        logger.info("results readings query: " + readings_query)
    readings_results = db.execute_query(db_connection=db_connection, query=readings_query).fetchall()

    return render_template("results.html", forecasts=forecasts_results, readings=readings_results, info_dict=info_dict)


@app.route('/sensors', methods=["POST", "GET"])
def sensors():
    ''''''
    if request.method == "GET":
        sensor_query = f"SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationAltitude FROM Sensors\n JOIN Locations ON Sensors.sensorLocationID = Locations.locationID\n ORDER BY sensorName DESC;"
        sensor_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        sensor_results = sensor_obj.fetchall()
        if DEBUG:
            logger.info(sensor_results)
        return render_template("sensors.html", sensors=sensor_results)
    elif request.method == "POST":
        return redirect("/")
    
@app.route('/models', methods=["POST", "GET"])
def models():
    ''''''
    if request.method == "GET":
        model_query = f"SELECT * FROM Models\n ORDER BY modelName DESC;"
        model_obj = db.execute_query(db_connection=db_connection, query=model_query)
        model_results = model_obj.fetchall()
        if DEBUG:
            logger.info(model_results)
        return render_template("models.html", models=model_results)
    elif request.method == "POST":
        return redirect("/")
    
@app.route('/forecasts', methods=["POST", "GET"])
def forecasts():
    ''''''
    if request.method == "GET":
        query = f"SELECT * FROM forecasts;"
        obj = db.execute_query(db_connection=db_connection, query=query)
        results = obj.fetchall()
        if DEBUG:
            logger.info(results)
        return render_template("forecasts.html", forecasts=results)
    elif request.method == "POST":
        return redirect("/")

@app.route('/locations', methods=["POST", "GET"])
def locations():
    ''''''
    if request.method == "GET":
        query = f"SELECT * FROM locations;"
        obj = db.execute_query(db_connection=db_connection, query=query)
        results = obj.fetchall()
        if DEBUG:
            logger.info(results)
        return render_template("locations.html", locations=results)
    elif request.method == "POST":
        return redirect("/")

@app.route('/dates', methods=["POST", "GET"])
def dates():
    ''''''
    if request.method == "GET":
        query = f"SELECT * FROM dates;"
        obj = db.execute_query(db_connection=db_connection, query=query)
        results = obj.fetchall()
        if DEBUG:
            logger.info(results)
        return render_template("dates.html", dates=results)
    elif request.method == "POST":
        return redirect("/")

@app.route('/readings', methods=["POST", "GET"])
def readings():
    ''''''
    if request.method == "GET":
        query = f"SELECT * FROM readings;"
        obj = db.execute_query(db_connection=db_connection, query=query)
        results = obj.fetchall()
        if DEBUG:
            logger.info(results)
        return render_template("readings.html", readings=results)
    elif request.method == "POST":
        return redirect("/")

@app.route('/library', methods=["POST", "GET"])
def library():
    if request.method == "GET":
        sensor_query = f"SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationAltitude FROM Sensors\n JOIN Locations ON Sensors.sensorLocationID = Locations.locationID\n ORDER BY sensorName DESC;"
        sensor_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        sensor_results = sensor_obj.fetchall()
        if DEBUG:
            logger.info(sensor_results)
        model_query = f"SELECT * FROM Models\n ORDER BY modelName DESC;"
        model_obj = db.execute_query(db_connection=db_connection, query=model_query)
        model_results = model_obj.fetchall()
        if DEBUG:
            logger.info(model_results)
        return render_template("library.html", sensors=sensor_results, models=model_results)
    elif request.method == "POST":
        return redirect("/")

@app.route("/delete/sensor/<int:sensorID>", methods=["POST", "GET"])
def deletesensor(sensorID):
    sensorID = escape(sensorID)
    if DEBUG:
        logger.info("delete sensor: " + str(sensorID))
    sensor_query = f"DELETE FROM Sensors\nWHERE sensorID={sensorID};"
    query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
    flash(f"Successfully deleted sensor!")
    return redirect("/library")

@app.route("/delete/model/<int:modelID>", methods=["POST", "GET"])
def deletemodel(modelID):
    modelID = escape(modelID)
    if DEBUG:
        logger.info("delete model: " + str(modelID))
    model_query = f"DELETE FROM Models\nWHERE modelID={modelID};"
    query_obj = db.execute_query(db_connection=db_connection, query=model_query)
    flash(f"Successfully deleted model!")
    return redirect("/library")

@app.route("/delete/forecast/<int:forecastID>", methods=["POST", "GET"])
def deleteforecast(forecastID):
    forecastID = escape(forecastID)
    if DEBUG:
        logger.info("delete forecast: " + str(forecastID))
    forecast_query = f"DELETE FROM Forecasts\nWHERE Forecasts.forecastID={forecastID};"
    query_obj = db.execute_query(db_connection=db_connection, query=forecast_query)

    return redirect("/results")

@app.route("/delete/reading/<int:readingID>", methods=["POST", "GET"])
def deletereading(readingID):
    readingID = escape(readingID)
    if DEBUG:
        logger.info("delete reading: " + str(readingID))
    reading_query = f"DELETE FROM Readings\nWHERE Readings.readingID={readingID};"
    query_obj = db.execute_query(db_connection=db_connection, query=reading_query)

    return redirect("/results")

@app.route("/edit/sensor/<int:sensorID>", methods=["POST", "GET"])
def sensoredit(sensorID):
    sensorID = escape(sensorID)
    if DEBUG:
        logger.info("edit sensor post: " + str(sensorID))
    if request.method == "GET":
        sensor_query = f"SELECT * FROM Sensors\nINNER JOIN Locations ON Sensors.sensorLocationID = Locations.locationID\nWHERE Sensors.sensorID = {sensorID};"
        query_results = db.execute_query(db_connection=db_connection, query=sensor_query).fetchall()
        if DEBUG:
            logger.info("edit sensor get: " + str(query_results))
        return render_template("editsensor.html", specific_sensor=query_results)
    
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

        return redirect("/library")

@app.route("/edit/model/<int:modelID>", methods=["POST", "GET"])
def modeledit(modelID):
    modelID = escape(modelID)
    if request.method == "GET":
        models_query = f"SELECT * FROM Models\nWHERE Models.modelID = {modelID};"
        query_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()
        if DEBUG:
            logger.info("edit model get: " + str(query_results))
        return render_template("editmodel.html", specific_model=query_results)
    
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

@app.route("/add/sensor", methods=["POST", "GET",])
def addsensor():
    if request.method == "GET":
        return render_template("addsensor.html")

    elif request.method == "POST":
        logger.info(str(request.form))
        location_query = f"INSERT INTO Locations (`locationName`, `locationLatitude`, `locationLongitude`, `locationAltitude`,)\nVALUES ({request.form['locationName']}, {request.form['locationLatitude']}, {request.form['locationLongitude']}, {request.form['locationAltitude']},);"
        if DEBUG: 
            logger.info("add sensor post first query: " + location_query)
        location_obj = db.execute_query(db_connection=db_connection, query=location_query)
        sensor_query = f"INSERT INTO Sensors (`sensorName`, `sensorAPIKey`, `sensorNumber`, `sensorLocationID`,)\nVALUES ({request.form['sensorName']}, {request.form['sensorAPIKey']}, {request.form['sensorNumber']}, {request.form['sensorLocationID']},);"
        if DEBUG:
            logger.info("add sensor post second query: " + sensor_query)
        query_obj = db.execute_query(db_connection=db_connection, query=sensor_query)
        return redirect("/library")

@app.route("/add/model", methods=["POST", "GET",])
def addmodel():
    if request.method == "GET":
        return render_template("addmodel.html")
    
    elif request.method == "POST":
        if DEBUG:
            logger.info("add model post: " + request.form['modelName'].upper())
        if request.form['modelName'].upper() not in valid_models_list:
            flash("Not a recognized Weather Model!")
            return render_template("addmodel.html")
        model_update = f"INSERT INTO `Models` (modelName)\n VALUES ('{request.form['modelName'].upper()}');"
        if DEBUG:
            logger.info("add model post query: " + model_update)
        model_obj = db.execute_query(db_connection=db_connection, query=model_update)
        return redirect("/library")

@app.route('/add/reading', methods=["POST", "GET"])
def addreading():
    if request.method == "GET":
        sensors_query = "SELECT * FROM Sensors;"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        return render_template("addreading.html", sensors=sensors_results)
    
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

@app.route('/add/forecast', methods=["POST", "GET"])
def addforecast():
    if request.method == "GET":
        sensors_query = "SELECT * FROM Sensors;"
        sensors_results = db.execute_query(db_connection=db_connection, query=sensors_query).fetchall()
        models_query = "SELECT * FROM Models;"
        models_results = db.execute_query(db_connection=db_connection, query=models_query).fetchall()
        return render_template("addforecast.html", sensors=sensors_results, models=models_results)
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)