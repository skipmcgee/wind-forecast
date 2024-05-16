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
    'forecastDateTime': '2024-04-01 15:00:00',
    'forecastTemperature': 58,
    'forecastPrecipitation': 0,
    'forecastWeatherCode': 'CLEAR',
    'forecastPressureMSL': 3,
    'forecastWindSpeed': 10.0,
    'forecastWindDirection': 220.0,
    'forecastCape': 3.5,
    'forecastLocation': 'La Bajada Ridge Launch',
    'forecastModel': 'ECMWF'
},
{
    'forecastID': 2,
    'forecastDateTime': '2024-04-01 16:00:00',
    'forecastTemperature': 58,
    'forecastPrecipitation': 0,
    'forecastWeatherCode': 'CLEAR',
    'forecastPressureMSL': 3,
    'forecastWindSpeed': 10.0,
    'forecastWindDirection': 220.0,
    'forecastCape': 4.1,
    'forecastLocation': 'La Bajada Ridge Launch',
    'forecastModel': 'ECMWF'
},
{
    'forecastID': 3,
    'forecastDateTime': '2024-04-01 17:00:00',
    'forecastTemperature': 62,
    'forecastPrecipitation': 0,
    'forecastWeatherCode': 'CLEAR',
    'forecastPressureMSL': 4,
    'forecastWindSpeed': 14.0,
    'forecastWindDirection': 230.0,
    'forecastCape': 4.2,
    'forecastLocation': 'La Bajada Ridge Launch',
    'forecastModel': 'ECMWF'
}
]

sample_locations = [
{
    'locationID': 1,
    'locationName': 'La Bajada Ridge Launch',
    'locationLatitude': 35.56195,
    'locationLongitude': -106.22596,
    'locationAltitude': 6135
},
{
    'locationID': 2,
    'locationName': 'Sandia Peak Launch',
    'locationLatitude': 35.196576,
    'locationLongitude': -106.434662,
    'locationAltitude': 10275
},
{
    'locationID': 3,
    'locationName': 'Sandia Crest Launch',
    'locationLatitude': 35.21342,
    'locationLongitude': -106.45026,
    'locationAltitude': 10600
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