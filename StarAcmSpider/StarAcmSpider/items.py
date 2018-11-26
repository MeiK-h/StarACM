# -*- coding: utf-8 -*-
import scrapy


class SolutionItem(scrapy.Item):
    source = scrapy.Field()
    run_id = scrapy.Field()
    run_id_str = scrapy.Field()
    username = scrapy.Field()
    problem = scrapy.Field()
    result = scrapy.Field()
    time = scrapy.Field()
    memory = scrapy.Field()
    language = scrapy.Field()
    code_length = scrapy.Field()
    submission_time = scrapy.Field()
