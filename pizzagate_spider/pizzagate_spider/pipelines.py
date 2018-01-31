# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class PizzagateSpiderPipeline(object):
	def __init__(self):
		self.setupDBCon()
	
	def setupDBCon(self):
		self.con = sqlite3.connect('Database/test.db')
		self.cur = self.con.cursor()
		
	def closeDB(self):
		self.con.close()
		
	def __del__(self):
		self.closeDB()
	
	def process_item(self, item, spider):
		if item.__class__.__name__ == 'ArticleItem':
			self.storeInDB_article(item)
		if item.__class__.__name__ == 'InstanceItem':
			self.storeInDB_instance(item)
		if item.__class__.__name__ == 'LinkItem':
			self.storeInDB_link(item)
		if item.__class__.__name__ == 'LinkRItem':
			self.storeInDB_linkrel(item)			
		return item
		
	def storeInDB_article(self, item):
		self.cur.execute(\
		"INSERT INTO article(author, url, title, datetime, domain, unixtime) \
		VALUES(?, ?, ?, ?, ?, ?)", \
		(item.get('author', ''), item.get('url', ''), item.get('title', ''), item.get('datetime', ''), item.get('domain', ''), item.get('unixtime', '') ))
		
		print('Article Added in Database')
		self.con.commit()
		
	def storeInDB_instance(self, item):
		self.cur.execute(\
		"INSERT INTO instance(url, text_body, text_body_html, links_contained, datetime, author, id, type, likes, reply_to, relevance, unixtime) \
		VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
		(item.get('url', ''), item.get('text_body', ''), item.get('text_body_html', ''), item.get('links_contained', ''), item.get('datetime', ''),  item.get('author', ''), item.get('id', ''), item.get('type', ''), item.get('likes', ''), item.get('reply_to', ''), item.get('relevance', ''), item.get('unixtime', '') ))
		
		print('Instance Added in Database')
		self.con.commit()
		
	def storeInDB_link(self, item):
		self.cur.execute(\
		"INSERT INTO link(url, response, parsable) \
		VALUES(?, ?, ?)", \
		(item.get('url', ''), item.get('response', ''), item.get('parsable', '') ))
		
		#print('Link Added in Database')
		self.con.commit()	
		
	def storeInDB_linkrel(self, item):
		self.cur.execute(\
		"INSERT INTO link_relation(link_from, link_to) \
		VALUES(?, ?)", \
		(item.get('link_from', ''), item.get('link_to', '') ))
		
		#print('Link Added in Database')
		self.con.commit()				