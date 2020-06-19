# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
from scrapy.http import FormRequest
from ..items import ManhuaItem
import re





class Xphone2020Spider(scrapy.Spider):
    name = 'xphone2020'
    allowed_domains = ['xphone2020.applinzi.com']
    man = ManhuaItem()
    headers= {'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pl;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=3a95c5b465850cda8062320884aa1e02',
    'Host': 'xphone2020.applinzi.com',
    'Origin': 'http://xphone2020.applinzi.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpReque '
    }
    def start_requests(self):
         base_url = "http://xphone2020.applinzi.com/post/allajax?"
         #所有请求集合
         requests = []
         for i in range(1, 97):#97
             formdata = {'channel': '1','cate': '','fullflag': '',
             'page': str(i),'order_by': 'hot','pageSize':'9'}
             #模拟ajax发送post请求
             url = base_url + urlencode(formdata)
             request = scrapy.Request(url,callback=self.parse_book,
                                 encoding='utf-8')
             requests.append(request)
         return requests
 
 
    def parse_book(self, response):
        #可以利用json库解析返回来得数据，在此省略
        jsonBody = json.loads(response.text)
        base_url = 'http://xphone2020.applinzi.com/post/listOnload'
        for i in jsonBody['lists']:
            bookid = re.findall("\d+", i['LinkUrl'])
            my_data = {'bookid':bookid[0]}
            yield scrapy.FormRequest(url=base_url,formdata=my_data,
      callback=self.parse_book_dir)
            
    
    def parse_book_dir(self,response):
        # 每一话的地址
        jsonBody = json.loads(response.text)
        base_url = 'http://xphone2020.applinzi.com/post/readOnload'
        print('bookid:',jsonBody['lists'][0]['CartoonId'])
        for i in jsonBody['lists']:
            my_data = {'bookid':i['CartoonId'],'chapterid':i['Id']}
            #my_data = {'bookid':'822','chapterid':i['Id']}

            yield scrapy.FormRequest(url=base_url,formdata=my_data,\
                callback=self.parse_book_jpg)

    def parse_book_jpg(self,response):
        jsonBody = json.loads(response.text)
        image = []
        for i in jsonBody['message']['imgData2'].split(','):
            image.append(i[6:-2].replace('\"',''))
        self.man['name'] = jsonBody['commit_zan']['Title']# 漫画名称
        self.man['vid'] = jsonBody['message']['vid']# 漫画名称的代码
        self.man['id'] = jsonBody['message']['id']# 漫画章节代码
        self.man['chap'] = jsonBody['message']['name']#漫画第几章节
        self.man['img'] = image# 某漫画某章节所有图片的地址
        yield self.man
        
            

    
            

            

