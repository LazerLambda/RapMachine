#!/usr/bin/python3

"""Item container class for LyricsSpider."""

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LyricsSpiderItem(scrapy.Item):
    """Class to init data structure for storing."""

    url = scrapy.Field()  # TODO: only in dev
    title = scrapy.Field()
    lyrics = scrapy.Field()
