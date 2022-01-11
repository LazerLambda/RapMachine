#!/usr/bin/python3

"""Module for Scraping battlerap.com."""

import logging
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess

from ..items import LyricsSpiderItem


class BattlerapComSpider(CrawlSpider):
    """Spider-Class for battlerap.com."""

    name = 'lyrics_crawler'
    allowed_domains = ['battlerap.com']
    start_urls = ['http://battlerap.com/lyrics/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'lyrics_spider.pipelines.LyricsSpiderPipeline': 300
        }
    }

    # NOTE: hardcoded with tags from websites
    # TODO: add more lyrics websites to crawler (e.g. Genius)
    # specification of the links that should be followed to get the data
    battlerap_artists = LinkExtractor(
        restrict_css='h2> a')
    battlerap_pagination = LinkExtractor(
        restrict_xpaths='//a[@class="next page-numbers"]')

    # rules which the crawler has to follow for the different websites
    rule_lyrics_battlerap = Rule(
        battlerap_artists,
        callback='parse_battlerap',
        follow=False)
    rule_pages_battlerap = Rule(
        battlerap_pagination,
        follow=True)

    rules = (
        rule_lyrics_battlerap, rule_pages_battlerap
    )

    def parse_battlerap(self, response: scrapy.http.response.html.HtmlResponse) -> None:
        """Parse battlerap lyrics from battlerap.com website.

        Args:
            response (scrapy.http.response.html.HtmlResponse): scrapy resonse
        """
        # get the title and lyrics from the website for further processing
        battle_title = response.css('h1.entry-title::text').get()
        main_content = response.css('div.entry-content')
        lyrics = main_content.css('p::text').getall()

        item = LyricsSpiderItem()

        # TODO: Find title
        item['url'] = response.request.url
        item['title'] = battle_title
        item['lyrics'] = lyrics

        yield item
