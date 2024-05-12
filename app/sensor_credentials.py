from dotenv import load_dotenv, find_dotenv
import os 

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

class Credentials():
    def __init__(self):
        self.holfuy_base_address = "https://api.holfuy.com/live/?"
        self.holfuy_station = os.environ.get("HOLFUY_STATION")
        self.holfuy_password = os.environ.get("HOLFUY_TOKEN")
        self.holfuy_bajada_id = "1151"
        self.holfuy_sandia_id = "954"
        self.holfuy_station_list = self.holfuy_bajada_id #f"{self.holfuy_bajada_id},{self.holfuy_sandia_id}"
