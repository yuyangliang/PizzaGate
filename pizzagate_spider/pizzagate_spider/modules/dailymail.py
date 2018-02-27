from bs4 import BeautifulSoup
import time
from dateutil import parser
import re

from pizzagate_spider.modules.latimes import LatimesDP, LatimesIP

class DailymailDP(LatimesDP):	
	def dailymail_main(self):
		'''
		Output: CSS selectors for article information for Dailymail.
		'''
		article_selector = 'div[id="js-article-text"] div[itemprop="articleBody"]'
		date_time = self.soup.select('span[class="article-timestamp article-timestamp-published"]')[0].get_text().replace('Published:', '').strip()
		unixtime = time.mktime(parser.parse(date_time).timetuple())
		title_selector = 'div[id="js-article-text"] h1'
		author_selector = 'div[id="js-article-text"] a[class="author"]'
		links_selector = 'div[id="js-article-text"] p a'
		likes = ''
		has_more = True
		
		return (article_selector, date_time, unixtime, title_selector, author_selector, links_selector, likes, has_more)
	
	
	# def latimes_clean(self):
		# '''
		# Output: Clean author name.
		# '''
		# author = self.author
		# self.author = author.split('|')[1]

class DailymailIP(LatimesIP):
	def dailymail_instance(self):
		'''
		Output: Xpaths for instance information for Dailymail.
		'''
		
		instance_xpath = '//div[@class="container"]'
		datetime_xpath = './/p[@class="user-info"]/text()'
		content_html_xpath = './/p[@class="comment-body comment-text"]'
		author_xpath = './/a[@class="js-usr"]/text()'
		likes_xpath = './/div[@class="rating-button grey-rating-button rating-button-up"]//text()'
		links_contained_xpath = './/p[@class="comment-body comment-text"]/a/@href'
		id_xpath = './/a[@class="js-usr"]/text()'
		reply_to_xpath = '//reply'
		
		return (instance_xpath, datetime_xpath, content_html_xpath, author_xpath, likes_xpath, links_contained_xpath, id_xpath, reply_to_xpath)		
