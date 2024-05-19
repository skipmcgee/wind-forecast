class KeyTranslation:
    ''' used for data structures, mapping and validation '''
    def __init__(self):
        self.key_dict = dict()
        self.key_dict['sensorID'] = 'ID'
        self.key_dict['sensorName'] = 'Sensor Name'
        self.key_dict['sensorAPIKEY'] = 'API Key' 
        self.key_dict['sensorNumber'] = 'Sensor Number'
        self.key_dict['locationLatitude'] = 'Latitude'
        self.key_dict['locationLongitude'] = 'Longitude'
        self.key_dict['locationAltitude'] = 'Altitude'
        self.key_dict['modelID'] = 'ID' 
        self.key_dict['modelName'] = 'Model Name'
        self.key_dict['forecastID'] = 'ID'
        self.key_dict['forecastDateID'] = 'Date'
        self.key_dict['forecastTemperature2m'] = 'Temperature'
        self.key_dict['forecastPrecipitation'] = 'Precipitation'
        self.key_dict['forecastWeatherCode'] = 'Weather Code'
        self.key_dict['forecastPressureMSL'] = 'Pressure MSL'
        self.key_dict['forecastWindSpeed10m'] = 'Wind Speed'
        self.key_dict['forecastWindDirection10m'] = 'Wind Direction'
        self.key_dict['forecastCape'] = 'Cape'
        self.key_dict['forecastModelID'] = 'Model'
        self.key_dict['forecastLocationID'] = 'Location'
        self.key_dict['forecastForDateTime'] = 'Date/Time'
        self.key_dict['locationID'] = 'ID'
        self.key_dict['locationName'] = 'Location Name'
        self.key_dict['locationLatitude'] = 'Latitude'
        self.key_dict['locationLongitude'] = 'Longitude'
        self.key_dict['locationAltitude'] = 'Altitude'
        self.key_dict['dateID'] = 'ID'
        self.key_dict['dateDateTime'] = 'Date/Time'
        self.key_dict['readingID'] = 'ID'
        self.key_dict['readingSensorID'] = 'Sensor'
        self.key_dict['readingWindSpeed'] = 'Average Wind Speed'
        self.key_dict['readingWindGust'] = 'Wind Gust'
        self.key_dict['readingWindMin'] = 'Wind Minimum Speed'
        self.key_dict['readingWindDirection'] = 'Wind Direction'
        self.key_dict['readingTemperature'] = 'Temperature'
        self.key_dict['readingDateID'] = 'Date ID'
        self.entities_list = ['models', 'locations', 'sensors', 'forecasts', 'readings', ] 
        self.valid_models_list = ['HRRR', 'ECMWF', 'MBLUE', 'GFS', 'NAM', 'ICON', ]
        self.current_supported_model_list = ['ECMWF', 'GFS']
        self.current_supported_sensor_list = ['1',]

        def check_valid_model(self, passed_model: str) -> bool:
            ''' check if model is supported and model name is valid '''
            if passed_model in self.valid_models_list:
                if passed_model in self.current_supported_sensor_list:
                    return True
            return False
