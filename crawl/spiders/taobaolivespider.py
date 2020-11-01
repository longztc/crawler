#!/usr/bin/env python
# coding=utf-8
import json

import requests
import scrapy
import re
from crawl import constants

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from crawl.items import TaobaoLiveItem
from scrapy.http import Request
from urllib.request import urlopen
from crawl.jsphlim.tool import ListCombiner

class SinaNewsSpider(scrapy.Spider):
    name = 'taobao_live_spider'
    start_urls = constants.Starts_URL
    allowed_domains = ['m.taobao.com']

    url_pattern = r'https?://(\w+)\.sina.com.cn/(\w+)/(\d{4}-\d{2}-\d{2})/doc-([a-zA-Z0-9]{15}).(?:s)html'
    url_pattern2 = r'https?://(\w+)\.sina.com.cn/(\w+)/(\w+)/(\d{4}-\d{2}-\d{2})/doc-([a-zA-Z0-9]{15}).(?:s)html'
    pattern = "<meta name=\"sudameta\" content=\"comment_channel:(\w+);comment_id:comos-([a-zA-Z0-9]{14})\""
    image_url_pattern = "<meta property=\"og:image\" content=\"(https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])\""

    def parse(self, response):
        pat = re.compile(self.url_pattern2)
        next_urls = re.findall(pat, str(response.body))

        for url in next_urls:
            article = 'http://'+url[0]+'.h5.m.taobao.com/'+url[1]+'/'+url[2]+'/'+url[3]+'/doc-'+url[4]+'.shtml'
            print(article)
            yield Request(article,callback=self.parse_news)

    def parse_news(self, response):
        item = TaobaoLiveItem()
        item['source'] = "TaobaoLive"
        pat = re.compile(self.url_pattern2)
        res = re.findall(pat, str(response.url))
        if (res != []):
            item['theme'] = constants.Themes.get(res[0][0])
            item['date'] = res[0][2]

        sel = requests.get(response.url)
        sel.encoding = 'utf-8'
        sel = sel.text

        pat = re.compile(self.pattern)
        res = re.findall(pat, str(sel))

        if res == []: return
        commentsUrl = 'https://h5.m.taobao.com/taolive/video.html?userId=3962528240'
        soup = BeautifulSoup(sel,'html.parser')

        if len(temp.text)>len(temp1.text):
            contents = temp.find_all('p')
        else:
            contents = temp1.find_all('p')

        item['comment'] = str(res[0][1])
        
        pat = re.compile(self.image_url_pattern)
        res = re.findall(pat, str(sel))

        item['user'] = str(res[1])

        yield item