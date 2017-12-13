# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from htmlparser import DomainParser

class Sp1Spider(scrapy.Spider):
    name = 'sp1'
    #allowed_domains = ['https://www.reddit.com/r/The_Donald/comments/5aupnh/breaking_i_believe_i_have_connected_a_convicted/']
    start_urls = ['http://https://www.reddit.com/r/The_Donald/comments/5aupnh/breaking_i_believe_i_have_connected_a_convicted//',
	'http://truepundit.com/breaking-bombshell-nypd-blows-whistle-on-new-hillary-emails-money-laundering-sex-crimes-with-children-child-exploitation-pay-to-play-perjury/', 
	'http://yournewswire.com/fbi-clinton-email-pedophile-ring/',
	'https://steemit.com/comet/@bitcoinnational/pizzagate-pedophila-and-cheese-pizza-warning-washington-dc-contains-murderous-perverts']

	def parse(self, response):
		try:
			rawhtml = response.xpath('//html').extract()[0]
			site = DomainParser(html = rawhtml, url = response.url)
			site.get_path_timestamp()
			site.inspect_date()
			
			if site.date_flag:
				site.inspect_content()
			
			if site.content_flag:
				url_retrieved = []
				extractor = LinkExtractor(restrict_xpaths = (site.link_xpath))
				links = extractor.extract_links(response)
			
				for link in links:
					url_retrieved.append(link.url)
					yield scrapy.Request(link.url, callback = self.parse)
				
				yield{'content': site.content, 'retrieved_url': url_retrieved, 'current_url': response.url, 'unixtime': site.unixtime}
		
		except:
			pass
			
	def start_requests(self):
		''' De-duplicate the start urls '''
		for url in self.start_urls:
			yield scrapy.Request(url)