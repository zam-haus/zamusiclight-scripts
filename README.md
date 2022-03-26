# Skripte für das ZAMusiclight

## Was?

_ZAMusiclight_ ist eine öffentlich zugängliche LED-Installation im [Zentrum für
Austausch und Machen](https://zam.haus) in Erlangen.

Sie besteht aus einem ESP32-Mikrocontroller und einem LED-Strip mit 300
RGBW-LEDs, die einzeln über das Netzwerk angesteurt werden können.

Weitere Information gibt es im [ZAM-Wiki](https://wiki.betreiberverein.de/books/projekte-aktuell/chapter/zamusiclight).

## Über dieses Repository

Hier liegen Beispielskripte und Skripte, die von Interessierten beigesteuert wurden.

Die Skripte sind in [Python](https://python.org) geschrieben und sollten in
einer üblichen Python 3-Umgebung ohne zusätzliche Abhängigkeiten funktionieren.

## Wo anfangen?

Solltest du gerade vor dem ZAMusiclight stehen (oder sitzen) und ein Skript
schreiben wollen, schau dir am Besten `rgbw_sinus.py` an. Dieses Skript ist
ausführlich kommentiert.

Es kann wie folgt gestartet werden, wobei `10.233.0.118` die aktuelle
IP-Adresse des ZAMusiclight-ESP32 ist:

```
./rgbw_sinus.py 10.233.0.118
```

## Lizenz

Alle Skripte stehen unter der MIT-Lizenz (siehe [COPYING](./COPYING)).
