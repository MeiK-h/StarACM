from StarAcmSpider.db import mongo_db


class StarAcmSpiderPipeline(object):
    def process_item(self, item, spider):
        insert_item = {
            'username': item['username'],
            'source': item['source'],
            'run_id': item['run_id'],
        }
        insert_item.update(item['data'])
        mongo_db.Solution.update_one({
            'username': insert_item['username'],
            'source': insert_item['source'],
            'run_id': insert_item['run_id'],
        }, {'$set': insert_item}, upsert=True)
        return item
