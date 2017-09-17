import pymysql
import hashlib
from bs4 import BeautifulSoup
import codecs
from urllib.request import urlopen, Request
import os
import re
import time
import uuid
import json
import random

def md5x(strsrc):
    return hashlib.md5(strsrc.encode('utf-8')).hexdigest()


class Data_base(object):


    def __init__(self):
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Host': 'www.qiushibaike.com',
                        'Pragma': 'no-cache',
                        'Referer': 'https://www.qiushibaike.com/joke/1434416/',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.163.400 QQBrowser/9.3.7080.400'}
        self.db_connect = pymysql.connect("localhost", "root", "root", "qsbk", charset='utf8')
        self.path_joke_list = r'C:\Users\Administrator\Desktop\糗事百科'
        self.path_joke_details = r'C:\Users\Administrator\Desktop\糗事百科详情'
        self.path_joke_personal = r'C:\Users\Administrator\Desktop\糗事百科个人'

    def create_table(self, sql):
        cur = self.db_connect.cursor()
        cur.execute(sql)
        self.db_connect.commit()

    def query(self, sql):
        cur = self.db_connect.cursor()
        cur.execute(sql)
        link_list = cur.fetchall()
        return link_list


class Download(Data_base):


    def download_jokes(self, url,file,headers={}):
        url = Request(url, headers=headers)
        url = urlopen(url)
        files = codecs.open(file, 'wb')
        for line in url:
            files.write(line)

        files.close()

    def download_joke_list(self, domain):
        for x in range(1, 14):
            url = 'https://www.qiushibaike.com%s%s' % (domain, x)
            file = self.path_joke_list + '\\' + md5x(url) + '.html'
            if not os.path.exists(file):
                self.download_jokes(url, file, headers=self.headers)

    def download_details(self):
        link_list = self.query("select comments_link from joke_details")
        for link in link_list:
            url = 'https://www.qiushibaike.com%s' % link
            file = self.path_joke_details + '\\' + md5x(url) + '.html'
            if not os.path.exists(file):
                self.download_jokes(url, file, headers=self.headers)


class Beautifulsoup(Download):


    def beautifulSoup_joke_list(self):

        def find_joketags(tag):
            return tag.has_attr('class') and 'article block untagged mb15 typs_' in  " ".join(tag['class']) and tag.name=='div'

        cur = self.db_connect.cursor()
        list_file = os.listdir(self.path_joke_list)
        for file in list_file:
            soup = BeautifulSoup(codecs.open(self.path_joke_list + '\\' + file, 'r', 'utf_8'))
            body = soup.body
            joke_list = body.find_all('div', {'id':'content'}, recursive=False)[0]\
                .find_all('div', class_='content-block clearfix', recursive=False)[0]\
                .find_all('div', class_='col1', recursive=False)[0]\
                .find_all(find_joketags, recursive=False)
            for joke in joke_list:
                id = joke.find_all('h2')[0].text.strip()
                if id == '匿名用户':
                    continue
                personal_link = joke.find_all('div', class_='author clearfix')[0].find_all('a')[0]['href']
                link = joke.find_all('a', class_='contentHerf')[0]['href']
                content = joke.find_all('span')[0].text.strip()
                funny = joke.find_all('span', class_='stats-vote')[0].find_all('i', class_='number')[0].text.strip()
                comments = joke.find_all('span', class_='stats-comments')[0]\
                    .find_all('i', class_='number')[0].text.strip()
                sql = '''insert into joke_list values ('%s', '%s', '%s', '%s', '%s', '%s')''' % (id, personal_link,
                                                                                                 link, content,
                                                                                                 comments,funny)
                print(sql)

                cur.execute(sql)
        self.db_connect.commit()

    def beautifulSoup_details(self):

        def find_joketags(tag):
            return tag.has_attr('class') and 'comment-block clearfix floor-' in " ".join(tag['class']) and tag.name=='div'

        cur = self.db_connect.cursor()
        list_file = os.listdir(self.path_joke_details)
        for idx, file in enumerate(list_file):
            soup = BeautifulSoup(codecs.open(self.path_joke_details + '\\' + file, 'r', 'utf_8'))
            id = soup.find_all('div', class_='author clearfix')[0].find_all('h2')[0].text.strip()
            if id == '匿名用户':
                continue
            personal_link = soup.find_all('div', class_='author clearfix')[0].find_all('a')[0]['href']
            comments_list = soup.find_all(find_joketags)
            for idx, comments in enumerate(comments_list):
                comments_id = comments.find_all('div', class_='replay')[0].find_all('a')[0].next.strip()
                comments_content = comments.find_all('span', class_='body')[0].string
                comments_link = comments.find_all('a')[0]['href']
                sql = '''insert into joke_details values ('%s', '%s', '%s', '%s')''' % (
                    personal_link,
                    comments_id.replace("\\", ' ').replace("'", ' ').replace('"', ' '),
                    comments_content.replace("\\", ' ').replace("'", ' ').replace('"', ' '),
                    comments_link)
                print(sql)
                cur.execute(sql)
        self.db_connect.commit()

    def beautifulSoup_personal_page(self):
        cur = self.db_connect.cursor()
        # list_file = os.listdir(self.path_joke_personal)
        # for file in list_file[:1]:
        file = '00aaa1790c71837436ebbed5cf353b0e.html'
        soup = BeautifulSoup(codecs.open(self.path_joke_personal + '\\' + file, 'r', 'utf_8'))
        user_statis = soup.find_all('div', class_='user-statis user-block')


        print()


















if __name__ == '__main__':
    b = Beautifulsoup()
    b.beautifulSoup_personal_page()