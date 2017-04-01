from scrapy.spiders import Spider
#from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
#from test.items import TestItem
import json
import csv, sys

import scrapy
import threading


#from barnes_and_nobles_crawl.items import BarnesAndNoblesCrawlItem

class BarnesAndNoblesCrawler(Spider) :
    name = "barnes_and_nobles_crawl"
    allowed_domains = ["barnesandnoble.com"]
    start_urls = ["http://www.barnesandnoble.com/s/"]
    site_url = "http://www.barnesandnoble.com"
    prefix = "C:\\Users\\Pradeep Kashyap\\Desktop\\CS838-Data Science\\CS838-Data-Science\\goodreads_crawl\\"

    #map to give months names from numbers
    date_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
                7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
    #variable to keep track of how many book information we've successfully scraped.
    tuple_count = 0
    
    def parse(self, response):
        file = open("booknames.txt", "r")
        line = file.readline()
        #Read all the book names and fetch the same books from barnes and nobles (half match and half non matches)
        while line != "" and self.tuple_count < 7000:
            # File format is 'bookname@authornames' in each line
            bookname,author = line.split('@')
            line = file.readline()
            request = scrapy.Request(self.site_url+ "/s/" + bookname+"/_/N-8q8", callback=self.parse_booklink)
            #pass the bookname and author to search and match from barnes and nobles
            request.meta['bookname'] = bookname
            request.meta['author'] = author
            yield request

    def parse_booklink(self, response):
        bookname = response.meta['bookname'].strip()
        author = response.meta['author'].strip()
        #Author names might be differently used in different sites, E.g. J.K. Rowling and J. K. Rowling.
        #It is hard to see the difference, but there is a space between J. and K. which mekes authors not matching.
        #Thus truncating all the spaces
        author = "".join(author.split()).strip()
        selector = Selector(response)

        # In the searched page, there can be books from many authors (serach results might give related books), thus
        # gothrough the list to find the first author match 
        authorlist = selector.xpath('//*[@id="gridView"]/li/ul[1]//li/div[2]/span/a/text()').extract()    
        authorlist = ["".join(X.split()).strip() for X in authorlist]
        urllist = selector.xpath('//*[@id="gridView"]/li/ul[1]//li/div[2]/p/a/@href').extract() 
        for i in range(0, len(authorlist)):
            if authorlist[i] == author:
                request = scrapy.Request(self.site_url + urllist[i], callback=self.parse_bookinfo)
                request.meta['bookname'] = bookname
                request.meta['author'] = author
                yield request
                break

    #parse the actual book's page for information such as author name, publisher, published date etc.        
    def parse_bookinfo(self, response):
        selector = Selector(response)
        bookname = response.meta['bookname'].strip()
        author = response.meta['author'].strip()

        #Verify if the book name is same or not.
        #item is the tuyple that is populated from this list
        itm = {}
        
        #if exception is hit in parsing any of the below information, then don't include this tuple in the result
        #just ignore it and return. The variable tuple_count is used to generate exactly 7000 tuples. I.e. We populate
        #books' details till tuple_count is 7000
        try:
            # Scrape the Title of the book (Not the original name, might have series number in the name)
            ext_bookname = selector.xpath('//*[@id="prodSummary"]/h1/text()').extract_first()
            itm['Original_Title'] = ext_bookname
        except:
            return

        try:
            ext_author = selector.xpath('//*[@id="prodSummary"]/span/a/text()').extract_first();
            itm['Author'] = ext_author
        except:
            return

        try:
            #product details are listed in the below format
            """
            ISBN-13:            9780545139700
            Publisher:          Scholastic, Inc.
            Publication date:   07/07/2009
            Series:             Harry Potter
            Edition description:Reprint
            Pages:              784
            """
            #The left column is the 'prod_detail_name' and right column values are 'prod_detail_value'
            prod_detail_name = selector.xpath('//*[@id="additionalProductInfo"]/dl//dt/text()').extract()
            prod_detail_value = []
            for i in range(0, len(prod_detail_name)):
                value = selector.xpath('//*[@id="additionalProductInfo"]/dl/dd[' + str(i + 1) + ']//text()').extract()
                value = "".join(value).strip()
                print value
                prod_detail_value.append(value)
        
            for i in range(0, len(prod_detail_name)):
                print prod_detail_name[i],":", prod_detail_value[i]
                if prod_detail_name[i] == "ISBN-13:":
                    itm['ISBN-13'] = prod_detail_value[i]
                    
                if prod_detail_name[i] == "Pages:":
                    itm['Pages'] = prod_detail_value[i]
                    
                if prod_detail_name[i] == "Publisher:":
                    itm['Publisher'] = prod_detail_value[i]
                    
                if prod_detail_name[i] == "Publication date:":
                    month, day, year = prod_detail_value[i].split('/')
                    print "Date : ", self.date_map[int(month)], self.daymap(int(day)), year
                    itm['Publication date'] = prod_detail_value[i]        
        except:
            print "Exception macha !"
            return
        
        #As fetching pages are done within threads, use locks for the shared tuple_count variable
        lock = threading.Lock()
        with lock:
            #update the tuple_count, as we've succcessfully parsed the webpage
            self.tuple_count = self.tuple_count + 1
        #yeild the populated tuple
        yield itm
    
    #to match the date format of goodreads, we need to append postfixes st,nd,rd,th after the date.
    def daymap(self, day):
        if day == 1 or day == 21 or day == 31:
            return str(day) + "st"
        
        if day == 2 or day == 22:
            return str(day) + "nd"
        
        if day == 3 or day == 23:
            return str(day) + "rd"
            
        return str(day) + "th"
        
    
    # read 14000 books from good reads. Read 50% of books from 21st centruy best sellers and
    # remaning 50% from 20th century. This make barnes and nobles' book details to match only 50% with good reads.
    # (goodreads details are only containing 21st century best sellers)
    def GenerateBooknamesAndAuthors(self):
        with open(self.prefix + "goodreads.json") as file1:
            data1 = json.load(file1)
        
        with open(self.prefix + "goodreads_20th_century.json") as file2:
            data2 = json.load(file2)
          
        name1 = []
        name2 = []
        for item in data1:
            try:
                name1.append(item['Original_Title'].encode(encoding="utf-8")+ "@" + item['Author'].encode(encoding="utf-8"))
            except:
                try:
                    name1.append(item['Title'].encode(encoding="utf-8") + "@" + item['Author'].encode(encoding="utf-8"))
                except:
                    print("No title for the book", item)
                
        for item in data2:
            try:
                name2.append(item['Original_Title'].encode(encoding="utf-8")+ "@" + item['Author'].encode(encoding="utf-8"))
            except:               
                try:
                    name2.append(item['Title'].encode(encoding="utf-8")+ "@" + item['Author'].encode(encoding="utf-8"))
                except:
                    print("No title for the book", item)
        
        print "name 1 = ", name1[0], "  Name 2 = ", name2[0]
        
        text_file = open("booknames.txt", "w")
        for i in range(0,len(name1)):
            text_file.write(name1[i] + "\n")
            text_file.write(name2[i] + "\n")
        text_file.close()