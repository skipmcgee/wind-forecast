sample_sensors = [
{
    'sensorID': 1,
    'sensorName': 'La Bajada Holfuy',
    'sensorLocation': 'La Bajada Ridge Launch',
    'sensorAPIKey': 'mytestapikey1234',
    'sensorNumber': 1151
},
{
    'sensorID': 2,
    'sensorName': 'Sandia Peak Holfuy',
    'sensorLocation': 'Sandia Peak Launch',
    'sensorAPIKey': 'mytestapikey23456',
    'sensorNumber': 1152
},
{
    'sensorID': 3,
    'sensorName': 'Sandia Peak Tempest',
    'sensorLocation': 'Sandia Peak Launch',
    'sensorAPIKey': 'mytestapikey345670',
    'sensorNumber': 2
}
]

sample_models = [
{
    'modelID': 1,
    'modelName': 'ECMWF'
},
{
    'modelID': 2,
    'modelName': 'HRRR'
},
{
    'modelID': 3,
    'modelName': 'GFS'
}
]

sample_forecasts = [
{
    'forecastID': 1,
    'Date Time': '2024-04-01 15:00:00',
    'Temperature': 58,
    'Precipitation': 0,
    'Weather Code': 'CLEAR',
    'Pressure MSL': 3,
    'Wind Speed': 10.0,
    'Wind Direction': 220.0,
    'Cape': 3.5,
    'Location': 'La Bajada Ridge Launch',
    'Model': 'ECMWF'
},
{
    'forecastID': 2,
    'Date Time': '2024-04-01 16:00:00',
    'Temperature': 58,
    'Precipitation': 0,
    'Weather Code': 'CLEAR',
    'Pressure MSL': 3,
    'Wind Speed': 10.0,
    'Wind Direction': 220.0,
    'Cape': 4.1,
    'Location': 'La Bajada Ridge Launch',
    'Model': 'ECMWF'
},
{
    'forecastID': 3,
    'Date Time': '2024-04-01 17:00:00',
    'Temperature': 62,
    'Precipitation': 0,
    'Weather Code': 'CLEAR',
    'Pressure MSL': 4,
    'Wind Speed': 14.0,
    'Wind Direction': 230.0,
    'Cape': 4.2,
    'Location': 'La Bajada Ridge Launch',
    'Model': 'ECMWF'
}
]

sample_locations = [
{
    'locationID': 1,
    'Name': 'La Bajada Ridge Launch',
    'Latitude': 35.56195,
    'Longitude': -106.22596,
    'Altitude': 6135
},
{
    'locationID': 2,
    'Name': 'Sandia Peak Launch',
    'Latitude': 35.196576,
    'Longitude': -106.434662,
    'Altitude': 10275
},
{
    'locationID': 3,
    'Name': 'Sandia Crest Launch',
    'Latitude': 35.21342,
    'Longitude': -106.45026,
    'Altitude': 10600
}
]

sample_dates = [
{
    'dateID': 1,
    'dateDateTime': '2024-04-01 08:00:00'
},
{
    'dateID': 2,
    'dateDateTime': '2024-04-01 09:00:00'
},
{
    'dateID': 3,
    'dateDateTime': '2024-04-01 10:00:00'
}
]

sample_readings = [
{
    'readingID': 1,
    'readingSensor': 'La Bajada Holfuy',
    'readingDate': '2024-04-01 08:00:00',
    'readingWindSpeed': 22.0,
    'readingWindGust': 28.0,
    'readingWindMin': 14.0,
    'readingWindDirection': 250,
    'readingTemperature': 64
},
{
    'readingID': 2,
    'readingSensor': 'La Bajada Holfuy',
    'readingDate': '2024-04-01 08:00:00',
    'readingWindSpeed': 22.0,
    'readingWindGust': 28.0,
    'readingWindMin': 14.0,
    'readingWindDirection': 250,
    'readingTemperature': 64
},
{
    'readingID': 3,
    'readingSensor': 'La Bajada Holfuy',
    'readingDate': '2024-04-01 09:00:00',
    'readingWindSpeed': 20.0,
    'readingWindGust': 22.0,
    'readingWindMin': 6.0,
    'readingWindDirection': 232,
    'readingTemperature': 66
}
]