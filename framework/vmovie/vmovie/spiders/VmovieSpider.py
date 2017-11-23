#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import scrapy
import time
import re
from urllib import parse
from vmovie.items import VmovieItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join

class VmovieSpider(scrapy.Spider):
    # 标志当前爬虫的名字
    name = 'vmovie'
    # 可选，指爬虫允许爬取的列表
    allow_domain = ['vmovier.com']
    start_urls = ['http://www.vmovier.com/index/index/p/1']

    def __init__(self):
        super(VmovieSpider, self).__init__()
        self.domain = 'www.vmovier.com/'

    def parse(self, response):
        # Get the next index URL and yield Requests
        next_selector = response.xpath('//a[@class="next"]/@href')
        for url in next_selector.extract():
            yield scrapy.Request(parse.urljoin(response.url, url))

        # Get item URL and yield Requests
        items_selector = response.xpath('//li[@class="clearfix"]')
        for item_selector in items_selector:
            # self.log('----------------------' + item_selector)
            # print(item_selector)
            # item_data = item_selector.extract()
            item = VmovieItem()
            item['name'] = item_selector.xpath("./a/@title")[0].extract()
            item['cover'] = item_selector.xpath("./a/img/@src")[0].extract()
            item['duration'] = item_selector.xpath('.//span[@class="film-time"]/'
                                               'text()')[0].extract()
            # ll = ItemLoader(item=VmovieItem(), response=item_selector)
            # ll.add_xpath('cover', "./a/img/@src")
            # ll.add_xpath('duration', '//span[@class="film-time"]/text()')
            # item = ll.load_item()
            detail_url = item_selector.xpath("./a/@href")[0].extract()
            self.log('----------------------' + detail_url)
            yield scrapy.Request(parse.urljoin(response.url, detail_url),
                                 callback=self.parse_detail, meta=item)

    def parse_detail(self, response):
        """ This function parses a property page.
        @url http://www.vmovier.com/53020?from=index_new_title
        @returns items dl
        @scrapes name desc playurl
        @scrapes time url project spider
        """
        # Create the loader using the response
        dl = ItemLoader(item=VmovieItem(), response=response)
        dl.add_value('name', response.meta['name'])
        dl.add_value('cover', response.meta['cover'])
        dl.add_value('duration', response.meta['duration'])
        # Load fields using XPath expressions
        # dl.add_xpath('name', '//h1[@class="post-title"]/text()',
        #              MapCompose(str.strip, lambda i: i.replace('&nbsp;', '')))
        dl.add_xpath('desc', '//div[@class="p00b204e980"]/p[position()>1]',
                     Join(' '), self.strip_tag, str.strip)
        dl.add_xpath('playurl', '//div[@class="p00b204e980"]//iframe/@src')

        # Housekeeping fields
        dl.add_value('time', int(time.time()))
        dl.add_value('url', response.url)
        dl.add_value('project', self.settings.get('BOT_NAME'))
        dl.add_value('spider', self.name)
        return dl.load_item()

    def strip_tag(self, string):
        """ This function parses a property page.
        @url http://www.vmovier.com/53020?from=index_new_title
        @returns result
        """
        dr = re.compile(r'<[^>]+>', re.S)
        result = re.sub(dr, '', string)
        result = result.replace('本文文字内容归本站版权所有，转载请注明来自V电影（vmovier.com）', '')
        return result

