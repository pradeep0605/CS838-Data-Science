from scrapy.spiders import Spider
#from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
#from test.items import TestItem
import scrapy
from amazon_crawl.items import AmazonCrawlItem

class GoodreadsScrawler(Spider) :
    name = "amazon_crawl"
    allowed_domains = ["amazon.com"]
    #Comprehension to list all the pages that we want
    start_urls = ["https://www.amazon.com/gp/bestsellers/books/ref=sv_b_2"]
    site_url = "https://www.amazon.com"
    
    def parse(self, response):
        hxs = Selector(response)
        rows = hxs.xpath('//*[@id="zg_browseRoot"]/ul/ul//li//a/@href')
        
        categories = []
        for row in rows:
            category = row.extract()            
            print(category)
            categories.append(category)
        
        for category in categories:
            category_100books = [category + "?_encoding=UTF8&pg=" + str(i) for i in range(1, 6)]
            category_100books = category_100books[1:]
            for _20books in category_100books:
                request = scrapy.Request(_20books, callback=self.parse_list, dont_filter=True)
                yield request
                #break
            #break
        #for link in links:
        #    request = scrapy.Request(link, callback=self.parse_bookinfo)
        #   yield request

    def parse_list(self, response):
        sel = Selector(response)
        _20books = sel.xpath('//*[@id="zg_centerListWrapper"]//div/div[2]/div/a/@href')
    
        #_20books = _20books[1:]
        for book in _20books:
            book_url = self.site_url + book.extract();
            print(book_url)
            request = scrapy.Request(book_url, callback=self.parse_bookinfo)
            yield request
            #break
                              
    def parse_bookinfo(self, response):
        sel = Selector(response)
        #items = response.meta['items']
        # An Item from this page
        
        itm = AmazonCrawlItem()
        # Scrape the Title of the book (Not the original name, might have series number in the name)
        try :
            Title = "" + sel.xpath('//*[@id="productTitle"]/text()').extract_first()
            if Title:
                Title = Title.strip()
            itm['Title'] = Title
            print(Title)
        except:
            print("Error Title")
        
        try:
            Average_Rating = sel.xpath('//*[@id="reviewSummary"]/div[2]/span/a/span/text()').extract_first()
            #Ratings = Ratings.split(" ")[0]
            Average_Rating = Average_Rating.strip()
            itm['Average_Rating'] = Average_Rating
            print(Average_Rating)
        except:
            print("Error Average_Rating")
        
        try:
            Ratings = sel.xpath('//*[@id="reviewSummary"]/div[1]/a/div/div/div[2]/div/span/text()').extract_first()
            Ratings = Ratings.strip()
            itm['Ratings'] = Ratings
            itm['Reviews'] = Ratings
            print(Ratings)
        except:
            print("Error Average_Rating")            
        
        try:
            ProductDetails = sel.xpath('//div[@class="content"]/ul/*[not(self::li[@id="SalesRank"])]//text()').extract()
            #'//div[@class="content"]/ul//li[not(self::li[@id="SalesRank"])]//text()'
            ProductDetails = [x.strip() for x in ProductDetails if x.strip() != ""]
            i = 0
            for i in range(0, len(ProductDetails)):
                #amazon website has this function in the body which is included as part of text when we extract()
                #Thus, we find that string which from where the code starts and prune the array to get cleaner data.
                if ProductDetails[i].find("function acrPopoverHover") != -1:
                    break
            ProductDetails = ProductDetails[0:i]

            itm['ProductDetails'] = ProductDetails
            print(ProductDetails)
        except:
            print("Error Product Details")

        try:
            Summary = sel.xpath('//p//text()').extract()
            itm['Summary'] = Summary
            #print(Summary)
        except:
            print("Error Average_Rating")
            
     
            
        yield itm

    
