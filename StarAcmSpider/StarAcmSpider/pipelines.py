# -*- coding: utf-8 -*-
from StarAcmSpider.models import get_session, Solution


class StaracmspiderPipeline(object):
    def __init__(self):
        self.session = get_session()

    def process_item(self, item, spider):
        solution = Solution(**item)
        try:
            self.session.add(solution)
        except:
            self.session.rollback()
        finally:
            self.session.commit()
        return item
