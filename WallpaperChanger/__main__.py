import os
import sys
import argparse
import logging
import logging.config
import traceback
from . import app
from . import __version__

def main():
    args = parse_arguments()
    initialise_logging(args)
    logging.info("")
    logging.info("App started!")

    try:
        app.App(args)
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt! Exiting app...")
    except Exception:
        # I know this is not the best, but this is to catch any unknown
        # exceptions that I may have not thought of and log them.
        # Should help with debugging the code.
        logging.error("Encountered Error! {}".format(traceback.format_exc()))

    sys.exit(0)


def initialise_logging(args):
    try:
        logging.basicConfig(
            filename=args.log_directory if args.log_directory is not None else './wallpaper.log',
            level=logging.DEBUG,
            format="[%(asctime)s]<%(levelname)s>: %(message)s",
            datefmt="%Y-%d-%m %I:%M:%S %p"
        )
    except PermissionError as e:
        print("Do not have permission to create '{}'!".format(e.filename), file=sys.stderr)
        print("Exiting program!", file=sys.stderr)
        sys.exit(1)


def parse_arguments():
    # Initialise the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cycle-speed", help="Set the rate at which wallpapers change.")
    parser.add_argument("-d", "--gallery-directory", help="Set the directory where the wallpapers reside.")
    parser.add_argument("-r", "--randomise", action="store_true", help="Displays the wallpapers in a random order.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--log-directory", help="Creates and logs to log file provided here. Must contain absolute path.")
    parser.add_argument("--configuration-path", help="This tells the program where to load the config from.")
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
