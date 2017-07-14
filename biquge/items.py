# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novel_id = scrapy.Field()
    novel_name = scrapy.Field()
    author = scrapy.Field()
    introduce = scrapy.Field()
    novel_link = scrapy.Field()
class ChapterContentItem(scrapy.Item):
    chapter_content = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_id = scrapy.Field()