from bs4 import BeautifulSoup
import time
import datetime

from pizzagate_V1.modules.htmlparser import DomainParser, InstanceParser

class RedditDP(DomainParser):	
	def reddit_main(self):
		'''
		Output: CSS selectors for article information for Reddit.
		'''
		article_selector = 'div[id="siteTable"]'
		date_time = self.soup.select('div[id="siteTable"] time')[0]['title']
		unixtime = time.mktime(datetime.datetime.strptime(date_time, "%a %b %d %X %Y %Z").timetuple())
		title_selector = 'a[class~="title"]'
		author_selector = 'a[class~="author"]'
		links_selector = 'div[class="entry unvoted"] a'
		likes = self.soup.select('div[class="score unvoted"]')[0]['title']
		has_more = True
		
		return (article_selector, date_time, unixtime, title_selector, author_selector, links_selector, likes, has_more)			
		
class RedditIP(InstanceParser):
	def reddit_instance(self):
		'''
		Output: Xpaths for instance information for Reddit.
		'''
		instance_xpath = '//div[@class="commentarea"]//div[@class="entry unvoted"]'
		datetime_xpath = './/time[@class="live-timestamp"]/@title'
		content_html_xpath = './/div[@class="md"]'
		author_xpath = './/a[contains(@class, "author")]/text()'
		likes_xpath = './/span[@class="score unvoted"]/@title'
		links_contained_xpath = './/div[@class="md"]//a/@href'
		id_xpath = './/input/@value'
		reply_to_xpath = './/a[@data-event-action="parent"]/@href'
		
		return (instance_xpath, datetime_xpath, content_html_xpath, author_xpath, likes_xpath, links_contained_xpath, id_xpath, reply_to_xpath)		