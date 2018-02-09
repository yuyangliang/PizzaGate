# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 10:37:48 2018

@author: Yuyang
"""

import sqlite3
from urlparse import urlparse
from collections import Counter
from datetime import datetime

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute('select url from link where parsable = "0" and response = "200"')
c.execute('select min(datetime) from article')
c.execute('select url from link')
c.execute('select url from link where response = "200"')
res = c.fetchall()

#re.search(r'(\w+|\W+)(?=.(com|org))', urlparse(url).netloc).group(1).lower()

domain = []
for i in res:
    domain.append(urlparse(i[0]).netloc)
    
domain =  Counter(domain)