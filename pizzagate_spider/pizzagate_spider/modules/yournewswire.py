from bs4 import BeautifulSoup
import time
import datetime

from pizzagate_V1.modules.reddit import RedditDP, RedditIP

class YournewswireDP(RedditDP):	
	def yournewswire_main(self):
		'''
		Output: CSS selectors for article information for Yournewswire.
		'''
		article_selector = 'article' 
		date_time = self.soup.select('span[class="entry-meta-date updated"]')[0].get_text()
		unixtime = time.mktime(datetime.datetime.strptime(date_time, "%B %d, %Y").timetuple())
		title_selector = 'h1[class="entry-title"]'
		author_selector = 'a[class="fn"]' 
		links_selector = 'div[class="entry-content clearfix"] a'
		likes = None
		has_more = True
		
		return (article_selector, date_time, unixtime, title_selector, author_selector, links_selector, likes, has_more)			
		
class YournewswireIP(RedditIP):
	def yournewswire_instance(self):
		'''
		Output: Xpaths for instance information for Yournewswire.
		'''
		instance_xpath = '//li[contains(@id, "dsq-comment")]'
		datetime_xpath = '//date'
		content_html_xpath = './/div[contains(@id, "dsq-comment-message")]/p'
		author_xpath = './/span[contains(@id, "dsq-author-user")]/text()'
		likes_xpath = '//likes'
		links_contained_xpath = './/div[contains(@id, "dsq-comment-message")]/p/a/@href'
		id_xpath = './/span[contains(@id, "dsq-author-user")]/text()'
		reply_to_xpath = '//reply'
		
		return (instance_xpath, datetime_xpath, content_html_xpath, author_xpath, likes_xpath, links_contained_xpath, id_xpath, reply_to_xpath)		
