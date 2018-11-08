# 概述

爬取吾爱破解论坛脱壳破解区和移动安全区的所有帖子内容，进行分词预处理，并且存入mongodb中

# 网址分析

吾爱破解：https://www.52pojie.cn/

>移动安全区：https://www.52pojie.cn/forum-65-1.html    31页 每页50篇帖子  约1500篇帖子

>脱壳破解区：https://www.52pojie.cn/forum-5-1.html    100页 每页50篇帖子  约5000篇帖子

移动安全区：按照最新来进行排序：

https://www.52pojie.cn/forum.php?mod=forumdisplay&fid=65&orderby=lastpost&orderby=lastpost&filter=lastpost&page=1

帖子地址：

https://www.52pojie.cn/thread-742703-1-1.html

thread-a-b-c：

>a代表帖子的ID号，唯一；

>b代表帖子的第几页；

>c恒为1.

# 网页元素分析

## 版块列表页面：

只需获得帖子的ID号即可；

发现每个帖子的部分都是在id='normalthread_{id}'的标签中；

## 帖子页面：

利用xpath来定位所需的页面元素

# 数据存树结构

key | 意义
-------- | --------
_id	| 帖子的ID号，唯一，且可以凭借ID确定帖子的url
url	| 帖子的地址
error	| （大多没有）获取不到帖子内容时，一般是没有查看帖子权限时，显示为"can't crawl!!"
page_total	| 帖子页数
forum_type	| 帖子类型
title	| 帖子标题
post_time	| 发帖时间
post_text	| 帖子正文
reply_dicts	| 列表，列表元素为字典。包含所有的回复信息，每一条回复以字典的形式存储，每个字典中存储回复时间、回复内容、以及过滤掉url的内容和保留中英文文本之后的内容
post_text_no_url	| 过滤掉网址url的帖子文本
post_text_chi	| 主题帖正文中的中文字符
post_chi_final	 | 主题帖正文中的中文字符的分词结果
post_text_eng	| 主题帖正文中的英文字符
post_eng_final	 | 主题帖正文中的英文字符的分词结果
reply_text_chi	| 所有回帖正文中的中文字符
reply_chi_final | 所有回帖正文中的中文字符的分词结果
reply_text_eng	| 所有回帖正文中的英文字符
reply_eng_final | 所有回帖正文中的英文字符的分词结果
