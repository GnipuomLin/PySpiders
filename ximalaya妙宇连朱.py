#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import os
import json
from urllib.request import urlretrieve  #下载库

#反爬虫
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

#获取网页源码
def get_html(url):
    response = requests.get(url,headers=HEADERS)
    return response

#获取专辑里的声音id
def get_sound_id(html):
    reg = re.compile('<a class="title" href="/1615410/sound/(.*?)/" hashlink')
    return re.findall(reg,html.text)

#喜马拉雅 小爬虫开始工作咯
if __name__ == '__main__':
    start_urls = ['http://www.ximalaya.com/1615410/album/270535?page={}'.format(i) for i in range(1,2)]
    print('-' * 20 + ' 喜马拉雅 妙宇连朱 小爬虫开始工作咯')
    path = r'妙宇连朱/'
    if not os.path.exists(path):
        os.makedirs(path)
        print(path + ' 文件夹创建成功')
    for url in start_urls:
        html = get_html(url)
        sound_ids = get_sound_id(html)
        for sound_id in set(sound_ids):
            #获取播放JSON文件
            urls = 'http://www.ximalaya.com/tracks/{}.json'.format(sound_id)
            sound_html = get_html(urls)
            # print(sound_html.json())
            m4a = sound_html.json()['play_path_64']
            title = sound_html.json()['title']
            file_name = path + '{}.m4a'.format(title)
            # print(file_name, m4a)
            try:
                urlretrieve(m4a,file_name)  #开始下载m4a音频文件
                print( '下载成功 >>>>>> ' + title)
            except Exception as e:
                print(e)
                continue
    print('-' * 20 + '喜马拉雅 妙宇连朱 勤劳的小爬虫工作结束了')