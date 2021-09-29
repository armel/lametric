#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import json
import csv

# --- constants & variables

file = "morse.csv"

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

    morse = {}
    reader = csv.reader(open(file, 'r'))
    for row in reader:
        letter, code = row
        morse[letter] = code

    letter = random.choice(morse.keys())
    code = morse[letter]
    recode = code.replace('.', '·')

    spell = ''

    for char in code:
        if char == '-':
            spell += 'dash'
        else:
            spell += 'dot'
        spell += ' '

    # format frame

    add_name(str(letter), "a11188")
    add_name(str(recode), "a11188")
    add_name(str(spell), "a11188")

    # post frame

    print
    print json.dumps(data, indent=4, separators=(",", ": "))

if __name__ == '__main__':
    main()
