import json
import requests
from bs4 import BeautifulSoup
import re,sys
from fake_useragent import UserAgent
import importlib
import os
importlib.reload(sys)
f = open('xiaoqu_data.txt', 'w+')
ua = UserAgent()
for i in range(1,41):
    # 循环构造url
    url = 'http://sz.lianjia.com/xiaoqu/futianqu/pg{}/'
    k = url.format(i)
    # 添加请求头，否则会被拒绝

    headers = {'Referer': 'https://sz.lianjia.com/xiaoqu/futianqu/',
        'user-agent':ua.random}
    # print(headers)
    res = requests.get(k, headers=headers)
    # print(res)
    # 基于正则表达式来解析网页内容，拿到所有的详情url
    # 原始可能是这么做的，但是后来发现bs4给我们提供了更方便的方法来取得各元素的内容
    # 正则表达式最重要的两个东西，.任意匹配字符，*匹配任意次数，？以html结束
    text = res.text
    # print(text)
    re_set = re.compile('https://sz.lianjia.com/xiaoqu/[0-9]+')
    re_get = re.findall(re_set,text)
    # print(re_get)

    #去重
    lst2 = {}.fromkeys(re_get).keys()
    # print(lst2)

    for name in lst2:
        headers = {'Referer': 'https://sz.lianjia.com/xiaoqu/',
        'user-agent':ua.random}
        res = requests.get(name, headers=headers)
        info = {}
        text2 = res.text
        
        soup = BeautifulSoup(text2, 'html.parser')
        data_hushu = soup.select(".xiaoquInfoContent")[6].text
        title = soup.select(".detailTitle")[0].text
        xiaoqu = soup.select(".actshowMap")
        print_str = title
        # print(title)
        # print(data_hushu)
        print_str = print_str + " " + data_hushu
        for a in xiaoqu:
            xq = a['xiaoqu']
            xq = xq.replace("[", " ")
            xq = xq.replace(",", " ")
            xq = xq.replace("]", "")
            print_str = print_str + xq
        #     print(xq)
        # print(print_str)
        f.write(print_str + os.linesep)