# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']


    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象
    # star_requests()方法读取 start_urls列表中的url并生成 request对象，发送给 引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):

        yield scrapy.Request(url=self.start_urls[0],callback=self.parse,dont_filter=False,cookies=self.cookies)

    # 解析函数
    def parse(self, response):
        """
        获取电影的标题和链接
        """
        # 打印网页的url
        print(response.url)
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        for movie in movies:
            item = MaoyanItem()
            title = movie.xpath('./a/text()') # 电影名称
            link =  movie.xpath('./a/@href') # 链接
            item['title'] = title.extract_first().strip()
            item['link'] = 'https://' + self.allowed_domains[0] + link.extract_first().strip() # 拼接完整的 url
            yield scrapy.Request(url=item['link'],meta={'item': item},callback=self.parse2)

    def parse2(self,response):
        """
        到对应标题的链接中获取电影信息
        """
        item = response.meta['item']
        infos = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        print(infos)
        for info in infos:
            category = info.xpath('./ul/li/a/text()').extract()
            date = info.xpath('./ul/li[last()]/text()').extract_first().strip()
            item['category'] = category
            item['date'] = date

        yield item