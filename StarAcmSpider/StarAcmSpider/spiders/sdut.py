# -*- coding: utf-8 -*-
import scrapy


class SdutSpider(scrapy.Spider):
    name = 'sdut'
    allowed_domains = ['acm.sdut.edu.cn']
    start_urls = ['http://acm.sdut.edu.cn/']

    def parse(self, response):
        pass
