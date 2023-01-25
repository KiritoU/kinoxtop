import json
import logging
from time import sleep

from bs4 import BeautifulSoup

from _db import database
from helper import helper
from settings import CONFIG

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


class Crawler:
    def crawl_soup(self, url):
        logging.info(f"Crawling {url}")
        html = helper.download_url(url)
        if html.status_code == 404:
            return 404

        soup = BeautifulSoup(html.content, "html.parser")

        return soup
