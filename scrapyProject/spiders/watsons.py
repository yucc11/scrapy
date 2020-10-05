# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup 
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from ..items import ScrapyprojectItem

class WatsonsSpider(scrapy.Spider):
    name = 'watsons'
    allowed_domains = ['watsons.com']
    start_urls = ['https://www.watsons.com.tw/']
    #def set_id(self):
        #self.id = 100

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        print("=============parse here========")
        #soup = BeautifulSoup(response.text, 'lxml')
        #quotes = soup.select('div.navContainer a')
        quotes = response.css('div.navContainer')
        #self.set_id()
        count = -1
        for q in quotes:
            count += 1
            if count < 3:
                continue
            #category = q.css('span::text')
            #category = q.text
            #print('\ncategory = ',category)
            url = q.css('a::attr(href)').extract_first()
            #url = q.get('href')
            category_url = response.urljoin(url)
            print('\ncategory = ',category_url)
            yield SplashRequest(category_url, self.parse_url, args={'wait': 0.5}, dont_filter=True)

    def parse_url(self, response):
        #11 times
        print('==============get urls=============')
        print('get url = ',response.url)
        #print(response.text)
        quotes = response.css('div.box.level3 div.box-head h2.box-head-name')
        #self.id += 1
        #print('ID = ',self.id)
        for q in quotes:
            #print('href.= ')
            a = q.css('a::attr(href)').extract_first()
            #print(a)
            category_url = response.urljoin(a)
            print('\ncategory = ',category_url)
            yield SplashRequest(category_url, self.parse_item, args={'wait': 0.5}, dont_filter=True)

    def parse_item(self, response):
        items = ScrapyprojectItem()
        print('------------get items-------------')

        print('get itme url  = ',response.url)
        quotes = response.css('div.productItemContainer')
        category = response.css('div.multilevel-title span:nth-child(2) a span::text').extract_first()
        for q in quotes:
            #use response.urljoin if needed -> join ref url(items['img']) & https://watsons.com.tw
            #https://www.watsons.com.tw
            url = q.css('div.productItemPhotoContainer a img::attr(data-original)').extract_first()
            title = q.css('div.productNameInfo a h3.h1::text').extract_first()
            price = q.css('div.productNameInfo div.h2::text').extract_first()
            items['store'] = 'watsons'
            items['category'] = category.strip()
            items['img'] = response.urljoin(url)
            items['title'] = title.strip()
            items['price'] = price.strip('$')
            yield(items)
        #get next page to finish parsing items in this category
        next_page_url = response.css('div.my-pagination a.next').extract_first()
        print('next_page_url = ',next_page_url)
        #print('ID = ',self.id)
        #yield SplashRequest(next_page_url, self.parse_item, args={'wait': 0.5}, dont_filter=True)::attr(href)

        #q.css('div.box .level3 div.box-head-name a::attr(href)')
        #items = UiddprojectItem()url = q.get('href')
            #category_url = response.urljoin(url)
        #for url in response.css('div.col-1 dt.lv1 a ::attr(href)'):
         #   category_url = response.urljoin(url)
         #   print('\ncategory_url = ',category_url)
      
