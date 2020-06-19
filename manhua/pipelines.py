# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html



from scrapy.pipelines.images import ImagesPipeline
import os
from urllib import request
class ManhuaPipeline:

    def __init__(self):
        # 查看当前目录，join是拼接构建的是绝对路径
        self.img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'漫画')
        if not os.path.exists(self.img_path):
            # 如果没有该路径则新建路径
            os.mkdir(self.img_path)


    def process_item(self, item, spider):
        img_name = item["name"]
        img_url = item["img"]
        img_name_chap = item['chap']

        # 三级目录
        img_name_path = os.path.join(self.img_path,img_name,img_name_chap)
        if not os.path.exists(img_name_path):
            os.makedirs(img_name_path)
        i = 0
        for url in img_url:
            img_name = str(i)+'.jpg'
            i=i+1
            try:
                print(img_name,img_name_chap,'正在下载')
                request.urlretrieve(url,os.path.join(img_name_path,img_name))
            # 这里下载图片使用的是urllib库进行的下载，后期说一下怎么使用scrapy正确的下载方式

            except Exception:
                pass
           