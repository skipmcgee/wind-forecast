import asyncio
import aiohttp
import json
from pprintjson import pprintjson as ppjson

# local imports
from app.sensor_credentials import Credentials

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json(),response.status

async def gather_data():
    creds = Credentials()
    info_type = "JSON"
    wind_speed_units = "mph"
    wind_average_options_tuple = (2,)# (0, 1, 2)
    urls = []
    for wind_avg in wind_average_options_tuple:
        url = f"{creds.holfuy_base_address}s={creds.holfuy_station_list}&pw={creds.holfuy_password}&avg={wind_avg}&m={info_type}&su={wind_speed_units}&utc&loc&tu=F&daily"
        #print("Holfuy URL: " + url)
        urls.append(url)
    valid_obj_list = []
    error_obj_list = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            json_object,status_code = await fetch(session, url)
            if status_code == 200:
                #ppjson(json_object)
                valid_obj_list.append(json_object)
            else:
                print("Status Code: " + status_code)
                error_obj_list.append(json_object)
    return valid_obj_list,error_obj_list

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    valid_obj_list,error_obj_list = loop.run_until_complete(gather_data())
