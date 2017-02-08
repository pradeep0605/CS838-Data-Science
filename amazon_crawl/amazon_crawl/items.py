# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field

#import scrapy
#import scrapy.item.Field


class AmazonCrawlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = Field()
    Original_Title = Field()
    Author = Field()
    Edition_Language = Field()
    Average_Rating = Field() # e.g. 4.5 / 5
    Ratings = Field() # Number of Ratings.
    Reviews = Field() # Number of Reviews.
    Genres = Field()
    Edition = Field()
    Pages = Field()
    Published_Date  = Field()
    Publication = Field()
    
    ISBN = Field()
    ISBN13 = Field()
    
    
    