# -*- coding: utf-8 -*-
#www.52pojie.cn
#获取帖子列表
import sys
import urllib
import requests
import random
import time
from lxml import etree
from pymongo import MongoClient

my_headers = [    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                  'Opera/9.25 (Windows NT 5.1; U; en)',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                  'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                  'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                  "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                  "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36']
headers = {
    'user-agent': random.choice(my_headers),
    'Connection': 'keep-alive',
    'host': 'www.52pojie.cn',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Enocding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_id(page):
    url = 'https://www.52pojie.cn/forum.php?mod=forumdisplay&fid=5&orderby=lastpost&orderby=lastpost&filter=lastpost&page={0}'.format(page)
    dict_list = []
    try:
        page_source = requests.get(url, headers=headers).content
    except:
        time.sleep(60)
        try:
            print("@@@@@@@@@@@@@@@@@@@@@@@@sleep@@@@@@@@@@@@@@@@@@@@@@@@@")
            page_source = requests.get(url, headers=headers).content
        except:
            sys.exit(0)
    html = etree.HTML(page_source)
    content_list = html.xpath("//*[starts-with(@id,'normalthread_')]")
    for content in content_list:
        post_id = content.xpath("@id")[0].replace('normalthread_', '')
        post_url = 'https://www.52pojie.cn/thread-{0}-1-1.html'.format(post_id)
        dict = {'_id': post_id,
                'post_url': post_url
                }
        print(dict)
        dict_list.append(dict)
    return dict_list

def save_mongo(dict_list):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.wuaipojie
    my_set = db.tkpj_list_1105_0950
    try:
        my_set.insert_many(dict_list)
        print('******************insert database success!*************************')
    except:
        for dict in dict_list:
            try:
                my_set.insert(dict)
            except:
                print('###################insert database fail!!#######################')
        print('******************insert database success!*************************')
if __name__ == '__main__':
    page = 1
    while page <= 100:
        print(page)
        dict_list = get_id(page)
        save_mongo(dict_list)
        page = page + 1