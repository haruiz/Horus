import requests
from config import config

def get_tamu_bus_next_stop(route_number):
   endpoint = "{}/{}/TimeTable".format(config["TAMU_ROUTES"]["ENDPOINT"], route_number)
   response = requests.get(endpoint)
   return response.json()

def joke_of_the_day():
   url = 'https://api.jokes.one/jod?category=knock-knock'
   response = requests.get(url)
   jokes=response.json()['contents']['jokes'][0]
   return jokes["joke"]["text"]



