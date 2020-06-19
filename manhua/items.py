# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ManhuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name= scrapy.Field()# 漫画名称
    vid = scrapy.Field()# 漫画名称的代码
    id = scrapy.Field()# 漫画章节代码
    chap = scrapy.Field()#漫画第几章节
    img= scrapy.Field()# 某漫画某章节所有图片的地址
