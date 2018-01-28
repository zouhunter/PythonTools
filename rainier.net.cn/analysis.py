import requests


# 连接分析模板
class LinkAnalysis:
    def __init__(self, url):
        self.url = url

    def get_page_text(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        return response.text