def main():
    import sys
    import random as random
    random.seed()
    from time import sleep
    from phue import Bridge

    # user-specific settings
    lights_in_play = [
#                      'Front Porch', 
                      'Entryway', 'Foyer',
                      'TV', 'Ledge 1', 'Ledge 2', 'Ledge 3', 'Ledge 4', 
                      'Office', 'Office Lamp 1A', 'Office Lamp 1B', 'Office Lamp 2A', 'Office Lamp 2B', 
                      'Bedroom 1', 'Bedroom 2'
                      ]

    # command-line argument parser
    import argparse
    parser = argparse.ArgumentParser(
            prog = 'ColorCycle',
            prefix_chars = '-/',
            description = """This program takes a series of color and brightness inputs and changes bulb charateristics accordingly.
                             It assumes that lights that are on will be used. Lights are tested for 'on' status every transition.""")
    parser.add_argument('bpm', help='Set tempo as beats per minute, decimal values allowed; positive values produce gradual changes, ' + 
                                    'negative values produce flash transitions; can be modified by -t', type=float)
    parser.add_argument('hues', help='A list of color values the lights will cycle through (0 - 65535)', type=int, nargs='+')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action="store_true")
    parser.add_argument('-b', '--brightness', help='Set bulb brightness (0 - 254)', type=int, default=254)
    parser.add_argument('-bLC', '--brightnessLivingColors', help='Set LivingColors bulb brightness (0 - 254)', type=int, metavar='briLC')
    parser.add_argument('-bH', '--brightnessHue', help='Set Hue bulb brightness (0 - 254)', type=int, metavar='briHue')
    parser.add_argument('-s', '--saturation', help='Set bulb color saturation (0 - 254)', type=int, default=254)
    parser.add_argument('-t', '--timing', help='Use seconds instead of bpm for transition timing', action="store_true", default=False)
    parser.add_argument('-m', '--monochrome', help='Cycle through color list with all lights the same color', action="store_true", default=False)
    # TODO: add option to specify bulb names
    # TODO: add option to specify light IDs
    # TODO: add option to print list of bulb name/ID combos
    # TODO: add option to print list of 'legal' named colors (green, red, energize)
    # TODO: add option to specify colors as names
    # TODO: add option to turn bulbs on at beginning of cycle
    # TODO: add option to specify bridge IP
    # TODO: add option to cycle non-randomly through the list; should be compatible wth -m
    # TODO: add black (off, flag as hue = -2) as a color; will have to store a list of live bulbs so that lights can turn back on
    args = parser.parse_args()
    if args.verbose:
        print('Verbosity set to ON')
        if args.timing:
            print('Timing is set to ' + str(abs(args.bpm)) + ' seconds.')
        else:
            print('Timing is set to ' + str(abs(args.bpm)) + ' bpm.')
        if args.bpm == 0:
            print('Lights will be set once and program will exit')
        elif args.bpm >= 0:
            print('Transitions will be gradual')
        elif args.bpm <= 0:
            print('Transitions will be instant')
        print('Hues that will be cycled through: ' + str(args.hues))
        print('Color saturation set to ' + str(args.saturation))
        print('Brightness set to ' + str(args.brightness))
        if args.brightnessLivingColors is not None:
            print('Brightness for LivingColors lamps set to ' + str(args.brightnessLivingColors))
        if args.brightnessHue is not None:
            print('Brightness for Hue bulbs set to ' + str(args.brightnessHue))

# Old manual command-line argument parsing; retained for reference
#    # Get cycling parameters.
#    if len(sys.argv) >= 3: # The name of the python script is always the first argument, so that plus 2 parameters = 3.
#        bpm = float(sys.argv[1])
#        hues = [int(h) for h in sys.argv[2:]]
#    elif len(sys.argv) == 1: # Use interactive input.
##        lights = b.get_light_objects('name')
#        bpm = float(input("BPM (can be decimal; negative for snap transitions): "))
#        hues = input("List of hue values (0 - 65535): ")
#        hues = [int(h) for h in hues.split()]
#    else:
#        print("Incorrect number of input arguments, 2 parameters must be provided.")
#        quit()
#    print('Color Cycler')
#    print('Usage: ColorCycle.py <BPM> <hue1 [hue2 ...]>')
    
    # assign brightness levels
    if args.brightnessLivingColors is not None:
        bri_lc = args.brightnessLivingColors # 0 to 254
    else:
        bri_lc = args.brightness
    if args.brightnessHue is not None:
        bri_hue = args.brightnessHue # 0 to 254
    else:
        bri_hue = args.brightness

    # Convert beats per minute (BPM) to tenths of seconds
    if args.timing == 0.0:
        transitiontime = 0
        waittime = 0.0
    else:
        if args.timing:
            # Use bpm argument as seconds, NOT as bpm
            if args.bpm >= 0: 
                transitiontime = int(args.bpm * 10)
                waittime = transitiontime / 10
            else: # use negative bpm to specify flash transitions
                transitiontime = 0
                waittime = -args.bpm
        else:
            # Use bpm as bpm
            if args.bpm >= 0: 
                transitiontime = int(round(60 / args.bpm * 10, 0))
                waittime = transitiontime / 10
            else: # use negative bpm to specify flash transitions
                transitiontime = 0
                waittime = round(60 / -args.bpm * 10, 0) / 10

    # assign light ID numbers to Hue and LivingColors lists (mainly due to brightness differences)
    b = Bridge()
