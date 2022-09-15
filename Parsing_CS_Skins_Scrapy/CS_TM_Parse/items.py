# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CsTmParseItem(scrapy.Item):
    fullName = scrapy.Field()
    quality = scrapy.Field()
    float = scrapy.Field()
    price = scrapy.Field()
    overprice = scrapy.Field()
    assetID = scrapy.Field()
    siteID = scrapy.Field()
    HighDemand = scrapy.Field()
    tradeLock = scrapy.Field()
    link = scrapy.Field()


