import scrapy
import json
from ..items import SteamItem
from scrapy import Selector
from scrapy.loader import ItemLoader

base_url = "https://store.steampowered.com/search/results/?query&start={}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1"
class BestSellingSpider(scrapy.Spider):
    name = 'best_selling'
    #allowed_domains = ['store.steampowered.com/']
    start_urls = [base_url.format(0)]




    def parse(self, response):
        resp_dict = json.loads(response.body)
        html = resp_dict.get('results_html')
        fi = Selector(text=html)

        games = fi.xpath("//body/a")
        for game in games:
            loader = ItemLoader(item=SteamItem(), selector=game, response=response)
            loader.add_xpath("game_url", ".//@href")
            loader.add_xpath("img_url", ".//div[@class = 'col search_capsule']/img/@src")
            loader.add_xpath("game_name", ".//span[@class = 'title']/text()")
            loader.add_xpath("release_date", ".//div[@class = 'col search_released responsive_secondrow']/text()")
            loader.add_xpath("platforms", ".//span[contains(@class, 'platform_img') or @class = 'vr_supported' or @class = 'vr_required']/@class")
            loader.add_xpath("rating", ".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html")

            yield loader.load_item()
        count = 22109
        increment = resp_dict.get('start')
        if increment <= count:
            next_url = base_url.format(increment+50)
            yield scrapy.Request(next_url, callback=self.parse)








