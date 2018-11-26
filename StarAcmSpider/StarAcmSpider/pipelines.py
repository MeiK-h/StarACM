# -*- coding: utf-8 -*-
from StarAcmSpider.db import session_commit
from StarAcmSpider.models import Last, Solution, get_session
from StarAcmSpider.settings import SQL_COMMIT_COUNT


class StaracmspiderPipeline(object):

    def open_spider(self, spider):
        self.count_dict = getattr(self, 'count_dict', {})
        self.count_dict[spider.name] = 0

    def process_item(self, item, spider):
        solution = Solution(**item)
        try:
            spider.session.add(solution)
            if self.count_dict[spider.name] % SQL_COMMIT_COUNT == 0:
                session_commit(spider.session)
            self.count_dict[spider.name] += 1
        except:
            spider.session.rollback()
        return item
