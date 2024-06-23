# Documentation from:
# https://apidocs.tempestwx.com/reference/get_observations-stn-station-id
# accessed: 6/21/2024
import time
import os
from dotenv import load_dotenv, find_dotenv
import pprint
import asyncio
import aiohttp
import datetime

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
tempest_token = os.environ.get("TEMPEST_TOKEN")
tempest_station = os.environ.get("TEMPEST_STATION")
tempest_station_name = os.environ.get("TEMPEST_STATION_NAME")


async def tempest_fetch(session, url):
    headers = {"accept": "application/json"}
    async with session.get(url, headers=headers) as response:
        return await response.json(), response.status


async def query_tempest(
    tempest_station_name: str,
    tempest_token: str,
    tempest_station: str = "134520",
    time_start_epoch: float = 0.0,
    time_end_epoch: float = 0.0,
    DEBUG: bool = False,
) -> tuple:
    tempest_token = str(tempest_token).strip()
    tempest_station = str(tempest_station)
    tempest_station_name = str(tempest_station_name).strip()
    # time_start_epoch = str(time_start_epoch)
    # time_end_epoch = str(time_end_epoch)
    # time_url = f"https://swd.weatherflow.com/swd/rest/observations/stn/{tempest_station}?token={tempest_token}&time_start={time_start_epoch}&time_end={time_end_epoch}&bucket=1&units_temp=f&units_wind=mph&units_pressure=mb&units_precip=in&units_distance=mi"
    url = f"https://swd.weatherflow.com/swd/rest/observations/stn/{tempest_station}?token={tempest_token}&bucket=1&units_temp=f&units_wind=mph&units_pressure=mb&units_precip=in&units_distance=mi"

    async with aiohttp.ClientSession() as session:
        json_object, status_code = await tempest_fetch(session, url)
    print("Tempest Query returned status code: " + str(status_code))
    # now let's convert this into the holfuy formatting for ease of useage
    if status_code == 200:
        if DEBUG:
            pprint.pp(json_object, indent=4)
        json_object = {
            "stationId": json_object["station_id"],
            "stationName": tempest_station_name,
            "dateTime": datetime.datetime.fromtimestamp(
                json_object["obs"][0][0]
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "wind": {
                "speed": json_object["obs"][0][3],
                "gust": json_object["obs"][0][4],
                "min": json_object["obs"][0][2],
                "unit": json_object["units"]["units_wind"],
                "direction": json_object["obs"][0][5],
                "station_pressure": json_object["obs"][0][6],
                "sea_level_pressure": json_object["obs"][0][7],
            },
            "temperature": json_object["obs"][0][8],
        }
        if DEBUG:
            print("CONVERTED JSON OBJECT:")
            pprint.pp(json_object, indent=4)
    return [
        json_object,
    ], [
        status_code,
    ]


if __name__ == "__main__":
    seconds = time.time()
    #print("Epoch Seconds: ", seconds)
    loop = asyncio.get_event_loop()
    response, status = loop.run_until_complete(
        query_tempest(
            tempest_station_name="Sandia Soaring Peak Tempest",
            tempest_token=tempest_token,
            tempest_station=tempest_station,
            DEBUG=False,
        )
    )
