from configparser import ConfigParser
from argparse import ArgumentParser

from utils.config import Config
from crawler import Crawler

def main(config_file):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    crawler = Crawler(config)
    crawler.start()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file)

