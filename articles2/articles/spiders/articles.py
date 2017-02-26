from scrapy.spiders import Spider
from scrapy import Selector
import scrapy
import re

#from articles.items import ArticlesCrawlItem

class ArticleScrawler(Spider) :
    name = "articles"
    allowed_domains = ["goodreads.com"]
    #Comprehension to list all the pages that we want
    start_urls = [("https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page=" + str(i)) for i in range(1,9)]
    site_url = "https://www.goodreads.com"
    
    def parse(self, response):
        hxs = Selector(response)
        rows = hxs.xpath("//tr//td/a/@href")
        
        links = []
        for row in rows:
            book_url = self.site_url +  row.extract()
            links.append(book_url)
            #print(book_url)
        
        for link in links:
            request = scrapy.Request(link, callback=self.parse_bookinfo)
            yield request
            #break

  
    def insert_text(self, text, index, string):
        #print("Text : ", text)
        #print("Index : ", index)
        #print("String : ", string)
        string = string[:index] + text + string[index:]
        return string

    def parse_bookinfo(self, response):
        selector = Selector(response)
        #items = response.meta['items']
        # An Item from this page
        
        itm = {}
        # Scrape the Title of the book (Not the original name, might have series number in the name)
        try :
            Title = selector.xpath('//*[@id="bookTitle"]/text()').extract_first()
            Title = Title.strip()
            itm['Title'] = Title 
            print(Title)
        except:
            print("Error Title")
             
        Character = ""
        #try:
            
        details = selector.xpath('//*[@id="bookDataBox"]//div[@class="clearFloats"]')
        for detail in details:
            # //*[@id="bookDataBox"]/div[1]/div[1]
            dtype = detail.xpath('div[1]/text()').extract_first()
            #print "Dtype = ", dtype
            if dtype == "Characters":
                Character = detail.xpath('div[2]/a/text()').extract_first().strip()
                print("Character = ", Character)
            
        #except:
        #    print("Error Character")

        try:
            # Get the name of the author
            Author = selector.xpath('//*[@id="bookAuthors"]/span[2]/a[1]/span/text()').extract_first()
            Author = Author.strip();
            print "Author = ", Author
        except:
            print("Error Author")
        
        Review = selector.xpath('//div[@class="reviewText stacked"]/span//text()').extract();
        #print(len(Review))
        
        #Review = [item for item in Review if isinstance(item, unicode)]
        #print(len(Review))
        Review = [item.strip() for item in Review if len(item.strip()) != 0]
        #print(len(Review))
        output = ' '.join(Review)
        
      
        #string = "hellow (world) this"
        
        #NEGATIVES, AUTHOR
        
        first = output.find(Author)
        if first != -1:
            output = self.insert_text("<---A>", first, output)
            output = self.insert_text("</---A>", first + 6 + len(Author), output)
        else:
            first_name = Author.split(' ')[0].strip()
            first = output.find(first_name)
            if first != -1:
                output = self.insert_text("<---A>", first, output)
                output = self.insert_text("</---A>", first + 6 + len(first_name), output)
            else:
                output = output + "<---A>" + Author + "</---A>"

        
        # If some mean author wants to talk about himself throughout the book, ufff ! then, tag other occurance of author name
        if Author == Character:
            first = output.find(Character, output.find("<---A>"+Author) + len(Author) + 13)
        else:
            first = output.find(Character)

        if len(Character) != 0:
            if first != -1:
                output = self.insert_text("<---C>", first, output)
                output = self.insert_text("</---C>", first + 6 + len(Character), output)
            else:
                first_name = Character.split(' ')[0].strip()
                if Author == Character:
                    first = output.find(Character, output.find("<---C>" + first_name) + len(first_name) + 13)
                else:
                    first = output.find(first_name)
                if first != -1:
                    output = self.insert_text("<---C>", first, output)
                    output = self.insert_text("</---C>", first + 6 + len(first_name), output)
                else: # Worst case, just put the name at the end of the output (unfortunately, there will not be any context here)
                    output = output + "<---C>" + Character + "</---C>"
        else:
            # If, by the curse of holy zeus god, there doesn't exist a character, then put Author name itself as a character name again.
            output = output + "<---C>" + Author + "</---C>" 

        # POSITIVES
        if output.find("<---C>"+Title+"</---C>") != -1:
            index = output.find(Title, output.find("<---C>"+Title+"</---C>") + len(Title) + 13)
        elif output.find("<---A>"+Title+"</---A>") != -1:
            index = output.find(Title, output.find("<---A>"+Title+"</---A>") + len(Title) + 13)
        else:
            index = output.find(Title)

        if index != -1:
            output = self.insert_text("<+++>", index, output)
            output = self.insert_text("</+++>", index + len(Title) + 5, output)
            # FIND THE SECOND TITLE IN THE COMMENTS
            index2 = output.find(Title, index + len(Title) + 13)
            if index2 != -1:
                output = self.insert_text("<+++>", index2, output)
                output = self.insert_text("</+++>", index2 + len(Title) + 5, output)
            else:
                output = "<+++>" + Title + "</+++>" + output 
        else:
            output = "<+++>" + Title + "</+++>" + output + "<+++>" + Title + "</+++>"

        # NEGATIVES : BRACKETS
        expr = r"(.*)\((.*)\)(.*)"
        group = re.match(expr, output)
        if group:
           bracket_index = output.find("(" + group.group(2) + ")")
           if group.group(2).find("+++") == -1 and group.group(2).find("---") == -1:
               output = self.insert_text("<---B>", bracket_index + 1, output)
               output = self.insert_text("</---B>", bracket_index + 1 + len(group.group(2)) + 6, output)
        else:
                print("No group found")
        
        # NEGATIVES: FULL STOP
        first = output.find(".") + 1
        second = 0
        while True:
            second = output.find(".", first)
            if second != -1:
                substr = output[first:second]
                word_count = len(substr.split(' '))
                if Title.find(substr) == -1 and len(substr) >= 7 and substr.find("+++") == -1 and substr.find("---") == -1 and word_count <= 7 and word_count >= 2:
                    output = self.insert_text("<---F>", first, output)
                    output = self.insert_text("</---F>", second + 6, output)
                    break
            else:
                break
            first = second + 1
            
        #NEGATIVES: COMMAS
        first = output.find(",") + 1
        second = 0
        while True:
            second = output.find(",", first)
            if second != -1:
                substr = output[first:second].strip()
                word_count = len(substr.split(' '))
                if Title.find(substr) == -1 and substr.find("+++") == -1 and substr.find("---") == -1 and substr.find(".") == -1 and word_count <= 7 and word_count >= 2:
                    output = self.insert_text("<---M>", first, output)
                    output = self.insert_text("</---M>", second + 6, output)
                    break
            else:
                break
            first = second + 1
        
        itm['Comments'] = output
        yield itm