# -*- coding: utf-8 -*-
import json
from datetime import datetime

import scrapy

from StarAcmSpider.items import SolutionItem
from StarAcmSpider.models import Language, Last, Result, get_session
from StarAcmSpider.db import update_last, session_commit


class SdutSpider(scrapy.Spider):
    name = 'sdut'
    allowed_domains = ['acm.sdut.edu.cn']

    def start_requests(self):
        self.session = get_session()
        last = self.session.query(Last).filter_by(source='sdut').all()
        if last:
            self.last = last[0].last
        else:
            self.last = 0
        self.logger.info(f'Spider crawl start on {self.last}')
        yield scrapy.Request(
            f'https://acm.sdut.edu.cn/onlinejudge2/index.php/API/Solution?limit=1000&order=ASC&runid={self.last}&cmp=g')

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        this_last = None

        for item in json_response:
            item['source'] = 'sdut'
            item.pop('uid')
            item.pop('cid')
            item['run_id'] = item['runid']
            item['run_id_str'] = str(item['runid'])
            item.pop('runid')
            item['username'] = item['user_name']
            item.pop('user_name')
            item['problem'] = str(item['pid'])
            item.pop('pid')
            item['result'] = conver_result(item['result'])
            item['language'] = conver_language(item['language'])
            item['submission_time'] = datetime.strptime(
                item['submission_time'], '%Y-%m-%d %H:%M:%S')

            solution = SolutionItem(**item)

            this_last = item['run_id']
            self.last = this_last
            yield solution

        if this_last:
            yield scrapy.Request(url=f'https://acm.sdut.edu.cn/onlinejudge2/index.php/API/Solution?limit=1000&order=ASC&runid={this_last}&cmp=g')

    def closed(self, reason):
        self.logger.info(f'save last {self.last} to database')
        update_last(self.session, 'sdut', self.last)
        session_commit(self.session)


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
