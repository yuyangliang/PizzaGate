from bs4 import BeautifulSoup
import time
from dateutil import parser
import re

from pizzagate_spider.modules.steemit import SteemitDP, SteemitIP

class ThelastamericanvagabondDP(SteemitDP):	
	def thelastamericanvagabond_main(self):
		'''
		Output: CSS selectors for article information for Thelastamericanvagabond.
		'''
		article_selector = 'div[class="post_wrapper"]'
		date_time = self.soup.select('div[class="post_detail"]')[0].get_text().split('  ')[0]
		unixtime = time.mktime(parser.parse(date_time).timetuple())
		title_selector = 'div[class="post_wrapper"] div[class="post_header"] h2'
		author_selector = 'div[class="post_wrapper"] div[class="post_detail"]'
		links_selector = 'div[class="post_wrapper"] p a'
		likes = ''
		has_more = True
		
		return (article_selector, date_time, unixtime, title_selector, author_selector, links_selector, likes, has_more)
	
	def thelastamericanvagabond_clean(self):
		'''
		Output: Clean author name.
		'''
		author = self.author
		self.author = re.search('(?<=(Posted by )).+', author).group(0).strip()

class ThelastamericanvagabondIP(SteemitIP):
	def thelastamericanvagabond_instance(self):
		'''
		Output: Xpaths for instance information for Thelastamericanvagabond.
		'''
		
		instance_xpath = '//div[@class="comment"]'
		datetime_xpath = './/div[@class="comment_date"]/text()'
		content_html_xpath = './/div[@class="right"]'
		author_xpath = './/strong/text()'
		likes_xpath = './/likes'
		links_contained_xpath = './/p/a/@href'
		id_xpath = './/strong/text()'
		reply_to_xpath = '//reply'
		
		return (instance_xpath, datetime_xpath, content_html_xpath, author_xpath, likes_xpath, links_contained_xpath, id_xpath, reply_to_xpath)		
