from datetime import datetime, date
import re
import requests
from config import config

def get_tamu_bus_next_stop(route_number, location):
   endpoint = "{}/{}/TimeTable".format(config["TAMU_ROUTES"]["ENDPOINT"], route_number)
   response = requests.get(endpoint)
   timetable = response.json()

   # assume we know the current location
   # get current time
   curr_time = datetime.strftime(datetime.now(), "%H:%M")
   next_time = _get_matching(timetable, location, curr_time)
   if next_time is None:
      # warn the user
      msg = 'No running buses...'
   else:
      # tell user the next bus arriving time
      print(next_time)
      time_left = datetime.strptime(next_time, "%H:%M") - datetime.strptime(curr_time, "%H:%M")
      msg = "The next bus will arrive in {}...".format(time_left)
   print(msg)

def _get_matching(timetable:dict, location:str, curr_time:str):
   res = ['00:00']
   next_time = ''
   for interval in timetable:
      for key in interval:
         if re.search(location, key):
            t = datetime.strptime(interval['{}'.format(key)], "%I:%M %p")
            res.append(datetime.strftime(t, "%H:%M"))
   for i in range(1, len(res)):
      if res[i-1] < curr_time <= res[i]:
         return res[i]
   return None

   

   #return response.json()
if __name__ == '__main__':
   location = 'Wolf Pen Creek'
   curr_time = "15:36"
   get_tamu_bus_next_stop(27, location)
