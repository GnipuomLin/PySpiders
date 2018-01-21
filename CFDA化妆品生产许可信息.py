#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
'''
化妆品生产许可信息管理系统 小爬虫
'''
class Cfda:

    #初始化函数
    def __init__(self):
        #初始化，要提交数据的网址
        self.url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
        #反爬虫
        self.HEADERS = {
            'Host': '125.35.6.84:81',
            'Referer': 'http://125.35.6.84:81/xk/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        #文件路径及名称
        self.file = open(r'D:\\PycharmProjects\\Spiders\cfda化妆品生产许可信息.txt', 'a')

    #获取post请求的信息
    def get_data(self,data):
        self.html = requests.post(self.url, data=data, headers=self.HEADERS, timeout=10)
        return self.html

    #获取json中字段信息
    def extract_data(self):
        for i in range(len(self.html.json()['list'])):
            self.EPS_NAME = self.html.json()['list'][i]['EPS_NAME']  # 企业名称
            self.PRODUCT_SN = self.html.json()['list'][i]['PRODUCT_SN']  # 许可证编号
            self.QF_MANAGER_NAME = self.html.json()['list'][i]['QF_MANAGER_NAME']  # 发证机关
            self.XK_DATE = self.html.json()['list'][i]['XK_DATE']  # 有效期至
            self.XC_DATE = self.html.json()['list'][i]['XC_DATE']  # 发证日期
            self.data = '\n企业名称:'+ self.EPS_NAME+'\t许可证编号:'+ self.PRODUCT_SN+'\t\t发证机关:'+ self.QF_MANAGER_NAME+'\t有效期至:'+ self.XK_DATE+'\t发证日期:'+self.XC_DATE + '\n' + '-'*165
            print(self.data)
            self.file.write(self.data)

    #关闭文件
    def fileclose(self):
        self.file.close()

if __name__ == '__main__':
    cfda = Cfda()
    #第1/286页，15条/页，总共【4277】条数据
    for i in range(1,10): # 测试前九页数据
        form_data = {
            'on':'true',
            'page':'{}'.format(i),
            'pageSize':'15',
            'productName':'',
            'conditionType':'1',
            'applyname':'',
            'applysn':''
        }
        cfda.get_data(form_data)
        cfda.extract_data()
    cfda.fileclose()
    print('化妆品生产许可信息管理系统，勤劳的小爬虫完成了工作')

