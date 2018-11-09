# -*- coding:utf-8 -*-

import redis
from pymongo import MongoClient

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def get_id_from_mongo():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.wuaipojie
    my_set = db.ydaq_list_1105_0941
    exist_set = db.ydaq_post_1105_1440
    for x in my_set.find():
        post_id = x['_id']
        print(x['post_url'])
        if exist_set.find({'_id': post_id}).count() == 0 :
            r.rpush('post_id', post_id)
        else:
            print("******************************")
        # r.rpush('tkpj_id', post_id)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

if __name__ == '__main__':
    get_id_from_mongo()

print("success0")
