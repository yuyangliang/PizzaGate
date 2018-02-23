from bs4 import BeautifulSoup
import time
from dateutil import parser

from pizzagate_V1.modules.yournewswire import YournewswireDP, YournewswireIP

class TruepunditDP(YournewswireDP):	
	def truepundit_main(self):
		'''
		Output: CSS selectors for article information for Truepundit.
		'''
		article_selector = 'div[id^="post-"]'
		date_time = self.soup.select('time')[0].get_text()
		unixtime = time.mktime(parser.parse(date_time).timetuple())
		title_selector = 'div[id^="post-"] h2[class="blog-post"]'
		author_selector = 'div[id^="post-"] span[class="author-bayside"] > a' 
		links_selector = 'div[id^="post-"] p a'
		likes = None
		has_more = False
		
		return (article_selector, date_time, unixtime, title_selector, author_selector, links_selector, likes, has_more)			

class TruepunditIP(YournewswireIP):
	pass
	# def truepundit_instance(self):
		# '''
		# Output: Xpaths for instance information for truepundit.
		# '''
		# instance_xpath = '//li[contains(@id, "dsq-comment")]'
		# datetime_xpath = '//date'
		# content_html_xpath = './/div[contains(@id, "dsq-comment-message")]/p'
		# author_xpath = './/span[contains(@id, "dsq-author-user")]/text()'
		# likes_xpath = '//likes'
		# links_contained_xpath = './/div[contains(@id, "dsq-comment-message")]/p/a/@href'
		# id_xpath = './/span[contains(@id, "dsq-author-user")]/text()'
		# reply_to_xpath = '//reply'
		
		# return (instance_xpath, datetime_xpath, content_html_xpath, author_xpath, likes_xpath, links_contained_xpath, id_xpath, reply_to_xpath)		
