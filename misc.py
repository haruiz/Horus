import requests
from config import config

def get_tamu_bus_next_stop(route_number):
   endpoint = "{}/{}/TimeTable".format(config["TAMU_ROUTES"]["ENDPOINT"], route_number)
   response = requests.get(endpoint)
   return response.json()

