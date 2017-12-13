from bs4 import BeautifulSoup
import time
import datetime
import re
from urlparse import urlparse

class DomainParser():
	def __init__(self, html, url):
		'''
		Input: Raw html and url of the site.
		Output: A BeautifulSoup object, the domain name and a list of keywords.
		'''
		self.soup = BeautifulSoup(html, 'lxml')
		self.domain = re.search(r'(\w+|\W+)(?=.(com|org))', urlparse(url).netloc).group(1).lower()
		self.kwlst = [r'\bpedo\w+\b', r'\btraffick\w+\b', r'\bsex slave\b', r'\bchild sex\b', r'\pizzagate\b', r'\bchild slave\b', r'\bpederast\b']
	
	def inspect_content(self):
		'''
		Output: Text content and a True/False flag indicating if content is relevant.
		'''
		rawcontent = self.soup.select(self.content_selector)[0]
		
		for script in rawcontent(['script', 'style']):
			script.extract()
			
		self.content = rawcontent.get_text(" ", strip = True)
		
		for wd in self.kwlst:
			if not re.search(wd, self.content.lower()) == None:
				self.content_flag = True
				break
	
	def inspect_date(self):
		'''
		Output: A True/False flag indicating if date is before December 4, 2016.
		'''
		self.date_flag = (self.unixtime <= 1480827600.0)
		
	def get_path_timestamp(self):
		'''
		Output: Assign attributes based on domain.
		'''
		self.content_selector, self.link_xpath, self.unixtime = getattr(self, self.domain)()
		
	def yournewswire(self):
		'''
		Output: CSS selector for content, Xpath for extracting links, Unix timestamp for Yournewswire
		'''
		content_selector = 'div[class="mh-main clearfix"]'
		link_xpath = '//div[@class="mh-main clearfix"]'
		date = self.soup.select('span[class="entry-meta-date updated"]')[0].get_text()
		unixtime = time.mktime(datetime.datetime.strptime(date, "%B %d, %Y").timetuple())
		
		return (content_selector, link_xpath, unixtime)
		
	def truepundit(self):
		'''
		Output: CSS selector for content, Xpath for extracting links, Unix timestamp for Truepundit
		'''
		content_selector = 'section[id="page-content"]'
		link_xpath = '//div[starts-with(@id, "post-")]'
		date = self.soup.select('time')[0].get_text()
		unixtime = time.mktime(datetime.datetime.strptime(date, "%B %d, %Y").timetuple())
		
		return (content_selector, link_xpath, unixtime)		
	
	def reddit(self):
		'''
		Output: CSS selector for content, Xpath for extracting links, Unix timestamp for Reddit
		'''
		content_selector = 'div[class="content"]'
		link_xpath = '//div[contains(@class, "usertext-body")]'
		date = self.soup.select('div[class="date"] > time')[0].get_text()
		unixtime = time.mktime(datetime.datetime.strptime(date, "%d %b %Y").timetuple())
		
		return (content_selector, link_xpath, unixtime)		
		
	def steemit(self):
		'''
		Output: CSS selector for content, Xpath for extracting links, Unix timestamp for steemit
		'''
		content_selector = 'div[class="Post"]'
		link_xpath = '//div[contains(@class, "entry-content")]'
		date = self.soup.select('div[class="PostFull__header"] span[class="updated"]')[0]['title']
		unixtime = time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y %I:%M %p").timetuple())
		
		return (content_selector, link_xpath, unixtime)			