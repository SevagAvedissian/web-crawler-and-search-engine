import os
import shelve
from threading import Lock
from urllib.parse import urlparse
from utils import get_logger, get_urlhash, normalize
from crawler.scraper import is_valid

class Frontier(object):
    def __init__(self, config):
        self.logger = get_logger("FRONTIER")
        self.config = config
        self.to_be_downloaded = list()
        self.blocked_domains = list()
        self.lock = Lock()
        self.save_file = "Data/frontier"

        # Load existing save file, or create one if it does not exist.
        self.save = shelve.open(self.save_file)

        # Set the frontier state with contents of save file.
        self._parse_save_file()
        if not self.save:
            for url in self.config.seed_urls:
                self.add_url(url)

    def _parse_save_file(self):
        total_count = len(self.save)
        tbd_count = 0
        for url, completed in self.save.values():
            if not completed and is_valid(url):
                self.to_be_downloaded.append(url)
                tbd_count += 1
        self.logger.info(
            f"Found {tbd_count} urls to be downloaded from {total_count} "
            f"total urls discovered.")

    def get_tbd_url(self):
        with self.lock:
            for url in self.to_be_downloaded:
                domain = urlparse(url).netloc
                if domain not in self.blocked_domains:
                    self.blocked_domains.append(domain)
                    self.to_be_downloaded.remove(url)
                    return url, domain
            return None, None

    def add_url(self, url):
        url = normalize(url)
        urlhash = get_urlhash(url)
        if urlhash not in self.save:
            with self.lock:
                self.save[urlhash] = (url, False)
                self.save.sync()
                self.to_be_downloaded.append(url)
    
    def mark_url_complete(self, url):
        urlhash = get_urlhash(url)
        if urlhash not in self.save:
            self.logger.error(
                f"Completed url {url}, but have not seen it before.")

        with self.lock:
            self.save[urlhash] = (url, True)
            self.save.sync()

    def unblock_domain(self, domain):
        with self.lock:
            self.blocked_domains.remove(domain)
    
    def is_empty(self):
        with self.lock:
            return len(self.to_be_downloaded) == 0 and len(self.blocked_domains) == 0
