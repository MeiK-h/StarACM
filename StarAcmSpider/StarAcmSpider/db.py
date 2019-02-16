import pymongo

mongo_client = pymongo.MongoClient()

mongo_db = mongo_client.StarACM


def update_last(username, source, last):
    # 更新 last
    mongo_db.User.update_one({
        'username': username,
        'source': source
    }, {'$set': {'last': last}})
