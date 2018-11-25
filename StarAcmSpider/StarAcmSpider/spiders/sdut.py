# -*- coding: utf-8 -*-
import scrapy
import json
from StarAcmSpider.models import Language, Result
from datetime import datetime


class SdutSpider(scrapy.Spider):
    name = 'sdut'
    allowed_domains = ['acm.sdut.edu.cn']
    start_urls = [
        'https://acm.sdut.edu.cn/onlinejudge2/index.php/API/Solution?limit=1000&order=ASC&runid=0&cmp=g']

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        last = None

        for item in json_response:
            item['source'] = 'sdut'
            item.pop('uid')
            item.pop('cid')
            item['run_id'] = item['runid']
            item.pop('runid')
            item['username'] = item['user_name']
            item.pop('user_name')
            item['problem'] = str(item['pid'])
            item.pop('pid')
            item['result'] = conver_result(item['result'])
            item['language'] = conver_language(item['language'])
            item['submission_time'] = datetime.strptime(
                item['submission_time'], '%Y-%m-%d %H:%M:%S')

            last = item['run_id']
            yield item

        if last:
            yield scrapy.Request(url=f'https://acm.sdut.edu.cn/onlinejudge2/index.php/API/Solution?limit=1000&order=ASC&runid={last}&cmp=g')


def conver_language(sdut_language):
    language_dict = {
        "gcc": Language.C,
        "g++": Language.CPP,
        "java": Language.JAVA,
        "python2": Language.PYTHON,
        "python3": Language.PYTHON,
        "c#": Language.CSHARP,
        "ruby": Language.RUBY,
        "go": Language.GO,
        "pascal": Language.PASCAL,
        "lua": Language.LUA,
        "haskell": Language.HASKELL,
        "perl": Language.PERL,
    }
    return language_dict[sdut_language].value if language_dict.get(sdut_language) else Language.OTHER.value


def conver_result(sdut_result):
    result_dict = {
        0: Result.RUNNING,
        1: Result.AC,
        2: Result.TLE,
        3: Result.MLE,
        4: Result.WA,
        5: Result.RE,
        6: Result.OLE,
        7: Result.CE,
        8: Result.PE,
        11: Result.SE,
        12: Result.RUNNING
    }
    return result_dict[sdut_result].value if result_dict.get(sdut_result) else Result.OTHER.value
