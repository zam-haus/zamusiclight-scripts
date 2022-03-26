#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2019-2022 Thomas Kolb
# This file is licensed under the terms of the MIT license. See COPYING for
# details.

# Importieren von sk6812_multistrip.py, welches das Netzwerkprotokoll für die
# LED-Leiste abstrahiert.
import sk6812_multistrip as sk6812

import time    # für sleep()
import sys     # zum Lesen der IP-Adresse aus den Kommandozeilenargumenten

import math

# Konstanten
NLED   = 150     # Anzahl der LEDs pro logischen Strip
NSTRIP = 2       # Anzahl der logischen Strips

# Objekt initialisieren
s = sk6812.SK6812(sys.argv[1], 2703)

# Wartezeit zwischen den Animationsschritten. Achtung, die LED-Leiste arbeitet
# immer mit 60 FPS! Dies ist insbesondere bei Verwendung von fade_color()
# relevant.
interval = 1.0/60

# Globale Skalierung für die Helligkeit.
scale = 0.5

# Startzeitpunkt der Animation
t0 = time.time()

# Hauptschleife
while True:
    # hole die aktuelle Zeit seit dem Start
    t = time.time() - t0

    # umskalieren in einen langsam fortschreitenden Phasenwert
    phase = t * 2*math.pi / 739.0

    # Laufe über alle LEDs in allen Strips ...
    for strip in range(NSTRIP):
        for i in range(NLED):
            # ... berechne für jede LED eine individuelle Farbe ...

            # Der Wertebereich ist 0 bis 255 für jeden Kanal. Es gibt vier
            # Kanäle: rot, grün, blau und weiß. Da weiß um einiges intensiver
            # als die anderen Kanäle ist, wird dieser hier pauschal auf 60%
            # gedimmt.
            x = 2*math.pi * i / NLED
            r = scale * (127 + 127 * math.sin(x + 283*phase + 0 * math.pi/2))
            g = scale * (127 + 127 * math.sin(x + 293*phase + 1 * math.pi/2))
            b = scale * (127 + 127 * math.sin(x + 307*phase + 2 * math.pi/2))
            w = scale * 0.6 * (127 + 127 * math.sin(x +  311*phase + 3 * math.pi/2))

            # ... und setze diese direkt
            s.set_color(strip, i, r, g, b, w)

        s.commit() # sendet alle bisherigen Befehle an die LED-Leiste. Muss
                   # spätestens nach 210 Befehlen aufgerufen werden!

    # Warte bis zum nächsten Frame
    time.sleep(interval)

