# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import json

class RunoobDataPipeline(object):
    def process_item(self, item, spider):
        return item



class MysqlPipeline(object):

    def __init__(self):

        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            db='runoob_data',
            host='127.0.0.1',
            user='root',
            passwd='',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=True)



    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        sql = "select * from `tbl_data` where url = '%s'" % item['url']
        tx.execute(sql)
        result = tx.fetchone()
        if result:
            log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        else:
            sql = """insert into `tbl_data`(`id`, `url`,`type`,`data`, `create_time`) VALUES (NUll,%s,%s,%s, CURRENT_TIMESTAMP);"""
            values = (item['url'], item['type'], item['data'])
            print(item['url'])
            # print(sql)
            tx.execute(sql, values)


    def handle_error(self, e):
        print ('handle_error')
        log.err(e)