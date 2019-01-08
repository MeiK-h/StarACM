import scrapy


class StarAcmSpiderItem(scrapy.Item):
    source = scrapy.Field()
    data = scrapy.Field()
