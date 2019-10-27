import os
import sys
import WallpaperChanger.app as app
import argparse
from WallpaperChanger import __version__

def main():
    args = parse_arguments()
    app.App(args)

def parse_arguments():
    # Initialise the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cycle-speed", help="Set the rate at which wallpapers change.")
    parser.add_argument("-d", "--gallery-directory", help="Set the directory where the wallpapers reside.")
    parser.add_argument("-r", "--randomise", action="store_true", help="Displays the wallpapers in a random order.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--load-config", help="Load previous configuration ")
    parser.add_argument("--version", action="store_true")
    parser.description = "A program that cycles through wallpapers for your desktop."
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(1)
    elif args is None:
        parser.print_help()
        sys.exit(1)

    return args


if __name__ == "__main__":
    main()
