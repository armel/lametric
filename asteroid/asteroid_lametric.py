#!/usr/local/bin/python

import requests
import datetime
import time
import json
import os

# --- constants & variables

http = "http://www.neowsapp.com/rest/v1/feed"
file = "asteroid.json"

data = {
    "frames": []
}


# -- public functions

# ---- add name

def add_name(text, icon):

    value = {
        "text": text,
        "icon": icon
    }

    data["frames"].append(value)


# ---- add sparkline

def add_sparkline(chart):

    value = {
        "chartData":
            chart
    }

    data["frames"].append(value)

# -- main loop

def main():
    # set date

    now = datetime.datetime.now()

    today = now.strftime("%Y-%m-%d")
    delta = (now + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
    year = now.strftime("%Y")

    # check file

    if os.path.isfile(file):
        modify = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d")

    if not os.path.isfile(file) or modify != today:     # if necessary update file
        try:
            r = requests.get(http+"?start_date="+today+"&end_date="+delta+"&detailed=false")
            f = open(file, 'w')
            f.write(r.content)
            f.close

            asteroid = json.loads(r.content)
        except:
            with open(file) as data_file:
                asteroid = json.load(data_file)
    else:
        with open(file) as data_file:
            asteroid = json.load(data_file)

    # analyse file

    count = 0
    message = []

    for i in asteroid["near_earth_objects"][today]:
        name = i["name"]

        velocity = i["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]
        velocity = str("%d" % float(velocity))
        velocity = "{0:,}".format(int(velocity)).replace(',', ' ')

        distance = i["close_approach_data"][0]["miss_distance"]["kilometers"]
        distance = str("%d" % float(distance))
        distance = "{0:,}".format(int(distance)).replace(',', ' ')

        magnitude = i["absolute_magnitude_h"]
        magnitude = str("%.2f" % float(magnitude))

        count += 1

        message.append(("neo %s - %s - Velocity: %s kph - Distance: %s km - Magnitude: %s" % (count, name, velocity, distance, magnitude)))

    # format frames

    add_name("today " + str(count), "a4772")

    indice = 1
    for i in message:
        add_name(i, "a4772")
        indice += 1

    total = 0
    prevision = []
    for i in xrange(0, 7):
        delta = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        count = 0
        try:
            for j in asteroid["near_earth_objects"][delta]:
                count += 1
        except:
            pass

        total += count
        prevision.append(count)

    add_name("week " + str(total), "a4772")
    add_sparkline(prevision)

    # post frames

    print
    print json.dumps(data, indent=4, separators=(",", ": "))

if __name__ == '__main__':
    main()
