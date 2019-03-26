# -*- coding: utf-8 -*-
import scrapy
import sys
from runoob_data.items import RunoobDataItem
import json


class RunoobApiSpider(scrapy.Spider):
    name = "runoob_api"
    allowed_domains = ["www.runoob.com"]
    start_urls = (
        'http://www.runoob.com/wp-json/wp/v2/posts?per_page=100&page=1',
        'http://www.runoob.com/wp-json/wp/v2/pages?per_page=100&page=1',
        'http://www.runoob.com/wp-json/wp/v2/media?per_page=100&page=1',
        'http://www.runoob.com/wp-json/wp/v2/categories?per_page=100&page=1',
        'http://www.runoob.com/wp-json/wp/v2/tags?per_page=100&page=1',
        'http://www.runoob.com/wp-json/wp/v2/tags?per_page=100&page=2',
    )
    # 编码设置为utf8,避免中文显示为unicode编码
    reload(sys)
    sys.setdefaultencoding('utf-8')

    def start_requests(self):
        reqs = []
        for i in range(1, 88):
            req = scrapy.Request("http://www.runoob.com/wp-json/wp/v2/posts?per_page=100&page=%s" % i)
            reqs.append(req)
        return reqs


    def parse(self, response):
        item = RunoobDataItem()
        url_str = response.url
        url_arr = url_str.split('?')
        url_arr1 = url_arr[0].split('/')
        api_type = url_arr1[-1]
        item['url'] = url_str
        item['type'] = api_type
        item['data'] = response.body
        # print(url_str)
        yield item
        # body = json.loads(response.body)
        # if response.status == 200 and isinstance(body, list) and len(body) == 100:
        #     url_arr2 = url_arr[1].split('&page=')
        #     next_page = str(int(url_arr2[1]) + 1)
        #     next_url = url_arr[0] + '?per_page=100&page=' + next_page
        #     print('next_page', next_page)
        #     yield scrapy.Request(next_url, self.parse(response))

