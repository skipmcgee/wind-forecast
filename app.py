from flask import Flask, render_template, flash, redirect
import os

from sample_data import *

# Configuration

app = Flask(__name__)

############
# Routes
############

@app.route('/')
def root():
    '''View for the website index'''

    return render_template('pages/index.html')

############
# Create
############

@app.route('/add/forecast', methods=['POST', 'GET'])
def add_forecast():
    '''API Route to add a forecast'''

    return render_template('add/forecast.html', models=sample_models, dates=sample_dates)

@app.route('/add/location', methods=['POST', 'GET'])
def add_location():
    '''API Route to add a location'''

    return render_template('add/location.html')

@app.route('/add/sensor', methods=['POST', 'GET'])
def add_sensor():
    '''API Route to add a sensor'''

    return render_template('add/sensor.html', locations=sample_locations)


@app.route('/add/model', methods=['POST', 'GET'])
def add_model():
    '''API Route to add a model'''

    return render_template('add/model.html')
    
@app.route('/add/date', methods=['POST', 'GET'])
def add_date():
    '''API Route to add a date'''

    return render_template('add/date.html')

@app.route('/add/reading', methods=['POST', 'GET'])
def add_reading():
    '''API Route to add a reading'''

    return render_template('add/reading.html', sensors=sample_sensors, dates=sample_dates)

############
# Read
############

@app.route('/forecasts', methods=['GET'])
def forecasts():
    '''View for the Forecasts Admin Page'''

    return render_template('pages/forecasts.html', forecasts=sample_forecasts)

@app.route('/locations', methods=['GET'])
def locations():
    '''View for the Locations Admin Page'''

    return render_template('pages/locations.html', locations=sample_locations)

@app.route('/sensors', methods=['GET'])
def sensors():
    '''View for the Sensors Admin Page'''
   
    return render_template('pages/sensors.html', sensors=sample_sensors)
    
@app.route('/models', methods=['GET'])
def models():
    '''View for the Models Admin Page'''

    return render_template('pages/models.html', models=sample_models)

@app.route('/dates', methods=['GET'])
def dates():
    '''View for the Dates Admin Page'''

    return render_template('pages/dates.html', dates=sample_dates)

@app.route('/readings', methods=['GET'])
def readings():
    '''View for the Readings Admin Page'''

    return render_template('pages/readings.html', readings=sample_readings)

############
# Update
############

@app.route('/edit/forecast/<int:forecastID>', methods=['POST', 'GET'])
def update_forecast(forecastID):
    '''API Route to update a forecast'''

    for forecast in sample_forecasts:
        if forecast['forecastID'] == forecastID:
            result = forecast

    return render_template('edit/forecast.html', specific_forecast=result, dates=sample_dates, locations=sample_locations, models=sample_models)

@app.route('/edit/location/<int:locationID>', methods=['POST', 'GET'])
def update_location(locationID):
    '''API Route to update a location'''

    for location in sample_locations:
        if location['locationID'] == locationID:
            result = location

    return render_template('edit/location.html', specific_location=result)

@app.route('/edit/sensor/<int:sensorID>', methods=['POST', 'GET'])
def update_sensor(sensorID):
    '''API Route to update a sensor'''

    for sensor in sample_sensors:
        if sensor['sensorID'] == sensorID:
            result = sensor

    return render_template('edit/sensor.html', specific_sensor=result, locations=sample_locations)

@app.route('/edit/model/<int:modelID>', methods=['POST', 'GET'])
def modeledit(modelID):
    '''API Route to update a model'''

    for model in sample_models:
        if model['modelID'] == modelID:
            result = model

    return render_template('edit/model.html', specific_model=result)

@app.route('/edit/date/<int:dateID>', methods=['POST', 'GET'])
def dateedit(dateID):
    '''API Route to update a date'''

    for date in sample_dates:
        if date['dateID'] == dateID:
            result = date

    return render_template('edit/date.html', specific_date=result)

@app.route('/edit/reading/<int:readingID>', methods=['POST', 'GET'])
def readingedit(readingID):
    '''API Route to update a reading'''

    for reading in sample_readings:
        if reading['readingID'] == readingID:
            result = reading

    return render_template('edit/reading.html', specific_reading=result, sensors=sample_sensors, dates=sample_dates)


############
# DELETE
############

@app.route('/delete/forecast/<int:forecastID>', methods=['GET'])
def delete_forecast(forecastID):
    '''API Route to delete a forecast'''

    return redirect('/forecasts')

@app.route('/delete/location/<int:locationID>', methods=['GET'])
def delete_location(locationID):
    '''API Route to delete a location'''

    return redirect('/locations')

@app.route('/delete/sensor/<int:sensorID>', methods=['GET'])
def delete_sensor(sensorID):
    '''API Route to delete a sensor'''

    return redirect('/sensors')
    
@app.route('/delete/model/<int:modelID>', methods=['GET'])
def delete_model(modelID):
    '''API Route to delete a model'''

    return redirect('/models')

@app.route('/delete/date/<int:dateID>', methods=['GET'])
def delete_date(dateID):
    '''API Route to delete a date'''

    return redirect('/dates')

@app.route('/delete/reading/<int:readingID>', methods=['GET'])
def delete_reading(readingID):
    '''API Route to delete a reading'''

    return redirect('/readings')

# Listener

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3797))
    app.run(port=port, debug=True)