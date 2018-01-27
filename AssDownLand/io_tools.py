import json


# 将页面信息转换为json 字符串并保存到本地文件
def save_page(page_json):
    """ 保存某页面的信息 """
    txt = json.dumps(page_json)
    with open('data/info.txt', 'a') as f:
        f.write(txt)
        f.write('\n')
