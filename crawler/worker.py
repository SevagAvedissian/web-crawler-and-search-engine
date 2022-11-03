from threading import Thread
from urllib import robotparser
from urllib.parse import urlparse
from utils import get_logger
import crawler.scraper as scraper
import requests
import asyncio
import json
import os

class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.event_loop = asyncio.new_event_loop()
        super().__init__(daemon=True)
        
    def run(self):
        asyncio.set_event_loop(self.event_loop)
        self.event_loop.create_task(self.work())
        self.event_loop.run_forever()

    async def work(self):
        while True:
            tbd_url, blocked_domain = self.frontier.get_tbd_url()
            if self.frontier.is_empty():
                self.logger.info("Frontier is empty. Stopping Crawler.")
                self.event_loop.stop()        
                return

            if tbd_url:
                robotstxt_url = urlparse(tbd_url)._replace(path="robots.txt", params="", query="", fragment="").geturl()
                rp = robotparser.RobotFileParser()
                rp.set_url(robotstxt_url)
                try:
                    rp.read()
                    can_crawl = rp.can_fetch("*", tbd_url)
                except:
                    can_crawl = True

                if can_crawl:
                    try:
                        resp = requests.get(url)
                    except:
                        self.frontier.mark_url_complete(tbd_url)
                        self.frontier.unblock_domain(tbd_url)
                        continue

                    self.event_loop.call_later(self.config.time_delay, self.unblock_domain, blocked_domain)
                    self.logger.info(f"Downloaded {tbd_url}, status <{resp.status_code}>")

                    document = {"url":tbd_url, "content":resp.text}
                    filename = str(abs(hash(tbd_url)))+".json"
                    with open(os.path.join("Data", "webpages", filename), "w+") as f:
                        json.dump(document, f)

                    scraped_urls = scraper.scraper(tbd_url, resp)
                    for scraped_url in scraped_urls:
                        self.frontier.add_url(scraped_url)
                    self.frontier.mark_url_complete(tbd_url)

                else:
                    self.frontier.mark_url_complete(tbd_url)
                    self.frontier.unblock_domain(blocked_domain)
                    continue

            await asyncio.sleep(self.config.time_delay)


    def unblock_domain(self, domain):
        self.frontier.unblock_domain(domain)
