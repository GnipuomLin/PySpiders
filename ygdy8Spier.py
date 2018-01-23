#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import pymysql

# 连接数据库
connect = pymysql.Connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'root',
    db = 'movie_demo',
    charset = 'utf8'
)
# 获取游标
cursor = connect.cursor()

#反爬虫
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

#获取电影列表
def get_movie_list(url):
    response = requests.get(url,headers=HEADERS,timeout=10)    #获取网页源码
    response.encoding = 'gb2312'    #设置网页编码
    reg = r'<a href="(.*?)" class="ulink">(.*?)</a>'   #使用正则表达式获取内页电影链接URL和电影标题
    return re.findall(reg, response.text)

#获取电影内页的电影信息及下载链接
def get_movie_content(url):
    response = requests.get(url,headers=HEADERS,timeout=10)    #获取网页源码
    response.encoding = 'gb2312'    #设置网页编码
    reg = '<!--Content Start-->(.*?)<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.*?)">'  #使用正则表达式获取内页电影信息及下载链接
    return re.findall(reg, response.text,re.S)

if __name__ == '__main__':
    # 共169页/4208条记录
    urls = ['http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'.format(i) for i in range(1,31)] #多页
    for url in urls:
        print('电影页url: ' + url)
        movie_lists = get_movie_list(url)    #遍历网页中的电影内页链接URL
        for movie_url, title in movie_lists:
            movie_url = 'http://www.ygdy8.net' + movie_url    #链接拼接
            movie_content = get_movie_content(movie_url)
            print('正在存储-----{}'.format(title))
            for content,link in movie_content:
                # print(content)
                # print(link)
                cursor.execute("insert into movie(title, content, link) values('{}','{}','{}')".format(title,content.replace("'",r"\'"),link))
                connect.commit()
        #     break
        # break
    # 关闭连接
    cursor.close()
    connect.close()