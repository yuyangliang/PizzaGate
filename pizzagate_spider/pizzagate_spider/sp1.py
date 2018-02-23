# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
import re
from bs4 import BeautifulSoup
from pizzagate_V1.modules.alldomain import DP, IP
from pizzagate_V1.items import ArticleItem, InstanceItem, LinkItem, LinkRItem
import logging
from src.json2xml import Json2xml
from pizzagate_V1.modules.domain_specifications import parsable_domain_list, json2xml_list
import time
import dateparser
from pizzagate_V1.modules.start_urls import urls

class Sp1Spider(scrapy.Spider):
	name = 'sp1'
	#allowed_domains = ['https://www.reddit.com/']
	#start_urls = urls
	start_urls = ['http://www.dailymail.co.uk/news/article-3643373/PICTURED-sinister-holiday-villa-paedophile-MP-Clement-Freud-hosted-McCanns-weeks-Madeleine-vanished.html']
	# start_urls = ['https://www.reddit.com/r/The_Donald/comments/5aupnh/breaking_i_believe_i_have_connected_a_convicted/',
	# 'https://truepundit.com/breaking-bombshell-nypd-blows-whistle-on-new-hillary-emails-money-laundering-sex-crimes-with-children-child-exploitation-pay-to-play-perjury/', 
	# 'http://yournewswire.com/fbi-clinton-email-pedophile-ring/',
	# 'https://steemit.com/comet/@bitcoinnational/pizzagate-pedophila-and-cheese-pizza-warning-washington-dc-contains-murderous-perverts']

	logging.getLogger().setLevel(logging.WARNING)
	handle_httpstatus_list = [301, 302, 400, 404, 500]
	
	def start_requests(self):
		''' De-duplicate the start urls '''
		for url in self.start_urls:
			yield scrapy.Request(url)

	def parse(self, response):
		linkitem = LinkItem()
		linkitem['url'] = response.url
		linkitem['response'] = response.status
		linkitem['parsable'] = any(d in response.url for d in parsable_domain_list)
			
		yield linkitem
		
		try:
		
			rawhtml = response.xpath('//html').extract()[0]
			article = DP(html = rawhtml, url = response.url)
			article.get_domaininfo()
			article.inspect_date()
			url_retrieved = []
			url_validate = re.compile(r'^https?')
			#logging.info(article.date_flag)
			#logging.info(article.has_more)
			
			if article.date_flag:
				article.inspect_article()
				article.clean_data()
			
			if article.content_flag:
				articleitem = ArticleItem()
				instanceitem = InstanceItem()
				linkritem = LinkRItem()
				
				articleitem['author'] = article.author
				articleitem['url'] = response.url
				articleitem['title'] = article.title
				articleitem['datetime'] = article.unixtime
				articleitem['domain'] = article.domain
				
				yield articleitem
				
				#main article as an instance
				instanceitem['author'] = article.author
				instanceitem['url'] = response.url
				instanceitem['datetime'] = article.datetime
				instanceitem['unixtime'] = article.unixtime
				instanceitem['type'] = 'Article'
				instanceitem['text_body'] = article.content
				instanceitem['text_body_html'] = article.content_html
				instanceitem['likes'] = article.likes
				instanceitem['links_contained'] = []
				instanceitem['relevance'] = article.content_flag
				instanceitem['gen_time'] = time.time()
				for link in article.links:
					if not url_validate.search(str(link['href'])) == None: 
						instanceitem['links_contained'].append(link['href'])
						linkritem['link_from'] = response.url
						linkritem['link_to'] = link['href']
						linkritem['gen_time'] = instanceitem['gen_time']
						yield linkritem
						url_retrieved.append(str(link['href']))
						yield scrapy.Request(str(link['href']), callback = self.parse)
					
				instanceitem['links_contained'] = ','.join(instanceitem['links_contained'])
					
				yield instanceitem
				
			if article.has_more:
				instance = IP(url = response.url)
				if instance.domain in json2xml_list:
					instance.get_instanceinfo_json()
					#logging.info(instance.json_xpath)
					
					json_data = Json2xml.fromstring(response.xpath(instance.json_xpath).extract_first()).data
					json_object = Json2xml(json_data).json2xml()
					
					instance_iter = BeautifulSoup(json_object, 'lxml').select(instance.instance_selector)
					#logging.info(len(instance_iter))
					for i in instance_iter:
						instanceitem['author'] = i.find(instance.author_selector).get_text()
						instanceitem['url'] = response.url			
						instanceitem['datetime'] = i.find_all(instance.datetime_selector)[-1].get_text()
						instanceitem['unixtime'] = time.mktime(dateparser.parse(instanceitem['datetime']).timetuple())
						instanceitem['type'] = 'Comment'
						instanceitem['text_body_html'] = ''
						instanceitem['text_body'] = i.find_all(instance.content_selector)[-1].get_text()
						instanceitem['likes'] = ''
						instanceitem['id'] = i.find_all('url')[-1].get_text()
						instanceitem['reply_to'] = ''
						instanceitem['links_contained'] = re.findall(r'(https?://[^\s]+)', instanceitem['text_body'])
						instanceitem['relevance'] = article.content_flag
						instanceitem['gen_time'] = time.time()
						for link in instanceitem['links_contained']:
							if not url_validate.search(str(link)) == None: 
								linkritem['link_from'] = response.url
								linkritem['link_to'] = str(link)
								linkritem['gen_time'] = instanceitem['gen_time']
								yield linkritem
								url_retrieved.append(str(link))
								yield scrapy.Request(str(link), callback = self.parse)
						
						instanceitem['links_contained'] = ','.join(instanceitem['links_contained'])
						
						if not instanceitem['text_body'] == None:
							yield instanceitem
				
				else:
					instance.get_instanceinfo()
					
					instance_iter = response.xpath(instance.instance_xpath)
					for i in instance_iter:
						instanceitem['author'] = i.xpath(instance.author_xpath).extract_first()
						instanceitem['url'] = response.url			
						instanceitem['datetime'] = i.xpath(instance.datetime_xpath).extract_first()
						instanceitem['unixtime'] = time.mktime(dateparser.parse(instanceitem['datetime']).timetuple())
						instanceitem['type'] = 'Comment'
						instanceitem['text_body_html'] = i.xpath(instance.content_html_xpath).extract_first()
						instanceitem['likes'] = i.xpath(instance.likes_xpath).extract_first()
						instanceitem['id'] = i.xpath(instance.id_xpath).extract_first()
						instanceitem['reply_to'] = i.xpath(instance.reply_to_xpath).extract_first()
						instanceitem['links_contained'] = i.xpath(instance.links_contained_xpath).extract()
						instanceitem['relevance'] = article.content_flag
						instanceitem['gen_time'] = time.time()
						for link in instanceitem['links_contained']:
							if not url_validate.search(str(link)) == None: 
								linkritem['link_from'] = response.url
								linkritem['link_to'] = str(link)
								linkritem['gen_time'] = instanceitem['gen_time']
								yield linkritem
								url_retrieved.append(str(link))
								yield scrapy.Request(str(link), callback = self.parse)
						
						instanceitem['links_contained'] = ','.join(instanceitem['links_contained'])
						
						if not instanceitem['text_body_html'] == None:
							instanceitem['text_body'] = BeautifulSoup(instanceitem['text_body_html'], 'lxml').get_text().strip()
							yield instanceitem
			
			# if not len(url_retrieved) == 0:
				# url_retrieved = list(set(url_retrieved))
				
				# urlfile = open('urls.txt', 'a')
				# for link in url_retrieved:
					# urlfile.write("{}\n".format(link))
					# yield scrapy.Request(link, callback = self.parse)
		
		except Exception as e:
			#pass
			raise