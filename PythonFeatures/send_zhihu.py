'''
实现模拟发送知乎私信
'''
# -*- coding:utf-8 -*-

import requests
import time
import json

# 响应头里面
url_temp = "https://www.zhihu.com/api/v4/messages"


# 发送类
class SendData:

    def __init__(self, url):
        self.url = url
        self.headers = {}
        self.cookies = {}
        pass

    def send(self, dat):
        print(dat)
        f = open(r'test.txt', 'r')  # 打开所保存的cookies内容文件
        cookies = {}  # 初始化cookies字典变量
        for line in f.read().split('\n'):  # 按照字符：进行划分读取
            # 其设置为1就会把字符串拆分成2份
            name, value = line.strip().split('=', 1)
            cookies[name] = value  # 为字典cookies添加内容

        self.headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
        }
# data=json.dumps(dat)
        response = requests.post(self.url, json=dat, headers=self.headers, cookies=cookies)
        print(response.text)
        print(response.status_code)
        pass


data = {
    'type': 'common',
    'content': 'test',
    'receiver_hash': 'eee5ba1b647b8d3b1ada81b99eb28e67'
}# 我的：eee5ba1b647b8d3b1ada81b99eb28e67
# 别人的：8dc19341ccccd510a2487c9beac0e187

sender = SendData(url_temp)
sender.send(data)
