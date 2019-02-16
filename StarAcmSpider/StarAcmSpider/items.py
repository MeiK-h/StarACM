import scrapy


class StarAcmSpiderItem(scrapy.Item):
    username = scrapy.Field()
    source = scrapy.Field()
    run_id = scrapy.Field()
    data = scrapy.Field()
