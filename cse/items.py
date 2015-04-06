#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy.item import Item, Field


class CseCrawlerItem(Item):
    url_id = Field()
    fetch_time = Field()
    url = Field()
    title = Field()
    content = Field()
    content_type = Field()
    encoding = Field()
