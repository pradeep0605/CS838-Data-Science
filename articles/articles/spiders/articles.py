from scrapy.spiders import Spider
from scrapy import Selector
import scrapy
#from articles.items import ArticlesCrawlItem
#import ArticlesCrawlItem

class ArticleScrawler(Spider) :
     name = "articles"
     allowed_domains = ["slate.com"]
     #Comprehension to list all the pages that we want
     start_urls = [("http://www.slate.com/topics/s/slate_book_review." + str(i) + ".html") for i in range(1,32)]
     site_url = "http://www.slate.com/"
     def parse(self, response):
         hxs = Selector(response)
         rows = hxs.xpath('/html/body/div[2]/article/section/div[1]//div/a/@href')
         for row in rows:
             print row.extract()
             request = scrapy.Request(row.extract(), callback=self.parse_article)
             yield request

     def parse_article(self, response):
         selector = Selector(response)
         #itm = ArticlesCrawlItem()
         itm = {}
         Title =  selector.xpath('//h1[@class="hed"]/text()').extract_first()
         Gist = selector.xpath('//h2[@class="dek"]/text()').extract_first()
         Reviewer = selector.xpath('//*[@id="main_byline"]/a/text()').extract_first() 
         #Body = selector.xpath('//*[@id="story-0"]/section//div//div/p/text()').extract_first()
         Body = selector.xpath('//p/text()').extract()
         combined = [x.strip() for x in Body]
         itm['Title'] = Title
         itm['Gist'] = Gist
         itm['Reviewer'] = Reviewer
         itm['Body'] = combined
         return itm



