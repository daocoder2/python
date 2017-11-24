# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class VmoviePipeline(object):
    def process_item(self, item, spider):
        return item


class PicsDownloadPipeline(ImagesPipeline):
    # def file_path(self, request, response=None, info=None):
    #     image_name = '这里可以自定义图片名'
    #     return 'full/%s' % (image_name)
    img_urls = set()

    def get_media_requests(self, item, info):
        for image_url in item['cover']:
            if image_url in self.img_urls:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.img_urls.add(image_url)
                yield Request(image_url)

    def item_completed(self, results, item, info):
        # [scrapy.pipelines.files] ：https://segmentfault.com/q/1010000008135270
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem("Item contains no images")
        item['cover_path'] = image_path
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        self.file = open('test.json', 'w', encoding='utf-8')
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n,"
        self.file.write(line)
        return item


