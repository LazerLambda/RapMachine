#!/usr/bin/python3

"""Program for crawling websites with rap lyrics and scraping their textual data"""


import json
import logging
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


logging.basicConfig(filename='lyrics_crawler.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class LyricsCrawlerSpider(CrawlSpider):
    name = 'lyrics_crawler'
    allowed_domains = ['battlerap.com', 'ohhla.com']
    start_urls = ['http://battlerap.com/lyrics/', 'http://www.ohhla.com/all.html']

    #NOTE: hardcoded with tags from websites
    #TODO: add more lyrics websites to crawler (e.g. Genius)
    # specification of the links that should be followed to get the data
    battlerap_artists = LinkExtractor(restrict_css='h2> a')
    battlerap_pagination = LinkExtractor(restrict_xpaths='//a[@class="next page-numbers"]')
    ohhla_artists = LinkExtractor(restrict_css='pre > a')
    ohhla_albums_and_songs = LinkExtractor(deny=r'Parent Directory', restrict_css='td > a')
    ohhla_pagination = LinkExtractor(restrict_xpaths=('//a[contains(@href,"all_two")]',
                                                      '//a[contains(@href,"all_three")]',
                                                      '//a[contains(@href,"all_four")]',
                                                      '//a[contains(@href,"all_five")]'))
    
    # rules which the crawler has to follow for the different websites
    rule_lyrics_battlerap = Rule(battlerap_artists, callback='parse_battlerap', follow=False)
    rule_pages_battlerap = Rule(battlerap_pagination, follow=True)
    rule_artists_ohhla = Rule(ohhla_artists, follow=True)
    rule_albums_ohhla = Rule(ohhla_albums_and_songs, callback='parse_ohhla', follow=True)
    rule_pages_ohhla = Rule(ohhla_pagination, follow=True)

    rules = (
        rule_lyrics_battlerap, rule_pages_battlerap, rule_artists_ohhla, rule_albums_ohhla, rule_pages_ohhla
    )
    
    
    def convert_to_json(self, data: dict, file_name: str) -> None:
        """Create a file to convert scraped text into JSON format.

        Args:
            data (dict): dictionary with song lyrics
            file_name (str): JSON filename
        """
        json_object = json.dumps(data)

        with open(file_name, "a") as output_file:
            output_file.write(json_object)


    def parse_battlerap(self, response: scrapy.http.response.html.HtmlResponse) -> None:
        """Parse battlerap lyrics from battlerap.com website.

        Args:
            response (scrapy.http.response.html.HtmlResponse): scrapy resonse
        """
        # get the title and lyrics from the website for further processing
        battle_title = response.css('h1.entry-title::text').get()
        main_content = response.css('div.entry-content')
        lyrics = main_content.css('p::text').getall()

        battlerap_lyrics = {
            battle_title: lyrics
        }

        self.convert_to_json(battlerap_lyrics, "battlerap.json")
        
    

    def parse_ohhla(self, response: scrapy.http.response.html.HtmlResponse) -> None:
        """Parse the ohhla.com rap lyrics database.

        Args:
            response (scrapy.http.response.html.HtmlResponse): scrapy response
        """
        # grab the HTML where the lyrics are stored on the website
        lyrics = response.css('pre::text').get()

        rap_lyrics = {
            "Song": lyrics
        }

        self.convert_to_json(rap_lyrics, "rap_songs.json")


    #TODO: Error handling
