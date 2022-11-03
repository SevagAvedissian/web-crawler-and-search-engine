import re


class Config(object):
    def __init__(self, config):
        self.threads_count = int(config["CRAWLER"]["THREADCOUNT"])
        self.seed_urls = config["CRAWLER"]["SEEDURL"].split(",")
        self.time_delay = float(config["CRAWLER"]["POLITENESS"])

        self.cache_server = None