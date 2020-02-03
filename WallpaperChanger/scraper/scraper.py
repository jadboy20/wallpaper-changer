import os
import sys
import requests
from urllib import parse
import logging
from lxml import html


# There should be an option to cache the image links of download them. That way they
# don't take up too much space. However, it will increase the amount of data usage.

class Scraper(object):
    def __init__(self, hostname):
        self.hostname = hostname
        self.results = []
    def search(self, query, num_results=10):
        """Use this funtion to return a list of links to images.

        query:
            The search parameter. This could be the theme that is being searched such as 'cute cats' etc...

        num_results:
            The maximum number of images to return. It is possible that there are a plethora of
            images returned. This can increase the time it takes to get results so we will only get a portion.

        returns:
            A list containing a list of url's pointing to the pictures to download.
            An empty list will be returned if unsuccessful.
        """
        pass

    def get_search_url(self, query):
        """Use this function to return the url with search parameter
        Example 'www.hostname.com?query=query'
        """
        pass


class HipWallpaperScraper(Scraper):
    """
    A web scraper for the web site "https://hipwallpaper.com"
    """
    def __init__(self):
        super().__init__("https://hipwallpaper.com")

    def search(self, query, num_results=10):
        sanitised_query = parse.quote(query)
        logging.info("Looking for images relating to: {}".format(query))
        logging.info("Send get request: {}".format(self.get_search_url(sanitised_query)))

        try:
            req = requests.get(self.get_search_url(sanitised_query))
            if req.status_code != 200:
                logging.warn("{} - {}".format(self.get_search_url(sanitised_query), req.status_code))
                return []
        except requests.exceptions.ConnectionError as e:
            # TODO: Fix this up and use a proper exception relating to the request module.
            logging.error("{}".format(str(e)))
        else:
            # First we need to get the categories since this website returns categories first.
            tree = html.fromstring(req.content)
            # Lets strip out all the categories.
            links = tree.xpath('//div[@class="row"]/a/@href')           # These are the path to the next page. These need to be appended to the hostname
            titles = tree.xpath('//span[@class="card-title"]/text()')   # These are the titles of each page. This can be considered the categories.

            num_pictures = 0
            images_to_return = []
            for link in links:
                url = self.hostname + link
                req = requests.get(url)
                tree = html.fromstring(req.content)
                images = tree.xpath('//a[@class="btn btn-primary"]/@href')

                images_to_return += images
                if len(images_to_return) > num_results:
                    images_to_return = images_to_return[:(num_results)]
                    break

            logging.info("Successfully got {} images!".format(len(images_to_return)))

            return images_to_return

    def write_images_to_file(self, results, path):

        if os.path.isdir(os.path.dirname(path)) is False:
            logging.info("Making directory {}".format(os.path.dirname(path)))
            os.mkdir(os.path.dirname(path))

        with open(path, 'w') as f:
            for url in results:
                f.write(url + "\n")

    def get_search_url(self, query):
        return self.hostname + "/search?q=" + query

    def download_images(self, cache_path, directory):
        # Start by reading the cache and pulling the images from there.
        with open(cache_path, 'r') as f:
            cache = f.readlines()

        for link in cache:
            w = WallpaperLink(link, directory)
            w.download()


class WallpaperLink(object):

    def __init__(self, link=None, save_to=None):
        self.link = link
        self.save_to = save_to

    def __str__(self):
        return str(self._link)

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, val):
        self._link = str(val).replace("\n", "")

    def get_basename(self):
        return os.path.basename(self._link)

    @property
    def save_to(self):
        return self._save_to

    @save_to.setter
    def save_to(self, val):
        if os.path.isdir(val):
            self._save_to = val
        else:
            raise EnvironmentError("{} is not a directory".format(val))

    @property
    def save_path(self):
        return os.path.join(self.save_to, self.get_basename())

    def save_path_exists(self):
        """Return true if the save path already exists. False otherwise"""
        return os.path.exists(self.save_path)

    def download(self):
        if self.save_path_exists() is False:
            req = requests.get(self.link)
            if req.status_code == 200:
                print("Saving to {}".format(self.save_path))
                with open(self.save_path, 'wb') as f:
                    f.write(req.content)
            else:
                logging.error("Unable to download {}. Got status code: {}".format(self.link, req.status_code))
        else:
                logging.info("{} already exists. Not downloading.".format(self.save_path))