#    b = Bridge('192.168.1.110') # update to phue allows Bridge() call without IP address after initial setup
    lights = b.get_light_objects('name')
    light_ids_hue = []
    light_ids_lc = []
    light_ids_in_play = []
    for name in lights_in_play:
        light_ids_in_play.append(int(b.get_light_id_by_name(name)))
        if b.get_light(int(b.get_light_id_by_name(name)))['modelid'] == 'LLC001': # LivingColors
             light_ids_lc.append(int(b.get_light_id_by_name(name)))
        elif b.get_light(int(b.get_light_id_by_name(name)))['modelid'] == 'LCT001': # Hue
             light_ids_hue.append(int(b.get_light_id_by_name(name)))
        else:
            print('else error')

    # randomly assign colors to lights and issue the commands via the hub
    if args.monochrome:
        # Set all bulbs to the same color; cycle through colors
        light_ids_on = []
        while True:
            hue = random.choice(args.hues)
            if hue == -1: # flag for white
                saturation = 0 # 0 to 254
                hue = random.choice([i for i in args.hues if i >= 0]) # choose from non-white values
            else:
                saturation = args.saturation # 0 to 254

            if hue == -2: # flag for black (off)
                # get light 'on' status and build a list of lights that are on; build fresh every time
                for id in light_ids_in_play:
                    if b.get_light(id, 'on'):
                        light_ids_on.append(id)
                command =  {'transitiontime' : transitiontime, 'on' : False}
                result = b.set_light(light_ids_in_play, command)
            else:
                # Set LivingColors lamps
                light_ids_on_lc = [id for id in light_ids_lc if id in light_ids_on]
                if len(light_ids_on_lc) > 0:
                    # If any bulbs are in the list, turn them on
                    command_lc =  {'on' : True, 'transitiontime' : transitiontime, 'hue' : hue, 'sat' : saturation, 'bri' : bri_lc}
                    result = b.set_light(light_ids_on_lc, command_lc)
                else: # empty list
                    command_lc =  {'transitiontime' : transitiontime, 'hue' : hue, 'sat' : saturation, 'bri' : bri_lc}
                    result = b.set_light(light_ids_lc, command_lc)
                # Set Hue bulbs
                light_ids_on_hue = [id for id in light_ids_hue if id in light_ids_on]
                if len(light_ids_on_hue) > 0:
                    # If any bulbs are in the list, turn them on
                    command_hue =  {'on' : True, 'transitiontime' : transitiontime, 'hue' : hue, 'sat' : saturation, 'bri' : bri_hue}
                    result = b.set_light(light_ids_on_hue, command_hue)
                else: # empty list
                    command_hue =  {'transitiontime' : transitiontime, 'hue' : hue, 'sat' : saturation, 'bri' : bri_hue}
                    result = b.set_light(light_ids_hue, command_hue)

            if args.verbose:
                if len(light_ids_lc) > 0:
                    print('LC  Bulb(s) ' + str(light_ids_lc) + ' set to hue = ' + str(hue) + ', sat = ' + str(saturation) + ', bri = ' + str(bri_lc))
                if len(light_ids_hue) > 0:
                    print('Hue Bulb(s) ' + str(light_ids_hue) + ' set to hue = ' + str(hue) + ', sat = ' + str(saturation) + ', bri = ' + str(bri_hue))
                print('-- pass complete, waiting ' + str(waittime) + ' seconds --')
            if waittime == 0.0:
                if args.verbose:
                    print('-- lights set, bpm = 0.0, exiting program --')
                break # end program
            else:
                sleep(waittime)
    else:
        # Set bulbs to random colors; wait; repeat
        while True:
            random.shuffle(light_ids_in_play)
            for light_id in light_ids_in_play:
                hue = random.choice(args.hues)
                if hue == -1: # flag for white
                    saturation = 0 # 0 to 254
                    hue = random.choice([i for i in args.hues if i >= 0]) # choose from non-white values
                else:
                    saturation = args.saturation # 0 to 254
                if light_id in light_ids_lc:
                    # Set LivingColors lamps
                    command =  {'transitiontime' : transitiontime, 'hue' : hue, 'sat' : saturation, 'bri' : bri_lc}
                elif light_id in light_ids_hue:
                    # Set Hue bulbs
                    command =  {'transitiontime' : transitiontime, 'hue' : hue, 'sat' : saturation, 'bri' : bri_hue}
                else:
                    print('else error')
                result = b.set_light(light_id, command)
                if args.verbose:
                    if light_id in light_ids_lc:
                        print('Bulb ' + str(light_id) + ' set to hue = ' + str(hue) + ', sat = ' + str(saturation) + ', bri = ' + str(bri_lc))
                    elif light_id in light_ids_hue:
                        print('Bulb ' + str(light_id) + ' set to hue = ' + str(hue) + ', sat = ' + str(saturation) + ', bri = ' + str(bri_hue))
            if args.verbose:
                print('-- pass complete, waiting ' + str(waittime) + ' seconds --')
            if waittime == 0.0:
                if args.verbose:
                    print('-- lights set, bpm = 0.0, exiting program --')
                break # end program
            else:
                sleep(waittime)

    # debug
#    import pdb
#    pdb.set_trace()
    # debug


if __name__ == '__main__':
    main()
