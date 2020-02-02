import os
import sys
from . import wallpaper
from . import WALLPAPER_DEFAULT_DIR, WALLPAPER_DEFAULT_CACHE
from . import scraper
import argparse


class App(object):

    def __init__(self, args):
        # Print received arguments.
        self.params = args
        self.create_default_directories()
        self.run()

    def create_default_directories(self):
        self.create_directory(WALLPAPER_DEFAULT_DIR)

    def create_directory(self, directory):
        if os.path.isdir(directory) is False:
            os.mkdir(directory)

    def run(self):
        wp = wallpaper.Wallpaper(self.params)
        wp.run()


