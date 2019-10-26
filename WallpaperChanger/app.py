import os
import sys
import WallpaperChanger.wallpaper as wallpaper
import argparse


class App(object):

    def __init__(self, args):
        # Print received arguments.
        print("Received arguments: ")
        self.params = args

        self.run()

    def run(self):
        wp = wallpaper.Wallpaper(self.params)


