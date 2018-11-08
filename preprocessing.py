# -*- coding: utf-8 -*-
#www.52pojie.cn
#处理获取到的帖子内容
#过滤掉特殊字符，保留中英文字符
#利用jieba进行中文分词
from pymongo import MongoClient
import jieba
import re


def import_stopword_dict():
    stopwords = []
    with open('stopword.txt', 'r') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            stopwords.append(line[:-1])
    return stopwords

def get_dict_from_mongo():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.ichunqiu
    my_set = db.test_1029
    for x in my_set.find():
        # post_id = x['_id']
        print(x['url'])
        # if int(post_id) <= 8532:
        if x.has_key('error'):
            save_mongo(x)
            continue
        dict = filter_url(x)
        dict = remain_chinese_english(dict)
        print('remain_chinese_english:')
        print(dict['post_text_chi'])
        print(dict['post_text_eng'])
        print(dict['reply_text_chi'])
        print(dict['reply_text_eng'])
        dict = jieba_text(dict)
        print('stop_word:')
        print(dict['post_chi_final'])
        print(dict['post_eng_final'])
        print(dict['reply_chi_final'])
        print(dict['reply_eng_final'])
        save_mongo(dict)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

#过滤掉文本中的网址url
def filter_url(dict):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(pattern, dict['post_text'])
    dict['post_text_no_url'] = re.sub(pattern, ' ', dict['post_text'])
    print('all urls:')
    for url in urls:
        print(url)

    for reply_dict in dict['reply_dicts']:
        reply_dict['post_text_no_url'] = re.sub(pattern, ' ', reply_dict['post_text'])
    return dict

def remain_chinese(dict):
    #处理帖子正文，保留中文字符
    post_text = dict['post_text']
    new_post_text = ''
    for uchar in post_text:
        if is_chinese(uchar):
            new_post_text = new_post_text + uchar
    dict['chinese_post_text'] = new_post_text.encode('utf-8')
    #处理帖子回复，保留中文字符
    dict['chinese_reply_text'] = ''
    for reply_dict in dict['reply_dicts']:
        reply_text = reply_dict['post_text']
        new_reply_text = ''
        for uchar in reply_text:
            if is_chinese(uchar):
                new_reply_text = new_reply_text + uchar
        reply_dict['chinese_post_text'] = new_reply_text.encode('utf-8')
        dict['chinese_reply_text'] = dict['chinese_reply_text'] + ' ' + reply_dict['chinese_post_text']
    return dict

#保留中英文字符
def remain_chinese_english(dict):
    # 处理帖子正文，保留中英文字符，其余均替换为space
    post_text = dict['post_text_no_url']
    post_text_chi = ''
    post_text_eng = ''
    for uchar in post_text:
        if is_chinese(uchar):
            post_text_chi = post_text_chi + uchar
        elif is_english(uchar):
            post_text_eng = post_text_eng + uchar.lower()
        else:
            post_text_chi = post_text_chi + ' '
            post_text_eng = post_text_eng + ' '
    dict['post_text_chi'] = post_text_chi.encode('utf-8')
    dict['post_text_eng'] = post_text_eng.encode('utf-8')
    # 处理帖子回复，保留中英文字符，其余均替换为space
    dict['reply_text_chi'] = ''
    dict['reply_text_eng'] = ''
    for reply_dict in dict['reply_dicts']:
        reply_text = reply_dict['post_text_no_url']
        new_reply_text = ''
        reply_text_chi = ''
        reply_text_eng = ''
        for uchar in reply_text:
            if is_chinese(uchar):
                reply_text_chi = reply_text_chi + uchar
            elif is_english(uchar):
                reply_text_eng = reply_text_eng + uchar.lower()
            else:
                reply_text_chi = reply_text_chi + ' '
                reply_text_eng = reply_text_eng + ' '
        reply_dict['post_text_chi'] = reply_text_chi.encode('utf-8')
        reply_dict['post_text_eng'] = reply_text_eng.encode('utf-8')
        #五个字以下的回复直接过滤掉，不进行分词
        if len(reply_dict['post_text_chi']) > 5 :
            dict['reply_text_chi'] = dict['reply_text_chi'] + ' ' + reply_dict['post_text_chi']
        if len(reply_dict['post_text_eng']) > 5 :
            dict['reply_text_eng'] = dict['reply_text_eng'] + ' ' + reply_dict['post_text_eng']
    return dict

#判断一个unicode是否为汉字
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

#判断一个unicode是否为英文字符
def is_english(uchar):
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


#利用jiaba进行分词
def jieba_text(dict):
    post_text_chi = dict['post_text_chi']
    post_text_eng = dict['post_text_eng']
    reply_text_chi = dict['reply_text_chi']
    reply_text_eng = dict['reply_text_eng']
    seg_post_chi = jieba.cut(post_text_chi)
    seg_post_eng = jieba.cut(post_text_eng)
    seg_reply_chi = jieba.cut(reply_text_chi)
    seg_reply_eng = jieba.cut(reply_text_eng)
    dict['post_chi_final'] = stop_word(seg_post_chi).encode('utf-8')
    dict['post_eng_final'] = stop_word(seg_post_eng).encode('utf-8')
    dict['reply_chi_final'] = stop_word(seg_reply_chi).encode('utf-8')
    dict['reply_eng_final'] = stop_word(seg_reply_eng).encode('utf-8')
    return dict

#去除掉无意义的停用词
def stop_word(seg_list):
    final_text = ''
    for word in seg_list:
        if word not in stopwords:
            final_text = final_text + ' ' + word
    return final_text

def save_mongo(dict):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.ichunqiu
    my_set = db.post_fenci_1106
    try:
        my_set.insert(dict)
        print('******************insert database success!*************************')
    except:
        print('###################insert database fail!!#######################')

if __name__ == '__main__':
    stopwords = import_stopword_dict()
    get_dict_from_mongo()
