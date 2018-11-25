# -*- coding: utf-8 -*-
from StarAcmSpider.models import get_session, Solution, Last


class StaracmspiderPipeline(object):
    def __init__(self):
        self.session = get_session()

    def process_item(self, item, spider):
        solution = Solution(**item)
        try:
            self.session.add(solution)
            self.session.commit()
        except:
            self.session.rollback()
        return item


def update_last(session, source, last, **kw):
    if source == 'sdut':
        sdut_last = session.query(Last).filter_by(source='sdut').all()
        if sdut_last:
            sdut_last = sdut_last[0]
            sdut_last.last = last
        else:
            sdut_last = Last(source='sdut', last=last, extra='')
        session.merge(sdut_last)
        session.commit()
