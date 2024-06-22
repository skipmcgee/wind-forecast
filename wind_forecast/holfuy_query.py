# Date: 05/30/2024
# Based on
# used the Holfuy API Documentation to create this code
# Source URL: https://api.holfuy.com/live/
import asyncio
import aiohttp
import pprint
import os
from dotenv import load_dotenv, find_dotenv

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
holfuy_token = os.environ.get("HOLFUY_TOKEN")
holfuy_station = os.environ.get("HOLFUY_STATION")


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json(), response.status


async def gather_data(holfuy_token: str, holfuy_station: str = '1151', DEBUG=False) -> tuple:
    base_url = "https://api.holfuy.com/live/?"
    info_type = "JSON"
    wind_speed_units = "mph"
    wind_average_options_tuple = (2,)  # (0, 1, 2)
    urls = []
    for wind_avg in wind_average_options_tuple:
        url = f"{base_url}s={holfuy_station}&pw={holfuy_token}&avg={wind_avg}&m={info_type}&su={wind_speed_units}&utc&loc&tu=F&daily"
        if DEBUG:
            print("Holfuy URL: " + url)
        urls.append(url)
    valid_obj_list = []
    error_obj_list = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            json_object, status_code = await fetch(session, url)
            if status_code == 200:
                if DEBUG:
                    pprint.pp(json_object, indent=4)
                valid_obj_list.append(json_object)
            else:
                print(f"Error with {str(url)}")
                print("Status Code: " + str(status_code))
                error_obj_list.append(json_object)
    return valid_obj_list, error_obj_list


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    valid_obj_list, error_obj_list = loop.run_until_complete(gather_data(holfuy_token))
    pprint.pp(valid_obj_list, indent=4)