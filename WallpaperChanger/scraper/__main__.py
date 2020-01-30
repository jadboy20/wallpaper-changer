import sys
import os
import requests
from lxml import html


OUTPUT_FILE = "../output/test.html"
ROOT_WEBSITE = "https://hipwallpaper.com"




def main():
    req = requests.get("https://hipwallpaper.com/search?q=fallout")
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
    links = tree.xpath('//div[@class="row"]/a/@href')
    return links


def get_pictures_from_links(links):
    pass


def get_pictures_from_link(link):
    req = requests.get(link)
    tree = html.fromstring(req.content)
    links = tree.xpath('//a[@class="btn btn-primary"]/@href')
    return links

def download_link(link):
    print("Downloading: {}".format(link))
    req = requests.get(link)
    with open("../output/{}".format(os.path.basename(link)), "wb") as f:
        f.write(req.content)


if __name__ == "__main__":
    main()
    sys.exit(0)