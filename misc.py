import re
from datetime import datetime

import requests

from config import config


def get_tamu_bus_next_stop(route_number) -> str:
    # get timetable
    endpoint="{}/{}/TimeTable".format(config["TAMU_ROUTES"]["ENDPOINT"],route_number)
    response=requests.get(endpoint)
    timetable=response.json()
    if len(timetable) <= 1:
        return 'No service is scheduled for this date'
    leave_campus=[]
    arrive=[]
    for interval in timetable:
        temp=list(interval.items())
        leave_campus.append(temp[0])
        arrive.extend(temp[1:])
    # get waypoints
    waypoints=_get_waypoints(timetable)
    # get current time
    curr_time=datetime.strftime(datetime.now(),"%H:%M")

    msg=''
    for location in waypoints[:-1]:

        next_time=_get_matching(arrive,location,curr_time)

        if next_time is None:
            # warn the user
            msg+='No bus available...'
            break
        else:
            # tell user the next bus arriving time
            time_left=(datetime.strptime(next_time,"%H:%M")-datetime.strptime(curr_time,"%H:%M")).seconds
            hour_left=time_left//3600
            minute_left=(time_left%3600)//60
            if hour_left > 1:
                msg+="The next bus will arrive at {} in {} hours and {} minutes...".format(location,hour_left,
                                                                                           minute_left)
            elif hour_left == 1:
                msg+="The next bus will arrive at {} in {} hour and {} minutes...".format(location,hour_left,
                                                                                          minute_left)
            else:
                msg+="The next bus will arrive at {} in {} minutes...".format(location,minute_left)
    next_time=_get_matching(leave_campus,waypoints[-1],curr_time)
    if next_time:
        time_left=(datetime.strptime(next_time,"%H:%M")-datetime.strptime(curr_time,"%H:%M")).seconds
        hour_left=time_left//3600
        minute_left=(time_left%3600)//60
        if hour_left > 1:
            msg+="The next bus will leave {} in {} hours and {} minutes...".format(waypoints[-1],hour_left,minute_left)
        elif hour_left == 1:
            msg+="The next bus will leave {} in {} hour and {} minutes...".format(waypoints[-1],hour_left,minute_left)
        else:
            msg+="The next bus will leave {} in {} minutes...".format(waypoints[-1],minute_left)

    return msg


def _get_waypoints(timetable: dict) -> list:
    waypoints=[]
    tour=timetable[0]
    for key in tour:
        start=re.search("[A-Z]",key).span()[0]
        waypoints.append(key[start:])
    return waypoints


def _get_matching(timetable: list,location: str,curr_time: str) -> str:
    res=['00:00']
    next_time=''
    for pair in timetable:
        key,value=pair
        if value is None:
            continue
        if re.search(location,key):
            t=datetime.strptime('{}'.format(value),"%I:%M %p")
            res.append(datetime.strftime(t,"%H:%M"))
    for i in range(1,len(res)):
        if res[i-1] < curr_time <= res[i]:
            return res[i]
    return None


def joke_of_the_day():
    url='https://api.jokes.one/jod?category=knock-knock'
    response=requests.get(url)
    jokes=response.json()['contents']['jokes'][0]
    return jokes["joke"]["text"]

    # return response.json()


if __name__ == '__main__':
    # curr_time = "03:20"
    msg=get_tamu_bus_next_stop('26')
    print(msg)
