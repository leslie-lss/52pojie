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

# line = "影音娱乐" + '\t' + "www.top100.cn" + '\t' + "nc.001pot.www" + '\t' + "巨鲸网"
# line = "母婴儿童" + '\t' + "www.babyhome.com.tw" + '\t' + "wt.moc.emohybab.www" + '\t' + "宝贝家庭亲子网"
# line = "财经证券" + '\t' + "www.ghzq.com.cn" + '\t' + "nc.moc.qzhg.www" + '\t' + "null"
# r.rpush('url_group', line)

# while True:
#     line = fo.readline()
#     if line:
#         r.rpush('url', line)
#     else:
#         break

# lines = fo.readlines()
#
# for line in lines:
#     r.rpush('url', line)

# url_list = []
# for line in lines:
#     url = line.split(',')[0]
#     url = url.replace(url[0], "")
#     url_list.append("http://" + url)
#
# for url in url_list:
#     r.rpush('url',url)

print("success0")