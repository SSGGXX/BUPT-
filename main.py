# -*-coding:utf-8-*-
# !python3
import requests
from bs4 import BeautifulSoup as bsoup
import csv
import os
from Login_Bupt import GetHtml
import pymongo
import json
from multiprocessing.pool import Pool


def process_detail_page(path, Url):  # 处理详细的通知内容
    html = Get_html_Entiy.get_html(Url)
    html_soup = bsoup(html, 'lxml')
    filename = html_soup.select('h1.text-center')[0].get_text()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    path = path + filename + '.txt'
    file = open(path, 'w', encoding='utf-8')
    contents = html_soup.select('div.singleinfo p')
    for content in contents:
        content = content.get_text()
        file.write(content)
    file.close()


def process_Unit(Url):  # 处理不同单位的通知
    htmls = [Url]
    content = Get_html_Entiy.get_html(Url)
    pages = bsoup(content, 'lxml').select('div.pagination-info span')
    i = 1
    if pages != []:
        pages = pages[0].get_text().split('/')[1]
        while i <= int(pages):
            htmls.append(Url + 'v_title=&pageIndex=' + str(i))
            i += 1
    for html in htmls:
        process_page(html)


def process_page(Url):  # 处理列表通知
    html = Get_html_Entiy.get_html(Url)
    html_soup = bsoup(html, 'lxml')
    dirname = html_soup.select('div.breadcrumbs')[0].get_text().split()
    details = html_soup.select('ul.newslist li')
    Url = 'http://my.bupt.edu.cn/'
    path = '通知文件/' + dirname[0] + '/' + dirname[1] + '/'
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    f = open(path + '概览.csv', 'a', encoding='utf-8')
    csv_write = csv.writer(f)
    csv_write.writerow(['名称', '时间', '单位', '链接'])
    for detail in details:
        link = detail.select('a')[0].get('href')
        title = detail.select('a')[0].get_text()
        Unit = detail.select('span')[0].get_text()
        Time = detail.select('span')[1].get_text()
        content = {
            'department': dirname[1],
            'title': title,
            'link': Url + link,
            'unit': Unit,
            'time': Time
        }
        collection.insert(content)
        data = [title, Time, Unit, Url + link]
        csv_write.writerow(data)
        # process_detail_page(path, Url + link)
    f.close()


def main():
    BaseUrl = 'http://my.bupt.edu.cn/detach.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5jb250YWluZXIuY29yZS5pbXBsLlBvcnRsZXRFbnRpdHlXaW5kb3d8cGUxMTQ0fHZpZXd8bm9ybWFsfGdyb3VwaWQ9Jmdyb3VwbmFtZT0mYWN0aW9uPWJ1bGxldGluUGFnZUxpc3Q_'
    html = Get_html_Entiy.get_html(BaseUrl)
    html_Soup = bsoup(html, 'lxml')
    links = html_Soup.select('ul.listcenter.list-unstyled li a')
    Url = 'http://my.bupt.edu.cn/detach.portal'
    Links = []
    for link in links:
        Links.append(Url + link.get('href'))  # 多线程
    #     process_Unit(Url+link.get('href'))   #单线程
    pool = Pool()
    pool.map(process_Unit, Links)
    pool.close()
    pool.join()


Get_html_Entiy = GetHtml()
mongo = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = mongo.bupt_noti
collection = db.notis
if __name__ == '__main__':
    main()
