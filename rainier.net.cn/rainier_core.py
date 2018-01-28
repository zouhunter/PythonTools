import analysis
import time
import re

from bs4 import BeautifulSoup

temp_url = 'http://www.rainier.net.cn'


# 获取类别
class MainPage(analysis.LinkAnalysis):
    def get_all_page_links(self):
        pages = set()
        html = BeautifulSoup(self.get_page_text(), 'html.parser')
        root = html.find_all('ul')[1]
        lists = root.find_all(lambda tag: tag.name == 'a' and 'href'in tag.attrs)
        for item in lists:
            url = temp_url + item['href']
            type_name = item.get_text()
            pages.add((url, type_name))
        return pages


class MovieGroupPage(analysis.LinkAnalysis):
    def get_movie_page_links(self):
        pages = set()
        html = BeautifulSoup(self.get_page_text(), 'html.parser')
        list = html.find_all('div', {'class': 'video-element'})
        for item in list:
            url =temp_url + item.a['href']
            type_name = item.find(lambda tag:tag.name == 'img' and 'alt' in tag.attrs)['alt']
            pages.add((url, type_name))
        return pages


class MoviePage(analysis.LinkAnalysis):
    def get_movie_link(self):
        html = BeautifulSoup(self.get_page_text(), 'html.parser')
        link = html.find('param', {'name': 'flashvars'})['value']
        reg = r'file=(.*?)&.*?'
        link = temp_url + re.findall(reg, link)[0]
        return link


# 获取视屏的地址和保存信息
def get_all_movie_infos(on_get):
    mp = MainPage('http://www.rainier.net.cn/cpys/glxtl/dxyqgxl/')
    pages = mp.get_all_page_links()
    for page_url, page_name in pages:
        mg = MovieGroupPage(page_url)
        video_pages = mg.get_movie_page_links()
        for movie_page_url, movie_page_name in video_pages:
            movie_page = MoviePage(movie_page_url)
            movie_url = movie_page.get_movie_link()
            directory = 'data/' + page_name
            file_name = directory + '/{0}.flv'.format(movie_page_name)
            img = (movie_url, directory, file_name)
            on_get(img)
            time.sleep(1)


if __name__ == '__main__':
    get_all_movie_infos(lambda x: print(x))
