import os
import sys
import WallpaperChanger.app as app


def main(args):
    app.App(args)


def initialise_args(self):
    """Create and return an argparse object."""
    args = argparse.ArgumentParser()

    # Add arguments
    args.add_argument("--set-speed", help="Set the rate at which wallpapers cycle.")

    return args

if __name__ == "__main__":
    main(sys.argv)
