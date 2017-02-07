from scrapy.spiders import Spider
#from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
#from test.items import TestItem
import scrapy
from goodreads_crawl.items import GoodreadsCrawlItem

class GoodreadsScrawler(Spider) :
    name = "goodreads_crawl"
    allowed_domains = ["goodreads.com"]
    #Comprehension to list all the pages that we want
    start_urls = [("https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page=" + str(i)) for i in range(1,2)]
    site_url = "https://www.goodreads.com"
    
    def parse(self, response):
        hxs = Selector(response)
        rows = hxs.xpath("//tr//td/a/@href")
        
        items = [] # A collection of items from all the webpages (basically an item is information about a book)
        
        for row in rows:
            book_url = self.site_url +  row.extract()
            #print(book_url)
            request = scrapy.Request(book_url, callback=self.parse_bookinfo)
            request.meta['items'] = items
            yield request
            #break
        #print("\n\n\nDONE WITH THE PROGRAM\n\n\n")

    def parse_bookinfo(self, response):
        selector = Selector(response)
        items = response.meta['items']
        # An Item from this page
        itm = GoodreadsCrawlItem()
        # Scrape the Title of the book (Not the original name, might have series number in the name)
        Title = "" + selector.xpath('//h1[@class="bookTitle"]/text()').extract_first()
        brackets = selector.xpath('//a[@class="greyText"]/text()').extract_first()
        Title = Title.strip()
        if brackets:
            brackets = brackets.strip()
            Title = Title + " " + brackets
        itm['Title'] = Title
        #print(Title)
        
        # Get the original Title of the book
        Original_Title = selector.xpath('//*[@id="bookDataBox"]/div[1]/div[2]/text()').extract_first()
        Original_Title = Original_Title.strip()
        itm['Original_Title'] = Original_Title
        #print(Title)
       
        
        # Get the name of the author
        Author = selector.xpath('//*[@id="bookAuthors"]/span[2]/a[1]/span/text()').extract_first()
        Author = Author.strip();
        itm['Author'] = Author
        #print(Author)
        
        Edition_Language = selector.xpath('//*[@id="bookDataBox"]/div[3]/div[2]/text()').extract_first()
        Edition_Language = Edition_Language.strip()
        itm['Edition_Language'] = Edition_Language
        #print(Edition_Language) 
        
        
        Average_Rating = selector.xpath('//*[@id="bookMeta"]/span[3]/span/text()').extract_first()
        Average_Rating = Average_Rating.strip()
        itm['Average_Rating'] = Average_Rating
        #print(Average_Rating)
        
        Ratings = selector.xpath('//*[@id="bookMeta"]/a[2]/span/text()').extract_first()
        Ratings = Ratings.strip()
        Ratings = Ratings.split(" ")[0]
        itm['Ratings'] = Ratings
        #print(Ratings)
        
        Reviews = selector.xpath('//*[@id="bookMeta"]/a[3]/span/span/text()').extract_first()
        Reviews = Reviews.strip()
        #Reviews = Reviews.split(" ")[0]
        itm['Reviews'] = Reviews
        #print(Reviews)
        
        #<a class="actionLinkLite bookPageGenreLink" href="/genres/fantasy">Fantasy</a>
        Genres = selector.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()').extract()
        itm['Genres'] = Genres
        #print(Genres)
        
        Edition = selector.xpath('//*[@id="bookDataBox"]/div[3]/div[2]/text()').extract_first()
        Edition = Edition.strip()
        #Reviews = Reviews.split(" ")[0]
        itm['Edition'] = Edition
        #print(Edition)
        
        
        Pages = selector.xpath('//*[@id="details"]/div[1]/span[3]/text()').extract_first()
        #Pages = Pages.strip()
        if Pages:
            Pages = Pages.split(" ")[0]
        itm['Pages'] = Pages
        #print(Pages)
        
        
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
    
        ISBN = selector.xpath('//*[@id="bookDataBox"]/div[2]/div[2]/text()').extract_first()    
        ISBN = ISBN.strip()
        itm['ISBN'] = ISBN
        #print(ISBN)           
        
        
        ISBN13 = selector.xpath('//*[@id="bookDataBox"]/div[2]/div[2]/span/span/text()').extract_first()    
        ISBN13 = ISBN13.strip()
        itm['ISBN13'] = ISBN13
        #print(ISBN13)

        #print("HERE!\n\n")
        items.append(itm)
        return items
        
    
