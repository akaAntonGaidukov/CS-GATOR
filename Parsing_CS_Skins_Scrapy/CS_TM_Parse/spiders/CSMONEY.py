import scrapy
from CS_TM_Parse.items import CsTmParseItem
import logging


class CsmoneySpider(scrapy.Spider):
    # Receiving the names of skins
    skins_list = []
    with open(r"C:\Users\user\Documents\JUPITER\CS_GATOR\Parsing_CS_Skins_Scrapy\CS_TM_Parse\all_skins.txt", "r") as f:
        for readline in f:
            skins_list.append(readline.strip('\n'))

    name = 'CSMONEY'
    allowed_domains = ['cs.money', 'inventories.cs.money']

    start_urls = []
    for skin_name in skins_list:
        start_urls.append(
            f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=35&isStore=true&limit=60&maxPrice=10000&minPrice=1&name={skin_name.replace("| ", "").replace(" ", "%20").replace("(", "%28").replace(")", "%29")}&offset=0&withStack=true')

    def parse(self, response):
        url = response.url
        where_offset = url.find('offset') + 7
        where_withStack = url.find('&withStack')
        offset_new = str(int(url[where_offset:where_withStack]) + 60)
        new_link = url[:where_offset] + offset_new + url[where_withStack:]

        try:
            json_data = response.json()['items']

            # Don't move to the next page if this one is not full
            if len(json_data) == 60:
                yield response.follow(new_link, callback=self.parse)

            for item in json_data:
                # Check is there any trade lock
                try:
                    trade_lock = item['tradeLock']
                    yield CsTmParseItem(fullName=item['fullName'], quality=item['quality'],
                                        float=item['float'],
                                        price=item['price'], overprice=item['overprice'], assetID=item['assetId'],
                                        siteID=item['id'], HighDemand=item['hasHighDemand'],
                                        tradeLock=trade_lock)
                    continue  # If there is a trade lock just continue

                except KeyError:  # means that this item has no trade lock
                    pass

                yield CsTmParseItem(fullName=item['fullName'], quality=item['quality'],
                                    float=item['float'],
                                    price=item['price'], overprice=item['overprice'], assetID=item['assetId'],
                                    siteID=item['id'], HighDemand=item['hasHighDemand'],
                                    tradeLock='None')
        except KeyError:  # means that this page DNE
            pass
