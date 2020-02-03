import sys
import os
import configparser
import logging

from .error import *

_MAX_CYCLE_SPEED = 3600
_MIN_CYCLE_SPEED = 5
class Config(object):
    """
    Configuration object for wall paper.
    """
    def __init__(self):
        self._filename = "./wallpaper.conf"
        self._config = configparser.ConfigParser()
        self.reset_config()

    def reset_config(self):
        """Reset config back to default value.
        """
        self._config['DEFAULT'] = {
            'cycle-speed': '5',
            'gallery-directory': os.path.expanduser(r"~\pictures"),
            'log-directory': os.path.expanduser(r"~\wallpaper.log"),
            'randomise': 'False',
            'online-mode': 'False',
            'query': 'Halo',
            'download-cap': 10
        }

    @property
    def filename(self):
        """Return the filename of the config file.
        This getter checks that the filename exists as well.
        """
        return self._filename

    @filename.setter
    def filename(self, val):
        """Setter for the filename of the config file.

        It will check if the directory is valid.
        """
        _FILENAME_DIR = os.path.dirname(val)
        if os.path.isdir(_FILENAME_DIR):
            self._filename = val
        else:
            raise EnvironmentError("Unable to find the directory '{}'".format(_FILENAME_DIR))


    @property
    def cycle_speed(self):
        """Get cycle_speed property.
        """
        val = -1
        try:
            val = int(self._config['DEFAULT']['cycle-speed'])
        except KeyError:
            logging.error("Unable to find the cycle speed parameter.")
        except ValueError:
            logging.error("Config cycle-speed is not an integer.")

        return val

    @cycle_speed.setter
    def cycle_speed(self, val):
        """Get cycle speed

        Raises
        ========
            `ValueError` if set value is outside of range.
            `TypeError` if set value is not a valid int.
        """
        # Check if val is valid integer.
        if type(val) is int:
            if (val >= 0) and (val <= _MAX_CYCLE_SPEED):
                self._config['DEFAULT']['cycle-speed'] = str(val)
            else:
                raise ValueError("'cycle-speed' must be between 5 and {}".format(_MAX_CYCLE_SPEED))
        else:
            raise ValueError("'cycle-speed' must be of type '{}' not '{}'".format(str(int), type(val)))

    @property
    def gallery_directory(self):
        """Return the gallery directory.
        """
        return self._config['DEFAULT']['gallery-directory']

    @gallery_directory.setter
    def gallery_directory(self, val):
        """Set the gallery directory.

        Raises
        ========
            `EnvironmentError` if the gallery directory could not be found.
        """
        if os.path.exists(str(val)) and os.path.isdir(str(val)):
            self._config['DEFAULT']['gallery-directory'] = val
        else:
            raise EnvironmentError("'{}' is not a valid directory.".format(str(val)))

    @property
    def log_directory(self):
        """Get the log directory.
        This is the directory where the log is stored.
        """
        return self._config['DEFAULT']['log-directory']

    @log_directory.setter
    def log_directory(self, val):
        """Set the log directory.
        This is the directory the log is stored. Log will always be
        wallpaper.log.

        Raises
        ========
            `EnvironmentError` if log directory does not exist.
        """
        if os.path.isdir(val):
            self._config['DEFAULT']['log-directory'] = val
        else:
            raise EnvironmentError("'{}' is not a valid directory.".format(str(val)))

    @property
    def randomise(self):
        """Get the randomise option.

        Raises
        ========
            `ConfigureFileOptionError` if unable to read a valid boolean from randomise option.
        """
        return tobool(self._config['DEFAULT']['randomise'])

    @randomise.setter
    def randomise(self, val):
        """Set the randomise option.
        """
        if type(val) is bool:
            self._config['DEFAULT']['randomise'] = str(val)

    @property
    def online_mode(self):
        """Return whether online mode is enabled.

        Raises
        ========
            `ConfigureFileOptionError` if unable to read a valid boolean from randomise option.
        """
        return tobool(self._config['DEFAULT']['online-mode'])

    @online_mode.setter
    def online_mode(self, val):
        if type(val) is bool:
            self._config['DEFAULT']['online-mode'] = str(val)

    @property
    def query(self):
        return str(self._config['DEFAULT']['query'])

    @query.setter
    def query(self, val):
        self._config['DEFAULT']['query'] = str(val)

    @property
    def download_cap(self):
        """Getter for the maximum number of images to download. Will not download any more than this amount."""
        return int(self._config['DEFAULT']['download-cap'])

    @download_cap.setter
    def download_cap(self, val):
        if type(val) is not int:
            raise ValueError("'download_cap' must be a of type 'int'")

        self._config['DEFAULT']['download-cap'] = val

    def save_config(self):
        """Save the config to file.
        """
        with open(self._filename, 'w') as configfile:
            self._config.write(configfile)

    def load_config(self):
        """Load the config from a file.

        Raises
        ========
            `EnvironmentError` if unable to find the configuration file.
        """
        if os.path.exists(self.filename):
            self._config.read(self.filename)
        else:
            raise EnvironmentError("Unable to find configuration file '{}'".format(self.filename))


def tobool(val):
    if (val == "False") or (val == "false"):
        val = False
    elif (val == "True") or (val == "true"):
        val = True
    else:
        # This shouldn't happen. Maybe raise a configuration
        # error.
        raise ConfigurationFileOptionError("Unable to read {} from option randomise.".format(val))

    return val


