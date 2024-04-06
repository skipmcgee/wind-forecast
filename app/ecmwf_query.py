import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def query_ecmwf(query_lat: float, query_long: float) -> tuple:
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)
	
	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/ecmwf"
	params = {
		"latitude": query_lat,
		"longitude": query_long,
		"hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "weather_code", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_direction_100m", "surface_temperature", "cape"],
		"temperature_unit": "fahrenheit",
		"wind_speed_unit": "mph",
		"precipitation_unit": "inch",
		"forecast_days": 7,
		"models": ["ecmwf_ifs025", "ecmwf_aifs025"]
	}
	responses = openmeteo.weather_api(url, params=params)
	
	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
	
	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
	hourly_weather_code = hourly.Variables(4).ValuesAsNumpy()
	hourly_pressure_msl = hourly.Variables(5).ValuesAsNumpy()
	hourly_surface_pressure = hourly.Variables(6).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(7).ValuesAsNumpy()
	hourly_wind_speed_100m = hourly.Variables(8).ValuesAsNumpy()
	hourly_wind_direction_10m = hourly.Variables(9).ValuesAsNumpy()
	hourly_wind_direction_100m = hourly.Variables(10).ValuesAsNumpy()
	hourly_surface_temperature = hourly.Variables(11).ValuesAsNumpy()
	hourly_cape = hourly.Variables(12).ValuesAsNumpy()
	
	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["apparent_temperature"] = hourly_apparent_temperature
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["weather_code"] = hourly_weather_code
	hourly_data["pressure_msl"] = hourly_pressure_msl
	hourly_data["surface_pressure"] = hourly_surface_pressure
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
	hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
	hourly_data["wind_direction_100m"] = hourly_wind_direction_100m
	hourly_data["surface_temperature"] = hourly_surface_temperature
	hourly_data["cape"] = hourly_cape
	
	hourly_dataframe = pd.DataFrame(data = hourly_data)
	print(hourly_dataframe)
