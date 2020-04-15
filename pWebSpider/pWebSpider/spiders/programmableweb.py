# -*- coding: utf-8 -*-
import scrapy
import os
import re

class ProgrammablewebSpider(scrapy.Spider):
    name = 'programmableweb'
    allowed_domains = ['programmableweb.com']

    start_urls = []
    rs = os.path.exists('E://pWebAPIListTest1.txt')
    if rs == True:
        # 打开文件
        fRead = open('E://pWebAPIListTest1.txt',mode = 'r')
        urllist = fRead.readlines()
        for url in urllist:
            # 去除换行键
            url = url.strip('\n')
            # 保存到现有列表
            start_urls.append('https://www.programmableweb.com'+url)
    
    
    # # 读取由requests爬取的全部链接
    # file=open('E://pWebAPIListTest1.txt','r',encoding='utf8')
    # # readlines读取返回列表
    # urllist=file.readlines()
    # start_urls = []
    # for u in urllist:
    #     # 由于写入时以\n分行,读取后会在尾部留有\n导致无法连接,需sub掉
    #     u=re.sub(r'\n','',u)
    #     # requests 爬取的相对链接 需要拼接
    #     start_urls.append('https://www.programmableweb.com'+u)


    def parse(self, response):
        # 提取数据
        desc = response.xpath('//div[@class="api_description tabs-header_description"]/text()').get()
        headline = response.xpath('//div[@class="master_record_div"]/h1/text()').get()
        tags = response.xpath('//div[@class="tags"]/a')
        tag = []
        for t in tags:
            tag.append(t.xpath('./text()').get())
        submitted = response.xpath('//div[@class="version pull-left col-lg-2"][2]/text()').get()
        status = response.xpath('//span[@class="recommended"][1]/text()').get()
        style = response.xpath('//div[@class="version-status-style pull-left col-lg-2"][1]/text()').get()
        followers = response.xpath('//a[@class="followers"]/span/text()').get()

        items = {
            'headline':headline,
            'desc':desc,
            'tag':tag,
            'submitted':submitted,
            'status':status,
            'followers':followers,
            'style':style
        }
        yield items