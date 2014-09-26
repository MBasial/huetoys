def main():
    import random as random
    random.seed()
    from time import sleep
    from time import time
    import re
    import sys
    from phue import Bridge
#    b = Bridge()
    b = Bridge('192.168.1.110')
#    b.connect()

    # command-line argument parser
    import argparse
    parser = argparse.ArgumentParser(
            prog = 'ColorCycle',
            prefix_chars = '-/',
            description = """This program takes a series of color and brightness inputs and changes bulb charateristics accordingly.
                             It assumes that lights that are on will be used. Lights are tested for 'on' status every transition.""")
    timinggroup = parser.add_mutually_exclusive_group()
    timinggroup.add_argument('-t', '--timing', help='Set tempo in seconds, decimal values allowed; positive values produce gradual changes, ' + 
                                               'negative values produce flash transitions', type=float)
    timinggroup.add_argument('-r', '--bpm', '--rate', help='Set tempo as beats per minute, decimal values allowed; positive values produce gradual changes, ' + 
                                            'negative values produce flash transitions', type=float)
    parser.add_argument('-w', '--wait', help='Set wait time separately from transition time (bpm or seconds)', type=float, default=0.0)
    parser.add_argument('-c', '--hues', '--colors', help='A list of color values the lights will cycle through (0 - 65535)', type=int, nargs='+', default=[-1])
    parser.add_argument('-b', '--brightness', help='Set bulb brightness (0 - 254, can be a list)', type=int, nargs='+', default=[254])
    parser.add_argument('-s', '--saturation', help='Set bulb color saturation (0 - 254)', type=int, nargs='+', default=[254])
    parser.add_argument('-m', '--monochrome', help='Cycle through color list with all lights the same color', action="store_true", default=False)
    parser.add_argument('-o', '--ordered', help='Cycle through color list in order (do not randomize); apparent ' +
                                                'color "chase" order will be in reverse bulb order', action="store_true", default=False)
    selectiongroup = parser.add_mutually_exclusive_group()
    selectiongroup.add_argument('-n', '--names', help='A list of bulb names to cycle through; regex OK; bulbs will be turned on', nargs='+')
    selectiongroup.add_argument('-i', '--ids', help='A list of bulb id values to cycle through; bulbs will be turned on', type=int, nargs='+')
    selectiongroup.add_argument('-nx', '--excludednames', help='Cycle through all bulbs except these; regex OK; bulbs will be turned on', nargs='+')
    selectiongroup.add_argument('-ix', '--excludedids', help='Cycle through all bulbs except these id values; bulbs will be turned on', type=int, nargs='+')
    parser.add_argument('-d', '--duration', help='Duration for which the pattern should repeat (minutes)', type=float) #, default = 0.0)
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action="store_true")
    parser.add_argument('-x', '--exit', help='Exit by turning bulbs off', action="store_true")

    # TODO: add option to print list of bulb name/ID combos (with additional option to sort by ID# or name? -d, -di, -dn for 'directory, by id, by name'?)
    # TODO: add option to print list of 'legal' named colors (green, red, energize)
    # TODO: add option to specify colors as names
    # TODO: consider using the data from this page to write color names corresponding to hues: http://en.wikipedia.org/wiki/List_of_colors_(compact)
    # TODO: add option to specify bridge IP
    # TODO: design a GUI with checkboxes, etc. for options (Kivy?)
    # TODO: add option to specify colors (and more?) as ranges, e.g. hues = [0-1000, 5000-6800, 40000-41000] would assign three colors chosen from those ranges (-cr, -br, -sr, -wr, -tr)
    # TODO: add an option that increases hue/brightness/etc. by an increment of X for each time Y -- this is a maybe
    # TODO: set up a series of testing comand lines (e.g. 0, 1, 5 bulbs, 0, 1, 5 colors, bad parameter values)
    
    args = parser.parse_args()
    if args.verbose:
        print('Verbosity set to ON')
        if args.timing is not None:
            if args.timing >= 0:
                print('Transition timing is set to ' + str(abs(args.timing)) + ' seconds with a wait time of ' + str(abs(args.wait)) + ' seconds')
            if args.timing < 0 and args.wait > 0.0:
                print('Transition timing is set to 0.0 seconds with a wait time of ' + str(abs(args.wait) + abs(args.timing)) + ' seconds')
            if args.timing == 0:
                print('Lights will be set once and program will exit')
            if args.timing >= 0:
                print('Transitions will be gradual')
            else:
                print('Transitions will be instant')
        if args.bpm is not None:
            # For bpm time specification, assume that sum(bpm, wait) = intended total bpm.
            # So for bpm=10 and wait=20, transitions should begin at a rate of 30 bpm (every 2.0 seconds)
            netbpm = abs(args.bpm) + abs(args.wait)
            print('Timing is set to ' + str(netbpm) + ' bpm with a transition/wait split of ' + 
                  str(round(abs(args.bpm) / netbpm, 0)) + '/' + str(round(abs(args.wait) / netbpm, 0)) + '%')
            if args.bpm == 0:
                print('Lights will be set once and program will exit')
            if args.bpm >= 0:
                print('Transitions will be gradual')
            else:
                print('Transitions will be instant')

        print('Hues that will be cycled through: ' + str(args.hues))
        if args.ids is not None:
            print('Bulbs that will be cycled through: ' + str(args.ids))
        if args.ordered:
            print('Colors and lamps will be cycled in the specified order')
        else:
            print('Colors and lamps will be cycled in random order')
        print('Color saturation set to: ' + str(args.saturation))
        print('Brightness set to: ' + str(args.brightness))
        if args.duration is not None:
            print('Pattern will be repeated for ' + str(args.duration) + ' minute(s)')
    
    # Convert timing/frequency to integer tenths of seconds (transitiontime).
    # Wait times are handled by sleep(), so wait time is in actual seconds.
    if args.timing is not None:
        # Frequency is in seconds
        if args.timing >= 0: 
            transitiontime = int(round(args.timing * 10, 0))
            waittime = args.wait
        else: # use negative timing to specify flash transitions
            transitiontime = 0
            waittime = -args.timing + args.wait
            # This arrangement allows a benign but nonsensical combination 
            # (e.g. flash transition of -10 seconds with a wait of 5 seconds).
            # If a negative timing and a wait time are specified, 
            # the timing and wait times will be added together.
            # This way, flipping a negative sign does not change the 
            # observed rate of changes.
    if args.bpm is not None:
        # Frequency is in bpm; netbpm is the sum of transition and wait values
        if args.bpm >= 0:
            transitiontime = int(round(60 / (args.bpm / netbpm) * 10, 0))
            waittime = 60 / (args.wait / netbpm)
        else: # use negative bpm to specify flash transitions
            transitiontime = 0
            waittime = 60 / netbpm
    if args.timing is None and args.bpm is None:
        transitiontime = 0
        waittime = 0

    # Get light names and ID numbers, and choose which lights will be active
    # Note: Bulb changes are transmitted using ID number.
    lights_in_play = b.get_light_objects('name')
    light_ids_in_play = []
    for name in lights_in_play:
        light_ids_in_play.append(int(b.get_light_id_by_name(name)))
    # Use a selection method: ID #s, names, exclude by #, exclude by name, default = all bulbs
    if args.ids is not None: # Set bulbs using ID numbers
        # Filter lights in use so that only specified bulbs are used.
        # Turn specified bulbs on.
        light_ids_in_play = [id_ for id_ in light_ids_in_play if id_ in args.ids]
        b.set_light(light_ids_in_play, 'on', True)
        lights_in_play = []
        for id_ in light_ids_in_play:
            lights_in_play.append(b.get_light(id_, 'name'))
    elif args.excludedids is not None: # Exclude bulbs using ID numbers
        # Filter lights in use so that only specified bulbs are used.
        # Turn specified bulbs on.
        light_ids_in_play = [id_ for id_ in light_ids_in_play if id_ not in args.excludedids]
        b.set_light(light_ids_in_play, 'on', True)
        lights_in_play = []
        for id_ in light_ids_in_play:
            lights_in_play.append(b.get_light(id_, 'name'))
    elif args.names is not None: # Set bulbs using names
        # Filter lights in use so that only specified bulbs are used.
        # Turn specified bulbs on.
        regex = re.compile('|'.join(args.names), re.IGNORECASE) # names joined with OR '|' connector
        # Usage note: '.*' is equivalent to DOS '*', '.' is equivalent to DOS '?'
        lights_in_play = [a for a in lights_in_play if re.search(regex, a)]
        light_ids_in_play = []
        for name in lights_in_play:
            light_ids_in_play.append(int(b.get_light_id_by_name(name)))
        b.set_light(light_ids_in_play, 'on', True)
    elif args.excludednames is not None: # Exclude bulbs using names
        # Filter lights in use so that only specified bulbs are used.
        # Turn specified bulbs on.
        regex = re.compile('|'.join(args.excludednames), re.IGNORECASE) # names joined with OR '|' connector
        # Usage note: '.*' is equivalent to DOS '*', '.' is equivalent to DOS '?'
        lights_in_play = [a for a in lights_in_play if not re.search(regex, a)]
        light_ids_in_play = []
        for name in lights_in_play:
            light_ids_in_play.append(int(b.get_light_id_by_name(name)))
        b.set_light(light_ids_in_play, 'on', True)
    else:
        pass # All lights will be adjusted as specified, but will not be switched on

    # randomly assign colors to lights and issue the commands via the hub
    try:
        if args.monochrome:
            # Set all bulbs to the same color; cycle through colors
            light_ids_on = []
            huenum = -1
            brinum = -1
            satnum = -1
            start = time()
            while True:
                loopstart = time()
                if args.duration is not None:
                    if args.duration < (time() - start) / 60:
                            break
                if args.ordered:
                    # This results in each bulb moving through the parameter list in order.
                    huenum = (huenum + 1) % len(args.hues)
                    brinum = (brinum + 1) % len(args.brightness)
                    satnum = (satnum + 1) % len(args.saturation)
                    hue = args.hues[huenum]
                    bri = args.brightness[brinum]
                    sat = args.saturation[satnum]
                else:
                    hue = random.choice(args.hues)
                    bri = random.choice(args.brightness)
                    sat = random.choice(args.saturation)
    
                hue_verbose = hue # used only for verbose printing
                if hue == -1: # flag for white
                    sat = 0 # 0 to 254
                    hue = random.choice([i for i in args.hues if i >= 0]) # choose from non-white values
    
                if hue == -2: # flag for black (off)
                    # get light 'on' status and build a list of lights that are on; build fresh every time
                    for id_ in light_ids_in_play:
                        if b.get_light(id_, 'on'):
                            light_ids_on.append(id_)
                    command =  {'transitiontime' : transitiontime, 'on' : False}
                    result = b.set_light(light_ids_in_play, command)
                else:
                    # Set bulbs
                    if len(light_ids_on) > 0:
                        # If any bulbs are in the list, turn them on
                        command =  {'on' : True, 'transitiontime' : transitiontime, 'hue' : hue, 'sat' : sat, 'bri' : bri}
                        result = b.set_light(light_ids_on, command)
                    else: # empty list
                        command =  {'transitiontime' : transitiontime, 'hue' : hue, 'sat' : sat, 'bri' : bri}
                        result = b.set_light(light_ids_in_play, command)
    
                if args.verbose:
                    if len(light_ids_in_play) > 0:
    #                    print('Hue Bulb(s) ' + str(light_ids_in_play) + ' set to hue = ' + str(hue) + ', sat = ' + str(sat) + ', bri = ' + str(bri))
                        print('Bulb(s) {light_id} set to hue = {hue:>5}, sat = {sat:>3}, bri = {bri:>3}'.format(light_id=light_ids_in_play, hue=hue_verbose, sat=sat, bri=bri))
                    print('-- pass complete, waiting ' + str(transitiontime / 10 + waittime) + ' seconds --')
                    if args.duration is not None:
                        elapsed = time() - start
                        print('-- ' + str(int(args.duration - elapsed/60)) + ' minutes ' + str(round(max((args.duration*60 - elapsed), 0) % 60, 1)) + ' seconds remaining --')
                if transitiontime + waittime == 0.0:
                    if args.verbose:
                        print('-- lights set, bpm = 0.0, exiting program --')
                    break # end program
                else:
                    loopelapsed = time() - loopstart
                    sleep(max(transitiontime / 10 + waittime - loopelapsed, 0))
    
                if len(args.hues) == 1 and len(args.brightness) == 1 and len(args.saturation) == 1:
                    if args.verbose:
                        print('-- only one color to cycle, exiting program --')
                    # only one color, no reason to keep changing it
                    break
        else:
            # Set bulbs to random colors; wait; repeat
            light_ids_on = []
            huenum = -1
            brinum = -1
            satnum = -1
            start = time()
            while True:
                loopstart = time()
                if args.duration is not None:
                    if args.duration < (time() - start) / 60:
                            break
    #            sat = args.saturation # 0 to 254
                if args.ordered:
                    huenum = (huenum + 1) % len(args.hues)
                    brinum = (brinum + 1) % len(args.brightness)
                    satnum = (satnum + 1) % len(args.saturation)
                else:
                    random.shuffle(light_ids_in_play)
                for light_index, light_id in enumerate(light_ids_in_play):
                    if args.ordered:
                        # Each bulb is assigned hues in the user-specified order.
                        # The intial hue is set by cycling through the color list in order.
                        # Visual note: the apparent "chase" direction of colors is the reverse 
                        # of the order of lights. 
                        hue = args.hues[(light_index + huenum) % len(args.hues)]
                        bri = args.brightness[(light_index + brinum) % len(args.brightness)]
                        sat = args.saturation[(light_index + satnum) % len(args.saturation)]
                    else:
                        hue = random.choice(args.hues)
                        bri = random.choice(args.brightness)
                        sat = random.choice(args.saturation)
                    hue_verbose = hue # used only for verbose printing
                    if hue == -1: # flag for white
                        sat = 0 # 0 to 254
                        if len([i for i in args.hues if i >= 0]) > 0:
                            hue = random.choice([i for i in args.hues if i >= 0]) # choose from non-white/black values
                        else:
                            hue = 0 # no colors available to choose, assume red
                    elif hue == -2: # flag for black
                        light_ids_on.append(light_id)
                        hue = random.choice([i for i in args.hues if i >= 0]) # choose from non-white/black values
                        command =  {'on' : False, 'transitiontime' : transitiontime}
    
                    if hue_verbose != -2: # if not black
                        # Set bulbs
                        if light_id in light_ids_on:
                            command =  {'on' : True, 'transitiontime' : transitiontime, 'hue' : hue, 'sat' : sat, 'bri' : bri}
                            light_ids_on.remove(light_id)
                        else:
                            command =  {'transitiontime' : transitiontime, 'hue' : hue, 'sat' : sat, 'bri' : bri}
                    result = b.set_light(light_id, command)
    
                    if args.verbose:
                        if light_id in light_ids_in_play:
                            print('Bulb {light_id:>2} set to hue = {hue:>5}, sat = {sat:>3}, bri = {bri:>3}'.format(light_id=light_id, hue=hue_verbose, sat=sat, bri=bri))
    
                    sat = args.saturation # 0 to 254
    
                if args.verbose:
                    print('-- pass complete, waiting ' + str(transitiontime / 10 + waittime) + ' seconds --')
                    if args.duration is not None:
                        elapsed = time() - start
                        # the following command could use some analysis for the max portion.
                        # the following command, with max removed, will result in an incorrect "59.9 seconds remaining" message at the end
                        # c:\python32\python ColorCycle.py -v -t 3.0 -b 1 -c 0 500 1000 1500 2000 63000 63500 64000 64500 65000 65535 -i10 12 15 19 -d 0.2 -s 254 250 245 240 -x
    #                    print('-- ' + str(int(args.duration - elapsed/60)) + ' minutes ' + str(round(max((args.duration*60 - elapsed), 0) % 60, 1)) + ' seconds remaining --')
                if transitiontime + waittime == 0.0:
                    if args.verbose:
                        print('-- lights set, bpm = 0.0, exiting program --')
                    break # end program
                else:
                    loopelapsed = time() - loopstart
                    len_text = 0
                    while (transitiontime / 10 + waittime - loopelapsed) > 0:
                        loopelapsed = time() - loopstart
                        elapsed = time() - start
                        len_text = underwrite('-- ' + str(int(args.duration - elapsed/60)) + ' minutes ' + str(round(max((args.duration*60 - elapsed), 0) % 60, 1)) + ' seconds remaining --', len_text)
                        sleep(min(1, transitiontime / 10 + waittime - loopelapsed))
            if args.exit:
                command =  {'transitiontime' : transitiontime, 'on' : False}
                result = b.set_light(light_ids_in_play, command)
                print('-- lights off, exiting program --')
    except KeyboardInterrupt:
        # Quit if we get a CTRL-C from the user
        if args.verbose:
            print('-- CTRL-C received, exiting program --')
        sys.exit()

    # debug
#    import pdb
#    pdb.set_trace()
    # debug


def underwrite(text, width):
    """Writes text and then backspaces over it. Returns the length of text written."""
    import sys
    len_text = sys.stdout.write(text.ljust(width))
    sys.stdout.flush()
    len_text = sys.stdout.write('\b' * len(text))
    sys.stdout.flush()
    return len_text


if __name__ == '__main__':
    main()
