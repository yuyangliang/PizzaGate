# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):
	author = scrapy.Field()
	url = scrapy.Field()
	datetime = scrapy.Field()
	title = scrapy.Field()
	domain = scrapy.Field()

class InstanceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	author = scrapy.Field()
	datetime = scrapy.Field()
	links_contained = scrapy.Field()
	url = scrapy.Field()
	id = scrapy.Field()
	type = scrapy.Field()
	likes = scrapy.Field()
	text_body = scrapy.Field()
	text_body_html = scrapy.Field()
	reply_to = scrapy.Field()
	relevance = scrapy.Field()
	unixtime = scrapy.Field()
	gen_time = scrapy.Field()
	
class LinkItem(scrapy.Item):
	url = scrapy.Field()
	response = scrapy.Field()
	parsable = scrapy.Field()
	
class LinkRItem(scrapy.Item):
	link_from = scrapy.Field()
	link_to = scrapy.Field()
	gen_time = scrapy.Field()