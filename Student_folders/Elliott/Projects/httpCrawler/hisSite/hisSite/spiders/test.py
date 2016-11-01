import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LxmlLinkExtractor

class AuthorSpider(scrapy.Spider):
    name = 'craig'

    start_urls = ['http://10.0.0.210:8084/']

    def parse(self, response):
        print response.css