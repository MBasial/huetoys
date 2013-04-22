def main():

    import sys
    import random as random
    random.seed()
    from time import sleep
    from phue import Bridge

    print('Disco Light Test')
    print('Usage: DiscoLight.py <BPM> <\'Light name\'>')
    
    # Get disco parameters.
    if len(sys.argv) >= 3: # The name of the python script is always the first argument, so that plus 2 parameters = 3.
        bpm = float(sys.argv[1])
        name = str(' '.join(sys.argv[2:])) # TODO: learn how to accept 'text in quotes'.
    elif len(sys.argv) == 1: # Use interactive input.
#        lights = b.get_light_objects('name')
        bpm = float(input("BPM (can be decimal): "))
        name = input("Name of disco light: ")
    else:
        print("Incorrect number of input arguments, 2 parameters must be provided.")
        quit()

    b = Bridge('192.168.1.110')
    light_id = int(b.get_light_id_by_name(name))

    # Convert beats per minute (BPM) to tenths of seconds
    if bpm >= 0: 
        transitiontime = int(round(60 / bpm * 10, 0))
        waittime = transitiontime / 10
    else: # use negative bpm to specify flash transitions
        transitiontime = 0
        waittime = round(60 / -bpm * 10, 0) / 10

    print('\'' + name + '\' at ' + str(abs(bpm)) + ' bpm (' + str(waittime) + ' s)')
    while True:
        hue = random.randint(0, 65535) # 0 to 65535
        brightness = random.randint(0, 254) # 0 to 254
        saturation = random.randint(0, 10) # 0 to 254
        if saturation != 0:
            saturation = random.randint(191, 254) # 0 to 254
#        command =  {'colormode' : 'hs'}
#        result = b.set_light(light_id, command)
#        print(result)
        command =  {'transitiontime' : transitiontime, 'hue' : hue, 'sat' : saturation, 'bri' : brightness}
        result = b.set_light(light_id, command)
        sleep(waittime)

    # debug
#    import pdb
#    pdb.set_trace()
    # debug

if __name__ == '__main__':
    main()

