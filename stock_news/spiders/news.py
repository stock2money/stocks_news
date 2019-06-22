# -*- coding: utf-8 -*-
import scrapy
from stock_news.items import NewsItem
import re

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['stock.jrj.com.cn']
    start_urls = ['http://stock.jrj.com.cn/list/stockgszx.shtml']
    base_url = 'http://stock.jrj.com.cn/list/stockgszx-%d.shtml'
    pages = 20

    def __init__(self):
        for i in range(2, self.pages):
            self.start_urls.append(self.base_url % i)

    def parse(self, response):
        news = response.xpath(
            '//*[@class="list-main"]/ul/li[not(contains(@class,"line"))]')
        for each in news:
            item = NewsItem()
            item["time"] = each.xpath('./span/text()').extract()[0]
            item["title"] = each.xpath('./a/@title').extract()[0]
            item["href"] = each.xpath('./a/@href').extract()[0]
            print(item)
            request = scrapy.Request(url=item["href"], callback=self.parseHref)
            request.meta['item'] = item
            yield request
            break
    
    def parseHref(self, response):
        item = response.meta['item']
        article = response.xpath('//*[@class="texttit_m1"]//text()').extract()
        detail = ''
        remove = re.compile(r'<.*?>', re.S)
        for p in article:
            if p == '\r\n':
                detail += '@'
                continue
            if '.klinehk{margin:0 auto 20px;}' in p:
                continue
            p = re.sub(remove, '', p)
            detail += p
        item['detail'] = detail
        yield item



