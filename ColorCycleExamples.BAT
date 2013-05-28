@echo off
REM red = 0
REM orange = 5632
REM yellow = 15104
REM green = 25500
REM blue = 46920
REM purple = 49955
REM magenta = 60160
REM red = 65535
REM white = -1
REM indigo = 47883

REM This batch file is not actually intended to be run as a whole.
REM It's really just a convenient spot for collecting ColorCycle command lines.

REM rainbow
c:\python32\python ColorCycle.py -t 60 0 5632 15104 25500 46920 47883 49955 60160 -1
REM rainbow snap
c:\python32\python ColorCycle.py -100 0 5632 15104 25500 46920 47883 49955 60160 -1

REM RGB
c:\python32\python ColorCycle.py -50 0 25500 46920

REM St. Paddy's Day
c:\python32\python ColorCycle.py -t 20 25500 -1 5632
REM 'Murrica
c:\python32\python ColorCycle.py -t 20 0 -1 46920
REM Christmas
c:\python32\python ColorCycle.py -t 20 0 -1 25500
REM Easter
c:\python32\python ColorCycle.py -t 60 -s 175 0 5632 15104 25500 46920 47883 49955 60160 -1

REM Night moves
c:\python32\python ColorCycle.py -t 30 -bLC 30 -bH 0 0 46920 47883 49955
REM Set lights low and exit
c:\python32\python ColorCycle.py 0.0 -bLC 30 -bH 0 0 46920 47883 49955
