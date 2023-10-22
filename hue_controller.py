import time
import random
import colorsys
import re
from datetime import datetime, timedelta
from phue import Bridge

COLOR_NAME_TO_RGB = {
    'red': (1.0, 0.0, 0.0),
    'green': (0.0, 1.0, 0.0),
    'blue': (0.0, 0.0, 1.0),
    # ... add more colors as needed
}

class HueController:
    def __init__(self, args, bridge_ip=None):
        self.args = args
        self.bridge = Bridge(bridge_ip or self.args.ip)
        self.bridge.connect()
        self.lights = self.bridge.lights

    def run(self):
        if self.args.colorname_list:
            self.list_color_names()
        elif self.args.exit:
            self.turn_off_lights()
        else:
            self.execute_pattern()

    def list_color_names(self):
        print('Available color names:')
        for color_name in COLOR_NAME_TO_RGB.keys():
            print(color_name)

    def turn_off_lights(self):
        for light in self.lights:
            self.bridge.set_light(light.light_id, 'on', False)

    def execute_pattern(self):
        if self.args.timing:
            transition_time = int(self.args.timing * 10)
        elif self.args.bpm:
            transition_time = int((60.0 / self.args.bpm) * 10)
        else:
            transition_time = 0
        
        color_list = self.args.hues if self.args.hues[0] != -1 else [random.randint(0, 65535) for _ in range(3)]
        brightness_list = self.args.brightness
        saturation_list = self.args.saturation
        
        if self.args.colornames:
            try:
                color_list = [COLOR_NAME_TO_RGB[color_name] for color_name in self.args.hues if color_name in COLOR_NAME_TO_RGB]
            except KeyError as e:
                print(f"Error: Invalid color name {e.args[0]}")
                return

        end_time = datetime.now() + timedelta(minutes=self.args.duration)
        selected_lights = self.get_selected_lights()

        while True:
            if self.args.duration > 0 and datetime.now() >= end_time:
                break
            
            if self.args.monochrome:
                for color, brightness, saturation in zip(color_list, brightness_list, saturation_list):
                    self.set_selected_lights(selected_lights, color, brightness, saturation, transition_time)
                    time.sleep(self.args.wait)
            elif self.args.ordered:
                for i, (color, brightness, saturation) in enumerate(zip(color_list, brightness_list, saturation_list)):
                    self.set_selected_lights(selected_lights[i % len(selected_lights)], color, brightness, saturation, transition_time)
                    time.sleep(self.args.wait)
            else:
                for color, brightness, saturation in zip(color_list, brightness_list, saturation_list):
                    self.set_selected_lights(selected_lights, color, brightness, saturation, transition_time)
                    time.sleep(self.args.wait)

    def get_selected_lights(self):
        selected_lights = []
        if self.args.names:
            for name_pattern in self.args.names:
                regex = re.compile(name_pattern)
                selected_lights.extend([light for light in self.lights if regex.match(light.name)])
        elif self.args.ids:
            selected_lights = [light for light in self.lights if light.light_id in self.args.ids]
        elif self.args.excludednames:
            for name_pattern in self.args.excludednames:
                regex = re.compile(name_pattern)
                selected_lights.extend([light for light in self.lights if not regex.match(light.name)])
        elif self.args.excludedids:
            selected_lights = [light for light in self.lights if light.light_id not in self.args.excludedids]
        else:
            selected_lights = self.lights  # Default to all lights

        return selected_lights

    def set_selected_lights(self, lights, rgb, brightness, transition_time):
        hue, saturation, _ = colorsys.rgb_to_hsv(*rgb)
        hue = int(hue * 65535)
        saturation = int(saturation * 254)
        command = {
            'transitiontime': transition_time,
            'on': True,
            'hue': hue,
            'bri': brightness,
            'sat': saturation
        }
        for light in lights:
            self.bridge.set_light(light.light_id, command)
