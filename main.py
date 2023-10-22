from arg_parser import get_args
from hue_controller import HueController

def main():
    args = get_args()
    controller = HueController(args)
    controller.run()

if __name__ == "__main__":
    main()
