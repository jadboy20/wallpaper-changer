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

            # TODO: What to do when there are no categories?


    def write_images_to_file(self, results, path):

        if os.path.isdir(os.path.dirname(path)) is False:
            logging.info("Making directory {}".format(os.path.dirname(path)))
            os.mkdir(os.path.dirname(path))

        with open(path, 'w') as f:
            for url in results:
                f.write(url + "\n")


    def get_search_url(self, query):
        return self.hostname + "/search?q=" + query
