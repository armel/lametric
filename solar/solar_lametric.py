#!/usr/bin/env python

import requests
import os
import json
from lxml import etree
from datetime import datetime, timedelta
from time import sleep

# --- constants & variables

http = "http://www.hamqsl.com/solarxml.php"
file = "data/solar.xml"

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

    now = datetime.now() - timedelta(minutes=60)
    today = format(now, "%Y-%m-%d %H:%M:%S")

    # check file

    if os.path.isfile(file):
        modify = datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d %H:%M:%S")

    # print today, modify

    if not os.path.isfile(file) or today > modify:     # if necessary update file
        r = requests.get(http)
        f = open(file, 'w')
        f.write(r.content)
        f.close
        solar = etree.fromstring(r.content)
    else:
        solar = etree.parse(file)

    # update
    for value in solar.xpath("/solar/solardata/updated"):
        updated = value.text.strip()
    # sfi solar flux index:
    for value in solar.xpath("/solar/solardata/solarflux"):
        solarflux = value.text.strip()
    # sn sunspot number
    for value in solar.xpath("/solar/solardata/sunspots"):
        sunspots = value.text.strip()
    # a-index
    for value in solar.xpath("/solar/solardata/aindex"):
        aindex = value.text.strip()
    # k-index
    for value in solar.xpath("/solar/solardata/kindex"):
        kindex = value.text.strip()
    # k-index nt
    for value in solar.xpath("/solar/solardata/kindexnt"):
        kindexnt = value.text.strip()
    # x-ray
    for value in solar.xpath("/solar/solardata/xray"):
        xray = value.text.strip()
    # aurora
    for value in solar.xpath("/solar/solardata/aurora"):
        aurora = value.text.strip()
    # normalisation
    for value in solar.xpath("/solar/solardata/normalization"):
        normalization = value.text.strip()
    # protonflux
    for value in solar.xpath("/solar/solardata/protonflux"):
        protonflux = value.text.strip()
    # electronflux
    for value in solar.xpath("/solar/solardata/electonflux"):
        electonflux = value.text.strip()
    # geomagfield
    for value in solar.xpath("/solar/solardata/geomagfield"):
        geomagfield = value.text.strip()
    # signalnoise
    for value in solar.xpath("/solar/solardata/signalnoise"):
        signalnoise = value.text.strip()
    # solarwind
    for value in solar.xpath("/solar/solardata/solarwind"):
        solarwind = value.text.strip()

    # calculatedconditions
    condition = []
    for value in solar.xpath("/solar/solardata/calculatedconditions/band"):
        condition.append(value.get("name") + " " + value.get("time") + " " + value.text.strip())

    # calculatedvhfconditions
    vhfcondition = []
    for value in solar.xpath("/solar/solardata/calculatedvhfconditions/phenomenon"):
        vhfcondition.append(value.get("name") + " " + value.get("location") + " " + value.text.strip())

    # format frames

    add_name("Last update " + str(updated), "a2245")
    add_name("SFI " + str(solarflux), "a2245")
    add_name("SN " + str(sunspots), "a2245")
    add_name("A-Index " + str(aindex), "a2245")
    if kindexnt != "No Report":
        add_name("K-Index " + str(kindex) + " / " + str(kindexnt), "a2245")
    else:
        add_name("K-Index " + str(kindex), "a2245")

    add_name("X-Ray " + str(xray), "a2245")
    add_name("Ptn Flx " + str(protonflux), "a2245")
    add_name("Elc Flx " + str(electonflux), "a2245")
    add_name("Aurora " + str(aurora) + " / " + str(normalization), "a2245")
    add_name("Solar Wind " + str(solarwind), "a2245")

    for i in xrange(0, 4):
        add_name("HF Conditions " + condition[i] + " / " + condition[i+4], "a2245")

    for i in xrange(0, 4):
        add_name("VHF Conditions " + vhfcondition[i], "a2245")

    add_name("Geomag Field " + str(geomagfield), "a2245")
    add_name("Sig Noise Lvl " + str(signalnoise), "a2245")

    # post frames

    print
    print json.dumps(data, indent=4, separators=(",", ": "))

if __name__ == '__main__':
    main()

