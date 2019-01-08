# -*- coding: utf-8 -*-
import json

import scrapy

from StarAcmSpider.items import StarAcmSpiderItem


class CodeforcesSpider(scrapy.Spider):
    name = 'codeforces'
    allowed_domains = ['codeforces.com']

    def start_requests(self):
        # TODO: 从数据库获得数据
        # TODO: last 的值是最后一个已得出结果的提交的 id
        userlist = [
            {
                'username': 'MeiK',
                'last': 44590452
            }
        ]
        for user in userlist:
            yield scrapy.Request(
                url=f'http://codeforces.com/api/user.status?handle={user["username"]}&from=1&count=10',
                meta={'from': 1, 'user': user}
            )

    def parse(self, response):
        data = json.loads(response.body_as_unicode())['result']

        user = response.meta.get('user')
        from_ = response.meta.get('from') + 10

        for item in data:
            # 如果已经获取到了之前的位置，则停止后续请求
            if item['id'] <= user['last']:
                return
            star_acm_item = StarAcmSpiderItem()
            star_acm_item['source'] = 'codeforces'
            star_acm_item['data'] = item
            yield star_acm_item

        if len(data) == 10:
            yield scrapy.Request(
                url=f'http://codeforces.com/api/user.status?handle={user["username"]}&from={from_}&count=10',
                meta={'from': from_, 'user': user}
            )
