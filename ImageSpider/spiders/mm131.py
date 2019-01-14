# -*- coding: utf-8 -*-
import time
import re

import scrapy
from ImageSpider.items import ImagespiderItem


host_name = "http://www.mm131.com/"
key_names = ["xinggan", "qingchun", "xiaohua", "chemo", "qipao", "mingxing"]


class Mm131Spider(scrapy.Spider):
    name = 'mm131'
    allowed_domains = ['www.mm131.com']
    start_urls = ['http://www.mm131.com/xinggan/']

    def parse(self, response):
        selector = scrapy.Selector(response)

        next_folder_pages = selector.xpath("//dd[@class='page']/a[text()='下一页']/@href").extract()
        next_folder_pages_text = selector.xpath("//dd[@class='page']/a/text()").extract()
        # total_pages = selector.xpath("//div[@class='content-page']/span/text()").extract()[0]
        # total_pics = int(re.findall(r"共(.+?)页", total_pages))

        # 读取图片夹下一页
        if '下一页' in next_folder_pages_text:
            next_url = "http://www.mm131.com/xinggan/%s" % next_folder_pages[0]
            request = scrapy.http.Request(next_url, callback=self.parse)
            # time.sleep(1)
            yield request

            # 读取每个图片夹的链接
            all_info = selector.xpath("//div[@class='main']/dl/dd/a[@target]")
            for info in all_info:
                link = info.xpath("@href").extract()[0]
                request = scrapy.http.Request(link, callback=self.parse_folder_page)
                # time.sleep(1)
                yield request

    def parse_folder_page(self, response):
        selector = scrapy.Selector(response)

        yield self.build_item(response)

        next_pages = selector.xpath("//div[@class='content-page']/a[text()='下一页']/@href").extract()[0]
        next_pages_text = selector.xpath("//div[@class='content-page']/a/text()").extract()
        if '下一页' in next_pages_text:
            next_url = "http://www.mm131.com/xinggan/%s" % next_pages
            request = scrapy.http.Request(next_url, callback=self.parse_item)
            yield request

    def parse_item(self, response):
        yield self.build_item(response)

    def build_item(self, response):
        selector = scrapy.Selector(response)
        item = ImagespiderItem()
        image_title = selector.xpath('//h5/text()').extract()
        image_url = selector.xpath("//div[@class='content-pic']/a/@href").extract()
        if selector.xpath("//div[@class='content-pic']/a/img/@src").extract():
            image_src = selector.xpath("//div[@class='content-pic']/a/img/@src").extract()
        if selector.xpath("//div[@class='content-pic']/a/img/@alt").extract():
            pic_name = selector.xpath("//div[@class='content-pic']/a/img/@alt").extract()

        item['title'] = image_title
        item['url'] = image_url
        item['src'] = image_src
        item['alt'] = pic_name
        return item

