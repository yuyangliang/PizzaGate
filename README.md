### Webpage crawling for pizzagate

This is a crawler for pizzagate related web pages. This is built upon Scrapy 1.5.

### How-to

To install Scrapy, see https://docs.scrapy.org/en/latest/intro/install.html

To set up Scrapy and get it running, see https://docs.scrapy.org/en/latest/intro/tutorial.html

Files in the project:

- items.py: specify the items to be crawled.

- pipelines.py: pipeline to the database. Sqlite used here. Change the directory accordingly in setupDBCon method ('Database/test.db' used here).

- settings.py: spider settings. Change the project name accordingly ('pizzagate_V1' used here).

- spiders/sp1.py: the main spider.

- modules: contains the supporting modules.

	- modules/alldomain.py: import all the individual domain modules here.

### Domains

Reddit

Yournewswire

Truepundit

Steemit

thelastamericanvagabond





