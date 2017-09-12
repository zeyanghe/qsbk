import pymysql
import pprint
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


#
#
#
# def joke_list():
#     db = pymysql.connect("localhost", "root", "root", "qsbk")
#     cur = db.cursor()
#     sql = '''create table joke_list(
#     authors  varchar(16) not null,
#     personal_link varchar(16),
#     link varchar(128) not null,
#     content varchar(500),
#     comments int,
#     funny int
#     )default charset=utf8'''
#     cur.execute(sql)
#     db.commit()
#
#
# def joke_details():
#     db = pymysql.connect("localhost", "root", "root", "qsbk")
#     cur = db.cursor()
#     sql = '''create table joke_details(
#     personal_link varchar(16) not null,
#     comments_id varchar(32) ,
#     comments_content varchar(256),
#     comments_link varchar(16)
#     )default charset=utf8'''
#     cur.execute(sql)
#     db.commit()


def db(sql):
    db = pymysql.connect("localhost", "root", "root", "qsbk")
    cur = db.cursor()
    cur.execute(sql)
    db.commit()



class Download(object):


    def download_jokes(self, url,file,headers={}):
        url = Request(url, headers=headers)
        url = urlopen(url)
        files = codecs.open(file, 'wb')
        for line in url:
            files.write(line)

        files.close()


class Beautifulsoup(Download):


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
        self.dbpath = pymysql.connect("localhost", "root", "root", "qsbk", charset='utf8')
        self.file = r'C:\Users\Administrator\Desktop\糗事百科'
        self.route = r'C:\Users\Administrator\Desktop\糗事百科详情'
        self.path = r'C:\Users\Administrator\Desktop\糗事百科个人'


    def download_8hr(self):
        for x in range(1, 14):
            url = 'https://www.qiushibaike.com/8hr/page/%s' % x
            file = self.file + '\\' + md5x(url) + '.html'
            if not os.path.exists(file):
                self.download_jokes(url, file, headers=self.headers)


    def download_hot(self):
        for x in range(1, 14):
            print(x)
            url = 'https://www.qiushibaike.com/hot/page/%s' % x
            file = self.file + '\\' + md5x(url) + '.html'
            if not os.path.exists(file):
                self.download_jokes(url, file, headers=self.headers)


    def download_text(self):
        for x in range(1, 14):
            print(x)
            url = 'https://www.qiushibaike.com/text/page/%s' % x
            file = self.file + '\\' + md5x(url) + '.html'
            if not os.path.exists(file):
                self.download_jokes(url, file, headers=self.headers)


    def download_details(self):
        db = self.dbpath
        cur = db.cursor()
        sql = "select link from joke_list"
        cur.execute(sql)
        link_list = cur.fetchall()
        for link in link_list:
            url = 'https://www.qiushibaike.com%s' % link
            file = self.route + '\\' + md5x(url) + '.html'
            if not os.path.exists(file):
                self.download_jokes(url, file, headers=self.headers)


    def download_personal_page(self):
        db = self.dbpath
        cur = db.cursor()
        sql = "select comments_link from joke_details"
        cur.execute(sql)
        link_list = cur.fetchall()
        for idx, link in enumerate(link_list):
            print(link)
            url = 'https://www.qiushibaike.com%s' % link
            file = self.path + '\\' + md5x(url) + '.html'
            if not os.path.exists(file):
                self.download_jokes(url, file, headers=self.headers)




    def beautifulSoup_joke_list(self):


        def find_joketags(tag):
            return tag.has_attr('class') and 'article block untagged mb15 typs_' in  " ".join(tag['class']) and tag.name=='div'


        db = self.dbpath
        cur = db.cursor()
        list_file = os.listdir(self.file)
        for file in list_file:
            soup = BeautifulSoup(codecs.open(self.file + '\\' + file, 'r', 'utf_8'))
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
            db.commit()


    def beautifulSoup_details(self):


        def find_joketags(tag):
            return tag.has_attr('class') and 'comment-block clearfix floor-' in  " ".join(tag['class']) and tag.name=='div'


        db = self.dbpath
        cur = db.cursor()
        list_file = os.listdir(self.route)
        for idx, file in enumerate(list_file):
            soup = BeautifulSoup(codecs.open(self.route + '\\' + file, 'r', 'utf_8'))
            id = soup.find_all('div', class_='author clearfix')[0].find_all('h2')[0].text.strip()
            if id == '匿名用户':
                continue
            personal_link = soup.find_all('div', class_='author clearfix')[0].find_all('a')[0]['href']
            # print(personal_link)
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
        db.commit()


    def beautifulSoup_personal_page(self):
        pass

















if __name__ == '__main__':
    # db(sql = '''create table page
    #                 (link varchar(16),
    #                 fans int,
    #                 follow int,
    #                 scandal int,
    #                 comment int,
    #                 smiling_face int,
    #                 selected int,
    #                 marriage varchar(16),
    #                 constellation varchar(16),
    #                 occupation varchar(16),
    #                 hometown varchar(16),
    #                 age varchar(16),
    #                 id varchar(32)
    #                 )default charset=utf8''')
    b = Beautifulsoup()
    # b.download_8hr()
    # b.download_hot()
    # b.download_text()
    # b.beautifulSoup_joke_list()
    # b.download_details()
    # b.beautifulSoup_details()
    b.download_personal_page()
