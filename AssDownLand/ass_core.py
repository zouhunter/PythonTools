# -*- coding: utf-8 -*-
import requests
import json
import os
import re

# ass 的官方网站

root_url = 'https://www.meitulu.com'
ass_url = 'https://www.meitulu.com/t/aiss/'
tag_reg1 = r'<ul id="tag_ul">(.*?)</ul>'
tag_reg2 = r'<li><a href="(.*?)">(.*?)</a></li>'
tag_group_reg1 = r'<div id="pages" class="text-c">(.*?)</div>'
tag_group_reg2 = r'<a href=".*?">(\d+)</a>'
page_group_reg1 = r'<ul class="img">(.*?)</ul>'
page_group_reg2 = r'<p class="p_title"><a href="(.*?)" target="_blank">(.*?)</a></p>'
image_group_reg1 = r'<div id="pages">(.*?)</div>'
image_group_reg2 = r'<a href=".*?">(\d+)</a>'
image_item_reg1 = r'<div class="content">\n<center>(.*?)</center>'
image_item_reg2 = r'img src="(.*?)" alt="(.*?)"'


# 连接分析模板
class LinkAnalysis:
    def __init__(self, url):
        self.url = url

    def get_page_text(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        return response.text


# 解析类型 (返回 url 和 类型名)
class TagAnalysis(LinkAnalysis):
    # 导航栏中的标签连接列表（返回url 和 类型 的组元）
    def get_tag_links(self):
        result = self.get_page_text()
        list_tag = re.findall(tag_reg1, result, re.S)
        list_link_tags = re.findall(tag_reg2, list_tag[0])
        return list_link_tags


# 解析类型中所有的界面 （返回url）
class GroupPageAnalysis(LinkAnalysis):
    # 返回所有一组中所有列表
    def get_group_links(self):
        pass

    # 获取tag 下所有页面
    def get_tag_pages(self):
        pages = []
        set(pages)
        pages.append(self.url)
        result = self.get_page_text()
        down_info = re.findall(tag_group_reg1, result, re.S)
        if len(down_info) > 0:
            links = re.findall(tag_group_reg2, down_info[0], re.S)
            len_links = len(links)
            if len_links > 0:
                max_num = int(links[len_links-1])
                for index in range(2, max_num + 1):
                    page_url = "{0}/{1}.html".format(self.url, index)
                    pages.append(page_url)
                    # print(page_url)
        pass
        return pages


# 解析一个组页面所有的连接 (返回 url,页面连接)
class PageLinksAnalysis(LinkAnalysis):

    # 获取一组中某一页的所有列表
    def get_page_links(self):
        result = self.get_page_text()
        item_content = re.findall(page_group_reg1, result, re.S)[0]
        return re.findall(page_group_reg2, item_content)


# 解析图片组页面所有的页连接（返回url）
class PicturePageAnalysis(LinkAnalysis):

    def get_picture_pages(self):
        pages = []
        set(pages)
        pages.append(self.url)
        result = self.get_page_text()
        down_info = re.findall(image_group_reg1, result, re.S)

        if len(down_info) > 0:
            links = re.findall(image_group_reg2, down_info[0], re.S)
            len_links = len(links)
            if len_links > 0:
                num_reg = r'.*?/(\d+).html'
                num = re.findall(num_reg, self.url)[0]
                max_num = int(links[len_links - 1])
                for index in range(2, max_num + 1):
                    # 下一页的结构为在后面加"_id"
                    page_url = str.replace(self.url, num, "{0}_{1}".format(num, index))
                    pages.append(page_url)
        pass
        return pages


# 解析一页内所有图片路径 （返回url 和 文件名）
class PictureAnalysis(LinkAnalysis):
    def get_pictures_info(self):
        result = self.get_page_text()
        picture_content = re.findall(image_item_reg1, result)[0]
        picture_list = re.findall(image_item_reg2, picture_content)
        return picture_list


# 获取整站的图片路径及保存路径 (图片url、目录名、要存储的名字)
def get_info_imgs():
    res = []
    tga = TagAnalysis(ass_url)
    tag_links = tga.get_tag_links()
    for tag_link, tag_name in tag_links:
        group = GroupPageAnalysis(tag_link)
        group_pages = group.get_tag_pages()
        for page in group_pages:
            page_link_holder = PageLinksAnalysis(page)
            page_links = page_link_holder.get_page_links()
            for page_link, page_name in page_links:
                picture_group_holder = PicturePageAnalysis(page_link)
                picture_pages = picture_group_holder.get_picture_pages()
                for picture_page in picture_pages:
                    pictures_holder = PictureAnalysis(picture_page)
                    pictures_info = pictures_holder.get_pictures_info()
                    for picture_url, picture_name in pictures_info:
                        directory = os.path.join("data", tag_name, page_name)
                        filepath = os.path.join(directory, "%s.jpg" % picture_name)
                        # 每张图片一组，包含 图片url，所在目录，存储路径
                        res.append((
                            picture_url, directory, filepath
                        ))
                        # break
                    # break
                break
            break
        break
    return res


if __name__ == "__main__":
    imgs = get_info_imgs()
    for url, directory, file_path in imgs:
        print(url)
        print(directory)
        print(file_path)


