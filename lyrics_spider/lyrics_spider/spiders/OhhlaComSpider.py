#!/usr/bin/python3

"""Module for Scraping ohhla.com."""

import logging
import scrapy
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess

from ..items import LyricsSpiderItem


class OhhlaComSpider(CrawlSpider):
    """Spider-Class for ohhla.com."""

    name = 'ohhla_crawler'
    allowed_domains = ['ohhla.com']
    start_urls = ['http://www.ohhla.com/all.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'lyrics_spider.pipelines.LyricsSpiderPipeline': 300
        }
    }

    # NOTE: hardcoded with tags from websites
    # TODO: add more lyrics websites to crawler (e.g. Genius)
    # specification of the links that should be followed to get the data

    ohhla_artists = LinkExtractor(restrict_css='pre > a')
    ohhla_albums_and_songs = LinkExtractor(deny=r'Parent Directory', restrict_css='td > a')
    ohhla_pagination = LinkExtractor(restrict_xpaths=('//a[contains(@href,"all_two")]',
                                                      '//a[contains(@href,"all_three")]',
                                                      '//a[contains(@href,"all_four")]',
                                                      '//a[contains(@href,"all_five")]'))

    # rules which the crawler has to follow for the different websites
    rule_artists_ohhla = Rule(ohhla_artists, follow=True)
    rule_albums_ohhla = Rule(ohhla_albums_and_songs, callback='parse_ohhla', follow=True)
    rule_pages_ohhla = Rule(ohhla_pagination, follow=True)

    rules = (
        rule_artists_ohhla, rule_albums_ohhla, rule_pages_ohhla
    )

    def parse_ohhla(self, response: scrapy.http.response.html.HtmlResponse) -> None:
        """Parse the ohhla.com rap lyrics database.

        Args:
            response (scrapy.http.response.html.HtmlResponse): scrapy response
        """
        # grab the HTML where the lyrics are stored on the website
        lyrics = response.css('pre::text').get()
        title = None
        if lyrics is not None:
            song = re.search(r"(Song:\s+)(.*?)\n", lyrics)
            if bool(song):
                title = song.group(2)

                lyricx_tmp = re.search(r"((t|T)yped (b|B)y:\s+)(.*?)(\n+)(.*)", lyrics, re. DOTALL)
                if bool(lyricx_tmp):
                    lyrics = lyricx_tmp.group(6)
                else:
                    from_song = re.search(r"(Song:\s+)(.*?)(\n+)(.*)", lyrics, re. DOTALL)
                    lyrics = from_song.group(4) if bool(from_song) is not None else lyrics

            # lyrics = lyrics.splitlines()

        item = LyricsSpiderItem()

        # TODO: Find title
        item['url'] = response.request.url
        item['title'] = title
        item['lyrics'] = lyrics

        yield item
