from django.shortcuts import render_to_response
import pymysql
import random
import json
from urllib.request import quote, unquote


db = pymysql.connect("localhost", "root", "root", "qsbk", charset='utf8')


def qsbk(request):
    cur = db.cursor()
    sql = "select * from test"
    cur.execute(sql)
    joke_list = cur.fetchall()[0: 50]
    joke_list = [list(x) for x in joke_list]
    for joke in joke_list:
        joke[1] = 'joke_detail/%s' % joke[1]
        url_user = 'http://127.0.0.1:8000/joke_user/%s' % quote(joke[0])
        joke.append(url_user)

    tup_items = [(1, "我要打十个搞笑图片"),
                 (2, "具有讽刺意义的笑话"),
                 (3, "定州方言版笑话"),
                 (4, "与美食有关的笑话"),
                 (5, "和会计有关的笑话"),
                 (6, "去饭店吃饭的笑话"),
                 (7, "笑话集锦你笑了吗")]

    list_links = [('/joke/%s' % x[0], x[1]) for x in tup_items]

    return render_to_response('qsbk.html', {'joke_list': joke_list,
                                            'joke_lists': list_links,
                                            })



def get_joke_list(requests, number):
    cur = db.cursor()
    sql = "select * from test"
    cur.execute(sql)
    num = int(number)
    joke_list = [list(x) for x in cur.fetchall()[num*50:(1+num)*50]]

    for joke in joke_list:
        joke[1] = 'http://127.0.0.1:8000/joke_detail/%s'%joke[1]

    title = '糗事百科'
    tup_items = [(1, "我要打十个搞笑图片"),
                 (2, "具有讽刺意义的笑话"),
                 (3, "定州方言版笑话"),
                 (4, "与美食有关的笑话"),
                 (5, "和会计有关的笑话"),
                 (6, "去饭店吃饭的笑话"),
                 (7, "笑话集锦你笑了吗")]

    list_links = [('/joke/%s'%x[0], x[1]) for x in tup_items]

    return render_to_response('qsbk_funny.html', {'title': title,
                                                  'joke_lists': list_links,
                                                  'joke_list': joke_list,
                                                  })


def joke_details(request,website):
    cur = db.cursor()
    sql = "select * from test where link like '%s'" % website
    cur.execute(sql)
    joke_list = cur.fetchone()
    sqls = "select link from test"
    cur.execute(sqls)
    link_list = cur.fetchall()
    link = random.choice(link_list)
    total_link = link
    sql_list = "select * from joke_comment where joke_link like '%s'" % website
    cur.execute(sql_list)
    joke_comment_list = cur.fetchall()
    tup_items = [(1, "我要打十个搞笑图片"),
                 (2, "具有讽刺意义的笑话"),
                 (3, "定州方言版笑话"),
                 (4, "与美食有关的笑话"),
                 (5, "和会计有关的笑话"),
                 (6, "去饭店吃饭的笑话"),
                 (7, "笑话集锦你笑了吗")]

    list_links = [('/joke/%s' % x[0], x[1]) for x in tup_items]

    return render_to_response('joke_details.html', {'total_link': total_link,
                                                    'joke_list': joke_list,
                                                    'joke_comment_list': joke_comment_list,
                                                    'list_links':list_links})



