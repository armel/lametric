#!/usr/bin/env python

import requests
import datetime
import json
import csv
import os

# --- constants & variables

http = "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt"
file = "exoplanet.csv"

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


# -- main loop

def main():
    # set date

    now = datetime.datetime.now()

    today = now.strftime("%Y-%m-%d")
    year = now.strftime("%Y")

    # check file

    if os.path.isfile(file):
        update = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d")

    if not os.path.isfile(file) or update != today:
        r = requests.get(http)
        f = open(file, 'w')
        f.write(r.content)
        f.close

    # analyse file

    total = 0
    total_this_year = 0

    for row in open(file, "rb"):
        if not row.startswith("#"):
            element = row.split(',')
            if element[14] == year:
                total_this_year += 1
            total += 1

    # format frame

    add_name(str(total), "a4749")
    add_name("+" + str(total_this_year), "a4749")

    # post frame

    print
    print json.dumps(data, indent=4, separators=(",", ": "))

if __name__ == '__main__':
    main()
