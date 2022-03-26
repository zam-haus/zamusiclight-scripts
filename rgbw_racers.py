#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2022 Julian Hammer
# This file is licensed under the terms of the MIT license. See COPYING for
# details.

# Importieren von sk6812_multistrip.py, welches das Netzwerkprotokoll für die
# LED-Leiste abstrahiert.
import sk6812_multistrip as sk6812

import time    # für sleep()
import sys     # zum Lesen der IP-Adresse aus den Kommandozeilenargumenten

import math
import random
import colorsys

# Konstanten
NLED   = 150     # Anzahl der LEDs pro logischen Strip
NSTRIP = 2       # Anzahl der logischen Strips

# Objekt initialisieren
s = sk6812.SK6812(sys.argv[1], 2703)

# Wartezeit zwischen den Animationsschritten. Achtung, die LED-Leiste arbeitet
# immer mit 60 FPS! Dies ist insbesondere bei Verwendung von fade_color()
# relevant.
interval = 1.0/60

last_frame = [(0,0,0,0)] * NLED * NSTRIP

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def random_color():
    return list(hsv2rgb(random.random(), 1, 1)) + [random.randint(0,255)]

def loc2sl(loc):
    # translates 1d-coordinate (loc) to
    # (strip, led) with:
    # (0,0) ... (0, 149) (1, 149) ... (1, 0)
    strip = loc // NLED
    led = loc % NLED
    if strip == 1:
        led = NLED - led
    return strip, led

MAXLOC = NLED*NSTRIP

racers = [
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.3),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.3),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.3),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.3),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.3),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.3),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.3),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.3),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.5),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.5),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.5),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*0.5),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*2),
    dict(loc=random.randint(0,299), color=random_color(), speed=(random.random()-0.5)*2),
]

# Clear all leds at start
for loc in range(MAXLOC):
    strip, led = loc2sl(loc)
    s.set_color(strip, led, 0,0,0,0)
    if loc % 150 == 0:
        s.commit()
s.commit()


print("{:>10} {:>8} {:>8}".format("frame", "AVG", "MAX"))
# Hauptschleife
f = 0  # frame counter
clear_leds = []
while True:
    for strip, led in clear_leds:
        # Clear leds
        s.set_color(strip, led, 0,0,0,0)
    clear_leds = []
        
    for r in racers:
        # Update location
        r['loc'] += r['speed']
        # Reverse at ends (0 and MAXLOC-1)
        if r['loc'] >= MAXLOC:
            r['loc'] = MAXLOC - (r['loc'] % MAXLOC)
            r['speed'] *= -1
        if r['loc'] < 0:
            r['loc'] *= -1
            r['speed'] *= -1

        # Interpolate color linearly between two leds
        strip, led = loc2sl(int(r['loc']))
        s.add_color(strip, led, *tuple([int(c*(math.ceil(r['loc'])-r['loc'])) for c in r['color']]))
        clear_leds.append((strip, led))
        strip, led = loc2sl(math.ceil(r['loc']))
        s.add_color(strip, led, *tuple([int(c*(r['loc']-int(r['loc']))) for c in r['color']]))
        clear_leds.append((strip, led))

        # Add tail of speed-depending length and logarithmicly decaying brightness
        tail = r['speed'] * 10
        if tail > 0:
            tail_range = range(1, int(tail))
        else:
            tail_range = range(-1, int(tail), -1)
        for i in tail_range:
            if not 0 <= int(r['loc'])-i < MAXLOC:
                continue
            strip, led = loc2sl(int(r['loc'])-i)
            color = tuple([int(c / (abs(i)*(abs(tail)/2)) ) for c in r['color'][:3]]+[0])  # blackout white
            s.add_color(strip, led, *color)
            clear_leds.append((strip, led))
        # last tail segment is interpolated
        if tail_range:
            if not 0 <= int(r['loc'])-i < MAXLOC:
                continue
            last_loc = r['loc']-i
            strip, led = loc2sl(math.ceil(last_loc))
            s.add_color(strip, led, *tuple([int(c*(last_loc-int(last_loc))) for c in color]))
            clear_leds.append((strip, led))

        # Random speed variation, limited to [-2, 2] interval
        r['speed'] = max(-2, min(2, r['speed'] + (random.random()-0.5)*0.01))

        # Use speed to define W-intensity ("whiteness")
        r['color'][3] = min(int(abs(r['speed'])*128), 255)

    if f % 600 == 0:
        print("{:>10} {:>8.2f} {:>8.2f}".format(
            f,
            sum([abs(r['speed']) for r in racers])/len(racers),
            max([abs(r['speed']) for r in racers])))

    s.commit()

    # Warte bis zum nächsten Frame
    time.sleep(interval)
    f += 1
