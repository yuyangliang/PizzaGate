# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy.spiders import CrawlSpider, Rule
import re
from htmlparser import DomainParser, InstanceParser
from pizzagate_spider.items import ArticleItem, InstanceItem
import logging

class Sp1Spider(scrapy.Spider):
	name = 'sp1'
    allowed_domains = ['https://www.reddit.com/']
	start_urls = ['https://www.reddit.com/r/The_Donald/comments/5aupnh/breaking_i_believe_i_have_connected_a_convicted/']
	# start_urls = ['https://www.reddit.com/r/The_Donald/comments/5aupnh/breaking_i_believe_i_have_connected_a_convicted/',
	# 'http://truepundit.com/breaking-bombshell-nypd-blows-whistle-on-new-hillary-emails-money-laundering-sex-crimes-with-children-child-exploitation-pay-to-play-perjury/', 
	# 'http://yournewswire.com/fbi-clinton-email-pedophile-ring/',
	# 'https://steemit.com/comet/@bitcoinnational/pizzagate-pedophila-and-cheese-pizza-warning-washington-dc-contains-murderous-perverts']

	logging.getLogger().setLevel(logging.DEBUG)

	def parse(self, response):
		try:
			rawhtml = response.xpath('//html').extract()[0]
			article = DomainParser(html = rawhtml, url = response.url)
			article.get_domaininfo()
			article.inspect_date()
			logging.debug(article.date_flag)
			
			if article.date_flag:
				article.inspect_article()
				logging.debug(article.content_flag)
			
			if article.content_flag:
				articleitem = ArticleItem()
				instanceitem = InstanceItem()
				
				articleitem['author'] = article.author
				articleitem['url'] = response.url
				articleitem['title'] = article.title
				articleitem['datetime'] = article.unixtime
				logging.debug(article.datetime)
				articleitem['domain'] = article.domain
				
				yield articleitem
				
				url_retrieved = []
				
				#main article as an instance
				instanceitem['author'] = article.author
				instanceitem['url'] = response.url
				instanceitem['datetime'] = article.datetime
				instanceitem['type'] = 'Article'
				instanceitem['text_body'] = article.content
				instanceitem['text_body_html'] = article.content_html
				instanceitem['likes'] = article.likes
				instanceitem['links_contained'] = []
				for link in article.links:
					instanceitem['links_contained'].append(link['href'])
					url_retrieved.append(str(link['href']))
					
				instanceitem['links_contained'] = ','.join(instanceitem['links_contained'])
					
				yield instanceitem
				
			instance = InstanceParser(url = response.url)
			instance.get_instanceinfo()
			
			instance_iter = response.xpath(instance.instance_xpath)
			for i in instance_iter:
				instanceitem['author'] = i.xpath(instance.author_xpath).extract_first()
				instanceitem['url'] = response.url
				instanceitem['datetime'] = i.xpath(instance.datetime_xpath).extract_first()
				instanceitem['type'] = 'Comment'
				instanceitem['text_body'] = ''.join(i.xpath(instance.content_xpath).extract()).strip()
				instanceitem['text_body_html'] = i.xpath(instance.content_html_xpath).extract_first()
				instanceitem['likes'] = i.xpath(instance.likes_xpath).extract_first()
				instanceitem['id'] = i.xpath(instance.id_xpath).extract_first()
				instanceitem['reply_to'] = i.xpath(instance.reply_to_xpath).extract_first()
				instanceitem['links_contained'] = i.xpath(instance.links_contained_xpath).extract()
				for link in instanceitem['links_contained']:
					url_retrieved.append(str(link))
					
				instanceitem['links_contained'] = ','.join(instanceitem['links_contained'])
					
				if not instanceitem['text_body_html'] == None:
					yield instanceitem
					
			url_retrieved = list(set(url_retrieved))
			logging.debug(url_retrieved)
			
			for link in url_retrieved:
				yield scrapy.Request(link, callback = self.parse)
		
		except:
			pass
			
	def start_requests(self):
		''' De-duplicate the start urls '''
		for url in self.start_urls:
			yield scrapy.Request(url)