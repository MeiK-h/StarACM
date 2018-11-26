from StarAcmSpider.models import Last


def session_commit(session):
    session.commit()


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
