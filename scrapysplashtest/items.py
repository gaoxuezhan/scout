# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class ProductItem(Item):
    collection = 'products'
    
    company = Field()
    code = Field()
    departureTime = Field()
    departureAirport = Field()
    departureCity = Field()
    timeCost = Field()
    type = Field()
    arriveTime = Field()
    arriveAirport = Field()
    arriveCity = Field()
    price = Field()
    updateTime = Field()
    targetDate = Field()
