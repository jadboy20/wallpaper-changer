import sys
import os
import requests
from urllib import parse
from lxml import html


OUTPUT_FILE = "../output/test.html"
ROOT_WEBSITE = "https://hipwallpaper.com"
OUTPUT_DIR="../output"

def main():
    theme = parse.quote(input("What would you like to search? "))
    url = "https://hipwallpaper.com/search?q={}".format(theme)
    print("Getting url: {}".format(url))

    req = requests.get(url)

    if req.status_code == 200:
        tree = html.fromstring(req.content)
        links = get_links_from_tree(tree)

        pictures = []
        for link in links:
            pictures += get_pictures_from_link(ROOT_WEBSITE + link)

        for picture in pictures:
            download_link(picture)


def write_out_contents(content):
    print("Writing out file to {}".format(OUTPUT_FILE))
    with open(OUTPUT_FILE, "w") as f:
        f.write(str(content))


def get_links_from_tree(tree) -> list:
    print("Getting links to pictures...")
    links = tree.xpath('//div[@class="row"]/a/@href')
    print("Got {} links!".format(len(links)))
    return links


def get_pictures_from_links(links):
    pass


def get_pictures_from_link(link):
    print("Getting links to wallpapers!")
    req = requests.get(link)
    tree = html.fromstring(req.content)
    links = tree.xpath('//a[@class="btn btn-primary"]/@href')
    print("Got {} pictures to download!".format(len(links)))
    return links

def download_link(link):
    print("Downloading: {}".format(link))
    req = requests.get(link)
    if os.path.isdir(OUTPUT_DIR) is False:
        os.mkdir(OUTPUT_DIR)

    with open("../output/{}".format(os.path.basename(link)), "wb") as f:
        f.write(req.content)


if __name__ == "__main__":
    main()
    sys.exit(0)