# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup 
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from ..items import ScrapyprojectItem


class CarrefourSpider(scrapy.Spider):
    name = 'carrefour'
    #allowed_domains = ['example.com']
    start_urls = ['https://online.carrefour.com.tw/']

    def start_requests(self):
    	for url in self.start_urls:
    		yield SplashRequest(url,self.parse,args={'wait':0.5})

    def parse(self, response):
        print('=============parse here=========')
        #soup = BeautifulSoup(response.text, 'lxml')
        #quotes = soup.select('div.detailed-class div.more-left div.top1 a:nth-child(1)')
        #each category

        for res in response.css('div.detailed-class div.more-left div.top1'):
            
            title = res.css('span::text').extract_first()

            for r in res.css('a'):
                tag = r.css('span::text').extract_first()
                
                if tag == None:
                    continue
                print('\n----------parsing : ', tag)

                url = r.css('::attr(href)').extract_first()
                category_url = response.urljoin(url)
                print('category_url = ',category_url)
                yield SplashRequest(category_url,callback=self.parse_item,args={'wait':0.5},dont_filter=True)
	
    def parse_item(self, response):
        print("~~~~~~~~~~~~items~~~~~~~~~~")
        print('items url = ',response.url)
        items = ScrapyprojectItem()
        category = response.css('div.crumbs a:nth-child(2)::text').extract_first()    
        for q in response.css('div.hot-recommend-item'):
            title = q.css('div.commodity-desc ::text').extract_first()
            price = q.css('div.current-price > span > em ::text').extract_first()
            items['store'] = 'carrefour'
            items['category'] = category.strip().strip('\/').strip()
            items['img'] = q.css('div.box-img > a > img::attr(data-src)').extract_first()
            items['title'] = title.strip()
            items['price'] = price.strip('$')
            yield(items)

        #apend next page here 

        #get next page url
        #yield parse item




    def parse_category(self, response):
        print("-------------get category----------")
        
        print('get url = ',response.url)
        
        category = response.css('div.crumbs a:nth-child(3)::text').extract_first()
        print('category = ', category)
        
        #get next url 
        for r in response.css('ul.commodity-classification ul.active li p'):
            url = r.css('a::attr(href)').extract_first()
            print('---smt = ', url)
            items_url = response.urljoin(url)
        #for q in response.css('div.hot-recommend-item'):
            #items['category'] = category
            #items['img'] = q.css('div.box-img > a > img::attr(data-src)').extract_first()
            #items['title'] = q.css('div.commodity-desc ::text').extract_first()
            #items['price'] = q.css('div.current-price > span > em ::text').extract_first()
            #yield(items)
        #quotes = soup.select("div.commodity-desc")
        #for q in quotes:
        #    items['title'] = q.text
        #    yield(items)
    