from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from CS_TM_Parse import settings
from CS_TM_Parse.spiders.CSMONEY import CsmoneySpider
from time import sleep
import sys

if __name__ == '__main__':
    # # Settings for loggs
    #logging.basicConfig(format=f'[%(levelname)s]  %(asctime)s --> %(message)s\n%(filename)s:%(lineno)d')

    # Starting the crawl
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    while True:
        process = CrawlerProcess(crawler_settings)
        process.crawl(CsmoneySpider)
        # Shit that prevents crash in the 2 loop
        if "twisted.internet.reactor" in sys.modules:
            del sys.modules["twisted.internet.reactor"]
        process.start()
        sleep(150)

