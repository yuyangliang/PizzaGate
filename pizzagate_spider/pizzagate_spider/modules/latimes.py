from bs4 import BeautifulSoup
import time
from dateutil import parser
import re

from pizzagate_spider.modules.nytimes import NytimesDP, NytimesIP

class LatimesDP(NytimesDP):	
	def latimes_main(self):
		'''
		Output: CSS selectors for article information for Latimes.
		'''
		article_selector = 'div[id="area-center-w-left"] div[id="area-article-first-block"]'
		date_time = self.soup.select('span[class="pubdate"]')[0].get_text()
		unixtime = time.mktime(parser.parse(date_time).timetuple())
		title_selector = 'div[id="area-center-w-left"] h1[class="multi-line-title-1"]'
		author_selector = 'div[id="area-center-w-left"] div[id="mod-article-byline"]'
		links_selector = 'div[id="area-center-w-left"] p a'
		likes = ''
		has_more = False
		
		return (article_selector, date_time, unixtime, title_selector, author_selector, links_selector, likes, has_more)
	
	
	def latimes_clean(self):
		'''
		Output: Clean author name.
		'''
		author = self.author
		self.author = author.split('|')[1]

class LatimesIP(NytimesIP):
	pass
	# def thelastamericanvagabond_instance(self):
		# '''
		# Output: Xpaths for instance information for Thelastamericanvagabond.
		# '''
		
		# instance_xpath = '//div[@class="comment"]'
		# datetime_xpath = './/div[@class="comment_date"]/text()'
		# content_html_xpath = './/div[@class="right"]'
		# author_xpath = './/strong/text()'
		# likes_xpath = './/likes'
		# links_contained_xpath = './/p/a/@href'
		# id_xpath = './/strong/text()'
		# reply_to_xpath = '//reply'
		
		# return (instance_xpath, datetime_xpath, content_html_xpath, author_xpath, likes_xpath, links_contained_xpath, id_xpath, reply_to_xpath)		
