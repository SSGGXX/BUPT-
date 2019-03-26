# -*-coding=utf-8-*-
# ! python3
import requests
import http.cookiejar
from bs4 import BeautifulSoup as bs


class GetHtml():

    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
        }

        # setting cookie
        self.s = requests.Session()
        self.s.cookies = http.cookiejar.CookieJar()
        r = self.s.get('https://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Findex.portal',
                       headers=self.header)
        dic = self.getLt(r.text)
        postdata = {
            'username': '',  # 此处为你的学号
            'password': '',  # 你的密码
            'lt': dic['lt'],
            'execution': 'e1s1',
            '_eventId': 'submit',
            'rmShown': '1'
        }
        self.s.post(
            'https://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Findex.portal',
            data=postdata, headers=self.header)

    def getLt(self, str):
        lt = bs(str, 'html.parser')
        dic = {}
        for inp in lt.form.find_all('input'):
            if (inp.get('name')) != None:
                dic[inp.get('name')] = inp.get('value')
        return dic

    def get_html(self, Url):
        response2 = self.s.get(Url, headers=self.header)  # ('http://my.bupt.edu.cn/index.portal',headers=header)
        response2.encoding = 'utf-8'
        return response2.text
