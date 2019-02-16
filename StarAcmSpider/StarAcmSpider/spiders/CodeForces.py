# -*- coding: utf-8 -*-
import json

import scrapy

from StarAcmSpider.db import mongo_db, update_last
from StarAcmSpider.items import StarAcmSpiderItem


class CodeforcesSpider(scrapy.Spider):
    name = 'CodeForces'
    allowed_domains = ['codeforces.com']

    def start_requests(self):
        userlist = mongo_db.User.find({'source': 'CodeForces'})
        for user in userlist:
            yield scrapy.Request(
                url=f'http://codeforces.com/api/user.status?handle={user["username"]}',
                meta={'user': user}
            )

    def parse(self, response):
        data = json.loads(response.body_as_unicode())['result']

        user = response.meta.get('user')
        for item in data:
            star_acm_item = StarAcmSpiderItem()
            star_acm_item['source'] = 'CodeForces'
            star_acm_item['username'] = user['username']
            star_acm_item['run_id'] = str(item['id'])
            star_acm_item['data'] = item
            yield star_acm_item

        # 更新 last
        update_last(user['username'], 'CodeForces', data[0]['id'])
