import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Control Philips Hue lights from the CLI.')
    
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
    
    parser.add_argument('-d', '--duration', help='Duration for which the pattern should repeat (minutes)', type=float, default=0.0)
    parser.add_argument('-p', '--ip', help='Specify bridge IP', type=str)
    parser.add_argument('-cn', '--colornames', help='Use color names instead of hue values', action='store_true', default=False)
    parser.add_argument('--colorname-list', help='List available color names', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action="store_true")
    parser.add_argument('-x', '--exit', help='Exit by turning bulbs off', action="store_true")

    return parser.parse_args()
