import os
import sys
import WallpaperChanger.app as app
import argparse
import logging
import logging.config
from WallpaperChanger import __version__

def main():
    args = parse_arguments()
    initialise_logging(args)
    logging.info("")
    logging.info("App started!")
    app.App(args)


def initialise_logging(args):
    try:
        logging.basicConfig(
            filename=args.log_directory if args.log_directory is not None else './wallpaper.log',
            level=logging.DEBUG,
            format="[%(asctime)s]<%(levelname)s>: %(message)s",
            datefmt="%Y-%d-%m %I:%M:%S %p"
        )
    except PermissionError as e:
        print("Do not have permission to create {}!".format(e.filename))
        print("Exiting program!")
        sys.exit(1)


def parse_arguments():
    # Initialise the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cycle-speed", help="Set the rate at which wallpapers change.")
    parser.add_argument("-d", "--gallery-directory", help="Set the directory where the wallpapers reside.")
    parser.add_argument("-r", "--randomise", action="store_true", help="Displays the wallpapers in a random order.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--log-directory", help="Absolute file name of the log.")
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
