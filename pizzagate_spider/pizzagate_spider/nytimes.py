from bs4 import BeautifulSoup
import time
from dateutil import parser
import re

from pizzagate_V1.modules.thelastamericanvagabond import ThelastamericanvagabondDP, ThelastamericanvagabondIP

class NytimesDP(ThelastamericanvagabondDP):	
	def nytimes_main(self):
		'''
		Output: CSS selectors for article information for Nytimes.
		'''
		article_selector = 'div[id="article"]'
		date_time = self.soup.select('h6[class="dateline"]')[0].get_text().replace('Published: ', '')
		unixtime = time.mktime(parser.parse(date_time).timetuple())
		title_selector = 'div[id="article"] h1[itemprop="headline"]'
		author_selector = 'div[id="article"] span[itemprop="name"]'
		links_selector = 'div[id="article"] p a'
		likes = ''
		has_more = False
		
		return (article_selector, date_time, unixtime, title_selector, author_selector, links_selector, likes, has_more)
	
	
	def nytimes_clean(self):
		'''
		Output: Clean author name.
		'''
		author = self.author
		self.author = author.replace('By ', '')	

class NytimesIP(ThelastamericanvagabondIP):
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
