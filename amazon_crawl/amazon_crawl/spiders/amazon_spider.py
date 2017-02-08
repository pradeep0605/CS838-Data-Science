from scrapy.spiders import Spider
#from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
#from test.items import TestItem
import scrapy
from goodreads_crawl.items import GoodreadsCrawlItem

class GoodreadsScrawler(Spider) :
    name = "amazon_crawl"
    allowed_domains = ["amazon.com"]
    #Comprehension to list all the pages that we want
    start_urls = ["https://www.amazon.com/gp/bestsellers/books/ref=sv_b_2"]
    site_url = "https://www.amazon.com"
    
    def parse(self, response):
        hxs = Selector(response)
        rows = hxs.xpath('//*[@id="zg_browseRoot"]/ul/ul//li//a/text()')
        
        for row in rows:
            print(row.extract())
        
        #for link in links:
        #    request = scrapy.Request(link, callback=self.parse_bookinfo)
        #   yield request


    def parse_bookinfo(self, response):
        selector = Selector(response)
        #items = response.meta['items']
        # An Item from this page
        
        itm = GoodreadsCrawlItem()
        # Scrape the Title of the book (Not the original name, might have series number in the name)
        try :
            Title = "" + selector.xpath('//h1[@class="bookTitle"]/text()').extract_first()
            brackets = selector.xpath('//a[@class="greyText"]/text()').extract_first()
            Title = Title.strip()
            if brackets:
                brackets = brackets.strip()
                Title = Title + " " + brackets
            itm['Title'] = Title    
        except:
            print("Error Title")
        
        try:
            # Get the original Title of the book
            Original_Title = selector.xpath('//*[@id="bookDataBox"]/div[1]/div[2]/text()').extract_first()
            Original_Title = Original_Title.strip()
            itm['Original_Title'] = Original_Title
            #print(Title)
        except:
            print("Error Original_Title")
        
        try:
            # Get the name of the author
            Author = selector.xpath('//*[@id="bookAuthors"]/span[2]/a[1]/span/text()').extract_first()
            Author = Author.strip();
            itm['Author'] = Author
            #print(Author)
        except:
            print("Error Author")
            
        try:
            Edition_Language = selector.xpath('//*[@id="bookDataBox"]/div[3]/div[2]/text()').extract_first()
            Edition_Language = Edition_Language.strip()
            itm['Edition_Language'] = Edition_Language
            #print(Edition_Language) 
        except:
            print("Error Edition_Language")
        
        try:
            Average_Rating = selector.xpath('//*[@id="bookMeta"]/span[3]/span/text()').extract_first()
            Average_Rating = Average_Rating.strip()
            itm['Average_Rating'] = Average_Rating
            #print(Average_Rating)
        except:
            print("Error Average_Rating")
            
        try:
            Ratings = selector.xpath('//*[@id="bookMeta"]/a[2]/span/text()').extract_first()
            Ratings = Ratings.strip()
            Ratings = Ratings.split(" ")[0]
            itm['Ratings'] = Ratings
            #print(Ratings)
        except:
            print("Error Ratings")
            
        try:
            Reviews = selector.xpath('//*[@id="bookMeta"]/a[3]/span/span/text()').extract_first()
            Reviews = Reviews.strip()
            #Reviews = Reviews.split(" ")[0]
            itm['Reviews'] = Reviews
        except:
            print("Error Reviews")
        #print(Reviews)
        
        #<a class="actionLinkLite bookPageGenreLink" href="/genres/fantasy">Fantasy</a>
        try:
            Genres = selector.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()').extract()
            itm['Genres'] = Genres
            #print(Genres)
        except:
            print("Error Genres")
        
        try:
            Edition = selector.xpath('//*[@id="bookDataBox"]/div[3]/div[2]/text()').extract_first()
            Edition = Edition.strip()
            #Reviews = Reviews.split(" ")[0]
            itm['Edition'] = Edition
            #print(Edition)
        except:
            print("Error Edition")
        
        try:
            Pages = selector.xpath('//*[@id="details"]/div[1]/span[3]/text()').extract_first()
            #Pages = Pages.strip()
            if Pages:
                Pages = Pages.split(" ")[0]
            itm['Pages'] = Pages
            #print(Pages)
        except:
            print("Error Pages")
        
        try:
            publish_details = selector.xpath('//*[@id="details"]/div[2]/text()').extract_first()
            publish_details = publish_details.strip()
            #publish_details = publish_details.split("by")
            date, Publication = publish_details.split("by")
            #date = publish_details[0]
            #publication = publish_details[1]
            date = date.split(" ")[1:]
            #remove unwated arrays : Alternatively it can also be done like  date = date.split(" ")[7:10]
            trim_date = [X for X in date if X != ""]
            itm['Published_Date'] = trim_date
            #print(trim_date)
            
            itm['Publication'] = Publication
            #print(Publication)
        except:
            print("Error Publication")
    
        try:
            ISBN = selector.xpath('//*[@id="bookDataBox"]/div[2]/div[2]/text()').extract_first()    
            ISBN = ISBN.strip()
            itm['ISBN'] = ISBN
            #print(ISBN)           
        except:
            print("Error ISBN")
        
        try:
            ISBN13 = selector.xpath('//*[@id="bookDataBox"]/div[2]/div[2]/span/span/text()').extract_first()    
            ISBN13 = ISBN13.strip()
            itm['ISBN13'] = ISBN13
        except:
            print("Error ISBN13")
        yield itm

    
