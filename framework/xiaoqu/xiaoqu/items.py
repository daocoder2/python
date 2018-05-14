# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose
from w3lib.html import remove_tags


class XiaoquItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # id 58小区拼音
    id = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    # 小区名字
    name = scrapy.Field()
    # 小区别名
    alias = scrapy.Field()
    # 小区地址
    detail_url = scrapy.Field()
    # 区名和商圈名
    qu_tarea = scrapy.Field()
    # 物业费
    wuye_fee = scrapy.Field()
    # 物业公司
    wuye_company = scrapy.Field()
    # 开发商
    builder = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 建筑年代
    jianzhu_year = scrapy.Field()
    # 建筑类型
    jianzhu_type = scrapy.Field()
    # 建筑面积
    jz_mianji = scrapy.Field()
    # 绿化率
    lvhualv = scrapy.Field()
    # 容积率
    rongjilv = scrapy.Field()
    # 小区简介
    desc = scrapy.Field()

