# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xiaoqu.dbhelper as db


class XiaoquPipeline(object):

    def process_item(self, item, spider):
        db_helper = db.DbHelper('STORE_CONFIG')
        try:
            query_sql = "select * from `xiaoqu` where `name`='%s'" % item['name']
            print(query_sql)
            (value, column) = db_helper.get_one(query_sql)
            # 重复
            if value:
                pass
            else:
                # item['detail_url'] = item['detail_url'].replace('/', '\/')
                insert_sql = "insert into `xiaoqu`(`name`, `alias`, `detail_url`, `quname`, `tarea`, `wuye_fee`," \
                             " `wuye_company`, `builder`, `address`, `jianzhu_year`, `jianzhu_type`, `jz_mianji`, " \
                             "`rongjilv`, `lvhualv`, `desc`) value ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                             "'%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (item['name'], item['alias'],
                                     item['detail_url'], item['qu_tarea'][0], item['qu_tarea'][1],
                                     item['wuye_fee'], item['wuye_company'], item['builder'],
                                     item['address'], item['jianzhu_year'], item['jianzhu_type'],
                                     item['jz_mianji'], item['rongjilv'], item['lvhualv'], item['desc'])
                # 提交sql语句
                print(insert_sql)
                insert_res = db_helper.insert(insert_sql)
                print(insert_res)
        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item
