#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

if __name__ == '__main__':
    timestamp = 1516697159  #时间戳
    while type(timestamp) == int or type(timestamp) == float:
        url = 'http://www.neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time={}'.format(timestamp)
        html = requests.get(url, headers=HEADERS,timeout=10)
        for i in range(20):
            content = html.json()['data']['data'][i]['group']['content']
            print(content)
            with open('Neihanshequ.txt','a',encoding='gb18030') as f:
                f.write(content + '\n'*2)
            # f.close()
        timestamp = html.json()['data']['max_time']