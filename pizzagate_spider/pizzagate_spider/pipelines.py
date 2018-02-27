# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from pizzagate_spider.settings import DB_NAME

class PizzagateSpiderPipeline(object):
    def __init__(self):
        self.setupDBCon()

    def setupDBCon(self):
        self.con = sqlite3.connect(DB_NAME)
        self.cur = self.con.cursor()
        self.createSchema()

    def createSchema(self):
        self.cur.execute("""CREATE TABLE if not exists instance
(
  author          TEXT,
  datetime        TEXT,
  unixtime        TEXT,
  links_contained TEXT,
  url             TEXT,
  id              TEXT,
  type            TEXT,
  likes           TEXT,
  text_body       TEXT,
  text_body_html  TEXT,
  reply_to        TEXT,
  relevance       TEXT,
  gen_time        TEXT NOT NULL
    PRIMARY KEY
    UNIQUE
)
""")
        self.cur.execute("""CREATE TABLE if not exists article
(
  author   TEXT,
  url      TEXT,
  datetime TEXT,
  title    TEXT,
  domain   TEXT
)""")
        self.cur.execute("""CREATE TABLE if not exists link
(
  url      TEXT,
  response TEXT,
  parsable TEXT
)""")
        self.cur.execute("""CREATE TABLE if not exists link_relation
(
  link_from TEXT,
  link_to   TEXT,
  gen_time  TEXT
);""")


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
        "INSERT INTO article(author, url, title, datetime, domain) \
        VALUES(?, ?, ?, ?, ?)", \
        (item.get('author', ''), item.get('url', ''), item.get('title', ''), item.get('datetime', ''), item.get('domain', '') ))

        print('Article Added in Database')
        self.con.commit()

    def storeInDB_instance(self, item):
        self.cur.execute(\
        "INSERT INTO instance(url, text_body, text_body_html, links_contained, datetime, author, id, type, likes, reply_to, relevance, unixtime, gen_time) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
        (item.get('url', ''), item.get('text_body', ''), item.get('text_body_html', ''), item.get('links_contained', ''), item.get('datetime', ''),  item.get('author', ''), item.get('id', ''), item.get('type', ''), item.get('likes', ''), item.get('reply_to', ''), item.get('relevance', ''), item.get('unixtime', ''), item.get('gen_time', '') ))

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
        "INSERT INTO link_relation(link_from, link_to, gen_time) \
        VALUES(?, ?, ?)", \
        (item.get('link_from', ''), item.get('link_to', ''), item.get('gen_time', '')))

        #print('Link Added in Database')
        self.con.commit()