# -*- coding: utf-8 -*-
import json

import scrapy

from StarAcmSpider.db import mongo_db, update_last
from StarAcmSpider.items import StarAcmSpiderItem


class SdutSpider(scrapy.Spider):
    name = 'SDUT'
    allowed_domains = ['acm.sdut.edu.cn']

    def start_requests(self):
        userlist = mongo_db.User.find({'source': 'SDUT'})
        for user in userlist:
            username = user['username']
            last = user['last']
            yield scrapy.Request(
                url=f'https://acm.sdut.edu.cn/onlinejudge2/index.php/API/Solution?user_name={username}&runid={last}&cmp=g&order=ASC&limit=100',
                meta={'user': user}
            )

    def parse(self, response):
        user = response.meta.get('user')
        username = user['username']

        data = json.loads(response.body_as_unicode())

        for item in data:
            star_acm_item = StarAcmSpiderItem()
            star_acm_item['source'] = 'SDUT'
            star_acm_item['username'] = user['username']
            star_acm_item['run_id'] = str(item['runid'])
            star_acm_item['data'] = item
            yield star_acm_item

        last = data[-1]['runid']
        user['last'] = last

        if len(data) == 100:
            yield scrapy.Request(
                url=f'https://acm.sdut.edu.cn/onlinejudge2/index.php/API/Solution?user_name={username}&runid={last}&cmp=g&order=ASC&limit=100',
                meta={'user': user}
            )

        # 更新 last
        update_last(username, 'SDUT', user['last'])
