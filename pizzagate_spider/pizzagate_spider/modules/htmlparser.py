from bs4 import BeautifulSoup
import time
import datetime
import re
from urllib.parse import urlparse
import logging


class DomainParser:
    def __init__(self, html, url):
        '''
		Input: Raw html and url of the site.
		Output: A BeautifulSoup object, the domain name and a list of keywords.
		'''
        self.soup = BeautifulSoup(html, 'lxml')
        self.domain = re.search(r'(\w+|\W+)(?=.(com|org|co.uk))', urlparse(url).netloc).group(1).lower()
        self.kwlst = [r'\bpedo\w+\b', r'\btraffick\w+\b', r'\bsex slave\b', r'\bchild sex\b', r'\bpizzagate\b',
                      r'\bchild slave\b', r'\bpederast\b', r'\babuse\b', r'\bpaedo\b']

    def inspect_article(self):
        '''
		Output: Text content and a True/False flag indicating if content is relevant.
		'''
        rawcontent = self.soup.select(self.article_selector)[0]

        for script in rawcontent(['script', 'style']):
            script.extract()

        self.content_html = str(rawcontent)
        self.content = rawcontent.get_text(" ", strip=True)
        self.title = self.soup.select(self.title_selector)[0].get_text()
        self.author = self.soup.select(self.author_selector)[0].get_text()
        self.links = self.soup.select(self.links_selector)
        self.content_flag = False

        for wd in self.kwlst:
            if not re.search(wd, self.content.lower()) == None:
                self.content_flag = True
                break

    def inspect_date(self):
        '''
		Output: A True/False flag indicating if date is before December 4, 2016.
		'''
        self.date_flag = (self.unixtime <= 1480827600.0)

    def get_domaininfo(self):
        '''
		Output: Assign class attributes based on domain.
		'''
        name = self.domain + '_main'
        self.article_selector, self.datetime, self.unixtime, self.title_selector, self.author_selector, self.links_selector, self.likes, self.has_more = getattr(
            self, name)()

    def clean_data(self):
        '''
		Output: Clean data.
		'''
        name = self.domain + '_clean'
        if hasattr(self, name):
            getattr(self, name)()


class InstanceParser:
    def __init__(self, url):
        '''
		Input: The url of the site.
		Output: The domain name.
		'''
        self.domain = re.search(r'(\w+|\W+)(?=.(com|org|co.uk))', urlparse(url).netloc).group(1).lower()

    def get_instanceinfo(self):
        '''
		Output: Assign class attributes based on domain.
		'''
        name = self.domain + '_instance'
        self.instance_xpath, self.datetime_xpath, self.content_html_xpath, self.author_xpath, self.likes_xpath, self.links_contained_xpath, self.id_xpath, self.reply_to_xpath = getattr(
            self, name)()

    def get_instanceinfo_json(self):
        '''
		Output: Assign class attributes based on domain that contains json.
		'''
        name = self.domain + '_instance'
        self.json_xpath, self.instance_selector, self.datetime_selector, self.content_selector, self.author_selector, self.likes_selector, self.id_selector, self.reply_to_selector = getattr(
            self, name)()
