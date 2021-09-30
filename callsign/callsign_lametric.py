#!/usr/bin/env python

import cgi
import json

# --- constants & variables

data = {
    "frames": []
}

callsign = "F4HWN"

try:
    arg = cgi.FieldStorage()
    callsign = arg['Callsign'].value

except:
    pass


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

    add_name(callsign, "a11188")
    add_name("ON AIR", "a11188")

    # post frame

    print
    print json.dumps(data, indent=4, separators=(",", ": "))

if __name__ == '__main__':
    main()
