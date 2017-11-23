#!/usr/bin/env python

import random
import json

# --- constants & variables

file = "indicatif.dat"

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

    # analyse file

    line = random.choice(open(file).readlines())
    line = line.strip()
    element = line.split(';')

    # format frame

    for i in xrange(0, len(element)):
        add_name(element[i], "a4297")

    # post frame

    print
    print json.dumps(data, indent=4, separators=(",", ": "))

if __name__ == '__main__':
    main()
