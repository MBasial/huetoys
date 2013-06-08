def main():
    from phue import Bridge
    import argparse

    # user-specific settings
    lights_in_play = [
                      'Office Lamp 1A'
#                      'Front Porch', 
#                      'Entryway', 'Foyer',
#                      'TV', 'Ledge 1', 'Ledge 2', 'Ledge 3', 'Ledge 4', 
#                      'Office', 'Office Lamp 1A', 'Office Lamp 1B', 'Office Lamp 2A', 'Office Lamp 2B', 
#                      'Bedroom 1', 'Bedroom 2'
                      ]

    print('SetBulb')
    # command-line argument parser
    parser = argparse.ArgumentParser(
            prog = 'SetBulb',
            prefix_chars = '-/',
            description = """This program assigns settings to a list of bulbs (list is currently coded into the .py file).""")
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action="store_true")
    parser.add_argument('-xy', help='An XY pair to define the bulb color (0.0-1.0, 0.0-1.0)', type=float, nargs=2, default=[0.5, 0.5])
    parser.add_argument('-t', '--timing', help='Set bulb transition time (seconds)', type=float, default=0)
    parser.add_argument('-b', '--brightness', help='Set bulb brightness (0 - 254)', type=float, default=254.0)
    # TODO: add option to specify bulb names
    # TODO: add option to specify light IDs
    # TODO: add option to print list of bulb name/ID combos
    # TODO: add option to print list of 'legal' named colors (green, red, energize)
    # TODO: add option to specify colors as names
    # TODO: add option to specify bridge IP
    args = parser.parse_args()

    x, y = args.xy[0], args.xy[1]
    transitiontime = int(args.timing * 10) # API uses 10ths of seconds
    bri = int(args.brightness)

    b = Bridge()
    lights = b.get_light_objects('name')
    light_ids_in_play = []
    for name in lights_in_play:
        light_ids_in_play.append(int(b.get_light_id_by_name(name)))

    if args.verbose:
        print('Verbosity set to ON')
        print('Bulbs to be set: ' + str(light_ids_in_play))
        print('XY color set to X = {0}, Y = {0}'.format(x, y))
        print('Transition speed set to ' + str(abs(args.timing)) + ' seconds.')
        print('Brightness set to ' + str(args.brightness))

    # issue commands via the hub
    command =  {'on' : True, 'transitiontime' : transitiontime, 'xy' : [x, y], 'bri' : bri}
    result = b.set_light(light_ids_in_play, command)
    print('-- lights set, exiting program --')

    # debug
#    import pdb
#    pdb.set_trace()
    # debug

if __name__ == '__main__':
    main()
