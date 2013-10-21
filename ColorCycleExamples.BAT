@echo off
REM red = 0
REM orange = 5632
REM yellow = 15104
REM green = 25500
REM blue = 46920
REM indigo = 47883
REM purple = 49955
REM magenta = 60160
REM red = 65535
REM white = -1
REM black (off) = -2

REM Office = 10 12 15 19
REM Bedroom = 6 7 13 14 16 18
REM Living Room and Entryway = 1 2 3 4 8 9 11
REM Tina`s Room = 17
REM Everything Except Front Porch = 6 7 13 14 16 18  10 12 15 19  1 2 3 4 8 9 11  17  20 21

REM This batch file is not actually intended to be run as a whole.
REM It is really just a convenient spot for collecting ColorCycle command lines.
goto end

REM rainbow
c:\python32\python ColorCycle.py -t 60 0 5632 15104 25500 46920 47883 49955 60160 -1
REM rainbow snap
c:\python32\python ColorCycle.py -100 0 5632 15104 25500 46920 47883 49955 60160 -1

REM RGB
c:\python32\python ColorCycle.py -50 0 25500 46920

REM St. Paddy`s Day
c:\python32\python ColorCycle.py -t 20 25500 -1 5632

REM `Murrica [bright, dim]
c:\python32\python ColorCycle.py -t 20 0 -1 46920
c:\python32\python ColorCycle.py -v -o -t 7 -w 233 -bLC 30 -bH 0  0 -1 46920

REM Christmas
c:\python32\python ColorCycle.py -t 20 0 -1 25500
REM Easter
c:\python32\python ColorCycle.py -t 60 -s 175 0 5632 15104 25500 46920 47883 49955 60160 -1

REM Night moves
c:\python32\python ColorCycle.py -v -t 20 -w 160 -bLC 30 -bH 0 -bLS 0  0 46920 47883 49955
title Office mono
c:\python32\python ColorCycle.py -v -t 20 -w 160 -b 30 -m 0 46920 47883 49955 -i 10 12 15 19
title Bedroom mono
c:\python32\python ColorCycle.py -v -t 20 -w 160 -b 30 -m 0 46920 47883 49955 -i 6 7 13 14 16 18
title House Interior mono
c:\python32\python ColorCycle.py -v -t 20 -w 160 -b 30 -m 0 46920 47883 49955 -i 6 7 13 14 16 18  10 12 15 19  1 2 3 4 8 9 11  17  20 21

REM Set lights low and exit
c:\python32\python ColorCycle.py 0.0 -bLC 30 -bH 0 0 46920 47883 49955

REM Set phasers to Energize
c:\python32\python ColorCycle.py 0.0 -bLC 203 -s 232 34495

REM Monochrome night moves
c:\python32\python ColorCycle.py -m -t 60 -bLC 30 -bH 0 0 46920 47883 49955

REM SetBulb example
c:\python32\python SetBulbXY.py -v -t 0.0 -b 254 -xy 0.3 0.9
c:\python32\python SetBulbXY_forPEST.py -v -t 0.0 -b 153.93 -xy 0.3 0.9

REM ordered rainbow snap
c:\python32\python ColorCycle.py -100 -o 0 5632 15104 25500 46920 47883 49955 60160 -1

REM quick, ordered rainbow snap with bulbs specified
c:\python32\python ColorCycle.py -o -t -3  0 5632 15104 25500 46920 47883 49955 60160 -i 10 12 13 14 15

REM NEW STYLE
c:\python32\python ColorCycle.py -v -t 120 -c 0 5632 -m -o -b 30 -i 6 7 13 14 16 18  10 12 15 19  1 2 3 4 8 9 11  17  20 21
title Random Night Colors
c:\python32\python ColorCycle.py -v -t 3 -w 120 -b 1 -c 0 5632 49955 60160 -i 6 7 13 14 16 18  10 12 15 19  1 2 3 4 8 9 11  17  20 21

REM Redshift
title Redshift
c:\python32\python ColorCycle.py -v -t 10 -b 254 250 245 240 -c 63000 63500 64000 64500 65000 65535 0 500 1000 1500 2000 -i 6 7 13 14 16 18  10 12 15 19 -d 120 -s 254 250 245 240 235


REM Debugging
c:\python32\python ColorCycle.py -v -t 3 -b 254 250 240 230 220 210 -c 5632 15104 40000 -i 10 12 15 19 -d 0.25 -s 254 200 150 100 -o
:end
