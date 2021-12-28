#!/usr/bin/python3

"""Module to process incoming data."""

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import json


class LyricsSpiderPipeline:
    """Pipeline Class for LyricsSpider."""

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        """Pipeline function to process incoming data and store it.

        Args:
            item (scrapy.Item): item to be processed
            spider (scrapy.Spider): the spider which scraped the item
        """
        # TODO: clean data

        # Write to json
        self.convert_to_json(ItemAdapter(item).asdict(), 'rap.json')

        # TODO: Write to DB
        return item

    def convert_to_json(self, data: dict, file_name: str) -> None:
        """Create a file to convert scraped text into JSON format.

        Args:
            data (dict): dictionary with song lyrics
            file_name (str): JSON filename
        """
        json_object = json.dumps(data)

        with open(file_name, "a") as output_file:
            output_file.write("\n" + json_object)
