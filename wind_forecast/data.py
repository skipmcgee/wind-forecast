class KeyTranslation:
    """used for data structures, mapping and validation"""

    def __init__(self):
        self.key_dict = dict()
        self.key_dict["sensorID"] = "Sensor ID"
        self.key_dict["sensorName"] = "Sensor Name"
        self.key_dict["sensorAPIKey"] = "API Key"
        self.key_dict["sensorNumber"] = "Sensor Number"
        self.key_dict["locationLatitude"] = "Latitude"
        self.key_dict["locationLongitude"] = "Longitude"
        self.key_dict["locationAltitude"] = "Altitude"
        self.key_dict["modelID"] = "Model ID"
        self.key_dict["modelName"] = "Model Name"
        self.key_dict["forecastID"] = "Forecast ID"
        self.key_dict["forecastDateID"] = "Date"
        self.key_dict["forecastTemperature2m"] = "Temperature"
        self.key_dict["forecastPrecipitation"] = "Precipitation"
        self.key_dict["forecastWeatherCode"] = "Weather Code"
        self.key_dict["forecastPressureMSL"] = "Pressure MSL"
        self.key_dict["forecastWindSpeed10m"] = "Wind Speed"
        self.key_dict["forecastWindDirection10m"] = "Wind Direction"
        self.key_dict["forecastCape"] = "Cape"
        self.key_dict["forecastModelID"] = "Model"
        self.key_dict["forecastLocationID"] = "Location"
        self.key_dict["forecastForDateTime"] = "Forecast For Date/Time"
        self.key_dict["locationID"] = "Location ID"
        self.key_dict["locationName"] = "Location Name"
        self.key_dict["locationLatitude"] = "Latitude"
        self.key_dict["locationLongitude"] = "Longitude"
        self.key_dict["locationAltitude"] = "Altitude"
        self.key_dict["dateID"] = "Date ID"
        self.key_dict["dateDateTime"] = "Created Date/Time"
        self.key_dict["readingID"] = "Reading ID"
        self.key_dict["readingSensorID"] = "Sensor"
        self.key_dict["readingWindSpeed"] = "Average Wind Speed"
        self.key_dict["readingWindGust"] = "Wind Gust"
        self.key_dict["readingWindMin"] = "Wind Minimum Speed"
        self.key_dict["readingWindDirection"] = "Wind Direction"
        self.key_dict["readingTemperature"] = "Temperature"
        self.key_dict["readingDateID"] = "Date of Observation ID"
        self.entities_list = [
            "models",
            "locations",
            "sensors",
            "forecasts",
            "readings",
        ]
        self.valid_models_list = [
            "ECMWF",
            "MBLUE",
            "GFS",
            "NAM",
            "ICON",
        ]
        self.current_supported_model_list = ["ECMWF", "GFS"]
        self.current_supported_sensor_list = [
            "1",
        ]
        self.current_supported_sensor_models_list = [
            "Holfuy",
            "Tempest",
        ]
        self.entities_list = [
            "models",
            "locations",
            "sensors",
            "forecasts",
            "readings",
        ]
        self.valid_models_tuple = (
            {
                "modelID": 1,
                "modelName": "ECMWF",
            },
            {
                "modelID": 2,
                "modelName": "GFS",
            },
            {
                "modelID": 3,
                "modelName": "ICON",
            },
            {
                "modelID": 4,
                "modelName": "MBLUE",
            },
            {
                "modelID": 5,
                "modelName": "NAM",
            },
        )

    def check_valid_model(self, passed_model_name: str) -> bool:
        """check if model is supported and model name is valid"""
        if passed_model_name in self.valid_models_list:
            return True
        return False

    def check_valid_sensor(self, passed_sensor_id: str) -> bool:
        """check if sensor is supported and sensor name is valid"""
        if passed_sensor_id in self.current_supported_sensor_list:
            return True
        return False
