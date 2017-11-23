# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 影片编号
    # vid = scrapy.Field()
    # 影片封面
    cover = scrapy.Field()
    # 影片时长
    duration = scrapy.Field()
    # 影片名称
    name = scrapy.Field()
    # 影片简介
    desc = scrapy.Field()
    # 影片地址
    playurl = scrapy.Field()

    # 抓取时间
    time = scrapy.Field()
    # 抓取地址
    url = scrapy.Field()
    # 项目名称
    project = scrapy.Field()
    # 蜘蛛名称
    spider = scrapy.Field()

    pass
