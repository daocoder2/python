#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import scrapy
import re
from xiaoqu.items import XiaoquItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join


class XiaoquSpider(scrapy.Spider):
    # 标志当前爬虫的名字
    name = 'xiaoqu'
    # 可选，指爬虫允许爬取的列表
    allow_domain = ['http://hf.58.com']
    # http://hf.58.com/xiaoqu/840/pn_2/ 蜀山区
    # http://hf.58.com/xiaoqu/841/pn_2/ 包河区
    # http://hf.58.com/xiaoqu/838/pn_2/ 庐阳区
    # http://hf.58.com/xiaoqu/839/pn_2/ 瑶海区
    # http://hf.58.com/xiaoqu/11384/pn_2/ 经开区
    # http://hf.58.com/xiaoqu/11385/pn_2/ 高新区
    # http://hf.58.com/xiaoqu/11386/pn_2/ 新站区
    # http://hf.58.com/xiaoqu/11387/pn_2/ 滨湖新区
    # http://hf.58.com/xiaoqu/11388/pn_2/ 政务区
    # http://hf.58.com/xiaoqu/22171/pn_2/ 北城新区
    # http://hf.58.com/xiaoqu/1974/pn_2/ 合肥周边
    start_urls = ['http://hf.58.com/xiaoqu/pn_1']

    def __init__(self):
        super(XiaoquSpider, self).__init__()
        self.domain = 'http://hf.58.com'

    def parse(self, response):
        # 获取下一页地址和发起请求
        next_selector = response.xpath('//a[@class="next"]/@href')
        for url in next_selector.extract():
            print(response.urljoin(url))
            yield scrapy.Request(response.urljoin(url))
        # 获取详情页地址和发起请求
        items_selector = response.xpath('//tr[@logr="p__8796520510214"]')
        for item_selector in items_selector:
            # item_selector = items_selector[0]
            item = XiaoquItem()
            item['name'] = item_selector.xpath('.//li[@class="tli1"]/a/text()')[0].extract()
            item['name'] = self.trim(item['name'])
            item['alias'] = item_selector.xpath('.//li[@class="tli1"]/a/span/text()')[0].extract()
            item['alias'] = self.trim(string=item['alias'], pattern=r'^\((.*?)\)$')
            item['detail_url'] = item_selector.xpath('.//li[@class="tli1"]/a/@href')[0].extract()
            yield scrapy.Request(response.urljoin(item['detail_url']),
                                 callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item'].copy()
        table_selector = response.xpath('//table[@class="info-tb"]')
        item['qu_tarea'] = table_selector.xpath('//a[@class="sq-link"]/text()').extract()
        item['address'] = table_selector.xpath('tr[position()=1]/td[position()=4]/text()').extract()
        if item['address']:
            item['address'] = item['address'][0]
            item['address'] = self.trim(item['address'])
        item['jianzhu_type'] = table_selector.xpath('//tr[position()=2]/td[position()=2]/text()').extract()
        if item['jianzhu_type']:
            item['jianzhu_type'] = item['jianzhu_type'][0]
            item['jianzhu_type'] = self.trim(item['jianzhu_type'])
        item['jianzhu_type'] = self.trim(item['jianzhu_type'])
        item['wuye_fee'] = table_selector.xpath('//tr[position()=3]/td[position()=4]/text()').extract()[0]
        item['wuye_fee'] = self.trim(string=item['wuye_fee'])
        item['wuye_fee'] = self.trim(string=item['wuye_fee'], pattern=r'(\d+\.\d+)')
        item['rongjilv'] = table_selector.xpath('//tr[position()=4]/td[position()=4]/text()').extract()[0]
        item['rongjilv'] = self.trim(string=item['rongjilv'], pattern=r'(\d+\.\d+)')
        item['jianzhu_year'] = table_selector.xpath('//tr[position()=5]/td[position()=2]/text()').extract()[0]
        item['jianzhu_year'] = self.trim(string=item['jianzhu_year']).replace('年', '')
        item['lvhualv'] = table_selector.xpath('//tr[position()=5]/td[position()=4]/text()').extract()
        if item['lvhualv']:
            item['lvhualv'] = item['lvhualv'][0]
            item['lvhualv'] = self.trim(string=item['lvhualv'])
        item['jz_mianji'] = table_selector.xpath('//tr[position()=6]/td[position()=4]/text()').extract()[0]
        item['jz_mianji'] = self.trim(string=item['jz_mianji']).replace('平方米', '')
        item['wuye_company'] = table_selector.xpath('//tr[position()=8]/td[position()=2]/text()').extract()[0]
        item['wuye_company'] = self.trim(string=item['wuye_company'])
        item['builder'] = table_selector.xpath('//tr[position()=9]/td[position()=2]/text()').extract()[0]
        item['builder'] = self.trim(string=item['builder'])
        item['desc'] = response.xpath('//div[@class="detail-mod desc-mod"]/p[@class="desc"]/text()').extract()
        if item['desc']:
            item['desc'] = item['desc'][0]
            item['desc'] = self.trim(string=item['desc'], next_line=True)
        yield item

    def trim(self, string, pattern=None, next_line=True):
        string = string.strip()
        if next_line:
            string = string.replace('\n', '')
            string = string.replace('\r', '')
        if pattern is not None:
            string_match = re.match(pattern, string, re.S)
            if string_match:
                string = string_match.groups()[0]
        return string


