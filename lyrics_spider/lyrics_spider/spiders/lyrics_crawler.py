#!/usr/bin/python3

"""Program for crawling websites with rap lyrics and scraping their textual data."""


import logging
from scrapy.crawler import CrawlerProcess
from .BattlerapComSpider import BattlerapComSpider
from .OhhlaComSpider import OhhlaComSpider

logging.basicConfig(filename='lyrics_crawler.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# TODO: Error handling

process = CrawlerProcess()
process.crawl(BattlerapComSpider)
process.crawl(OhhlaComSpider)
process.start()
