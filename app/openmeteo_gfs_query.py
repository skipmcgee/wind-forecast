import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry


def query_gfs(query_lat: float, query_long: float) -> tuple:
  print(f"query_gfs started for lat: {str(query_lat)}, long: {str(query_long)}")

  # Setup the Open-Meteo API client with cache and retry on error
  cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
  retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
  openmeteo = openmeteo_requests.Client(session = retry_session)

  # Make sure all required weather variables are listed here
  # The order of variables in hourly or daily is important to assign them correctly below
  url = "https://api.open-meteo.com/v1/gfs"
  params = {
  	"latitude": query_lat,
    "longitude": query_long,
  "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "weather_code", "pressure_msl", "surface_pressure", "visibility", "wind_speed_10m", "wind_speed_80m", "wind_direction_10m", "wind_direction_80m", "wind_gusts_10m", "temperature_80m", "is_day", "cape", "lifted_index", "convective_inhibition"],
  	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max", "uv_index_clear_sky_max", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum"],
  	"minutely_15": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "weather_code", "wind_speed_10m", "wind_speed_80m", "wind_direction_10m", "wind_direction_80m", "wind_gusts_10m", "visibility", "cape", "is_day"],
  	"temperature_unit": "fahrenheit",
  	"wind_speed_unit": "mph",
  	"precipitation_unit": "inch",
  	"timezone": "America/Denver",
  	"models": ["gfs_seamless", "gfs_global", "gfs_hrrr", "gfs_graphcast025"]
  }
  responses = openmeteo.weather_api(url, params=params)
  
  # Process first location. Add a for-loop for multiple locations or weather models
  response = responses[0]
  print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
  print(f"Elevation {response.Elevation()} m asl")
  print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
  print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
  
  # Process minutely_15 data. The order of variables needs to be the same as requested.
  minutely_15 = response.Minutely15()
  minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()
  minutely_15_relative_humidity_2m = minutely_15.Variables(1).ValuesAsNumpy()
  minutely_15_apparent_temperature = minutely_15.Variables(2).ValuesAsNumpy()
  minutely_15_precipitation = minutely_15.Variables(3).ValuesAsNumpy()
  minutely_15_weather_code = minutely_15.Variables(4).ValuesAsNumpy()
  minutely_15_wind_speed_10m = minutely_15.Variables(5).ValuesAsNumpy()
  minutely_15_wind_speed_80m = minutely_15.Variables(6).ValuesAsNumpy()
  minutely_15_wind_direction_10m = minutely_15.Variables(7).ValuesAsNumpy()
  minutely_15_wind_direction_80m = minutely_15.Variables(8).ValuesAsNumpy()
  minutely_15_wind_gusts_10m = minutely_15.Variables(9).ValuesAsNumpy()
  minutely_15_visibility = minutely_15.Variables(10).ValuesAsNumpy()
  minutely_15_cape = minutely_15.Variables(11).ValuesAsNumpy()
  minutely_15_is_day = minutely_15.Variables(12).ValuesAsNumpy()
  
  minutely_15_data = {"date": pd.date_range(
  	start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
  	end = pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
  	freq = pd.Timedelta(seconds = minutely_15.Interval()),
  	inclusive = "left"
  )}
  minutely_15_data["temperature_2m"] = minutely_15_temperature_2m
  minutely_15_data["relative_humidity_2m"] = minutely_15_relative_humidity_2m
  minutely_15_data["apparent_temperature"] = minutely_15_apparent_temperature
  minutely_15_data["precipitation"] = minutely_15_precipitation
  minutely_15_data["weather_code"] = minutely_15_weather_code
  minutely_15_data["wind_speed_10m"] = minutely_15_wind_speed_10m
  minutely_15_data["wind_speed_80m"] = minutely_15_wind_speed_80m
  minutely_15_data["wind_direction_10m"] = minutely_15_wind_direction_10m
  minutely_15_data["wind_direction_80m"] = minutely_15_wind_direction_80m
  minutely_15_data["wind_gusts_10m"] = minutely_15_wind_gusts_10m
  minutely_15_data["visibility"] = minutely_15_visibility
  minutely_15_data["cape"] = minutely_15_cape
  minutely_15_data["is_day"] = minutely_15_is_day
  
  minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
  print(minutely_15_dataframe)
  
  # Process hourly data. The order of variables needs to be the same as requested.
  hourly = response.Hourly()
  hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
  hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
  hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
  hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()
  hourly_pressure_msl = hourly.Variables(4).ValuesAsNumpy()
  hourly_surface_pressure = hourly.Variables(5).ValuesAsNumpy()
  hourly_visibility = hourly.Variables(6).ValuesAsNumpy()
  hourly_wind_speed_10m = hourly.Variables(7).ValuesAsNumpy()
  hourly_wind_speed_80m = hourly.Variables(8).ValuesAsNumpy()
  hourly_wind_direction_10m = hourly.Variables(9).ValuesAsNumpy()
  hourly_wind_direction_80m = hourly.Variables(10).ValuesAsNumpy()
  hourly_wind_gusts_10m = hourly.Variables(11).ValuesAsNumpy()
  hourly_temperature_80m = hourly.Variables(12).ValuesAsNumpy()
  hourly_is_day = hourly.Variables(13).ValuesAsNumpy()
  hourly_cape = hourly.Variables(14).ValuesAsNumpy()
  hourly_lifted_index = hourly.Variables(15).ValuesAsNumpy()
  hourly_convective_inhibition = hourly.Variables(16).ValuesAsNumpy()
  
  hourly_data = {"date": pd.date_range(
  	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
  	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
  	freq = pd.Timedelta(seconds = hourly.Interval()),
  	inclusive = "left"
  )}
  hourly_data["temperature_2m"] = hourly_temperature_2m
  hourly_data["precipitation_probability"] = hourly_precipitation_probability
  hourly_data["precipitation"] = hourly_precipitation
  hourly_data["weather_code"] = hourly_weather_code
  hourly_data["pressure_msl"] = hourly_pressure_msl
  hourly_data["surface_pressure"] = hourly_surface_pressure
  hourly_data["visibility"] = hourly_visibility
  hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
  hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
  hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
  hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
  hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
  hourly_data["temperature_80m"] = hourly_temperature_80m
  hourly_data["is_day"] = hourly_is_day
  hourly_data["cape"] = hourly_cape
  hourly_data["lifted_index"] = hourly_lifted_index
  hourly_data["convective_inhibition"] = hourly_convective_inhibition
  
  hourly_dataframe = pd.DataFrame(data = hourly_data)
  print(hourly_dataframe)
  
  # Process daily data. The order of variables needs to be the same as requested.
  daily = response.Daily()
  daily_weather_code = daily.Variables(0).ValuesAsNumpy()
  daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
  daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
  daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
  daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
  daily_sunrise = daily.Variables(5).ValuesAsNumpy()
  daily_sunset = daily.Variables(6).ValuesAsNumpy()
  daily_daylight_duration = daily.Variables(7).ValuesAsNumpy()
  daily_sunshine_duration = daily.Variables(8).ValuesAsNumpy()
  daily_uv_index_max = daily.Variables(9).ValuesAsNumpy()
  daily_uv_index_clear_sky_max = daily.Variables(10).ValuesAsNumpy()
  daily_precipitation_sum = daily.Variables(11).ValuesAsNumpy()
  daily_rain_sum = daily.Variables(12).ValuesAsNumpy()
  daily_showers_sum = daily.Variables(13).ValuesAsNumpy()
  daily_snowfall_sum = daily.Variables(14).ValuesAsNumpy()
  
  daily_data = {"date": pd.date_range(
  	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
  	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
  	freq = pd.Timedelta(seconds = daily.Interval()),
  	inclusive = "left"
  )}
  daily_data["weather_code"] = daily_weather_code
  daily_data["temperature_2m_max"] = daily_temperature_2m_max
  daily_data["temperature_2m_min"] = daily_temperature_2m_min
  daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
  daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
  daily_data["sunrise"] = daily_sunrise
  daily_data["sunset"] = daily_sunset
  daily_data["daylight_duration"] = daily_daylight_duration
  daily_data["sunshine_duration"] = daily_sunshine_duration
  daily_data["uv_index_max"] = daily_uv_index_max
  daily_data["uv_index_clear_sky_max"] = daily_uv_index_clear_sky_max
  daily_data["precipitation_sum"] = daily_precipitation_sum
  daily_data["rain_sum"] = daily_rain_sum
  daily_data["showers_sum"] = daily_showers_sum
  daily_data["snowfall_sum"] = daily_snowfall_sum
  
  daily_dataframe = pd.DataFrame(data = daily_data)
  print(daily_dataframe)

  # figure out return of values to process


if __name__ == "__main__":
  query_gfs('35.562', '-106.226')