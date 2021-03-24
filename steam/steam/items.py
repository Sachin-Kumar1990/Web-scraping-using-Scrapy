# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_html(review_summary):
    review_holder = ""
    try:
        review_holder = remove_tags(review_summary)
    except TypeError:
        review_holder = "No reviews"
    return review_holder

    # noinspection PyUnreachableCode
def get_platforms(one_class):
    platforms1 = []
    platform = one_class.split(' ')[-1]
    if platform == "win":
        platforms1.append("Windows")
    if platform == "mac":
        platforms1.append("Apple")
    if platform == "linux":
        platforms1.append("Linux")
    if platform == "music":
        platforms1.append("Music")
    if platform == "vr_required":
        platforms1.append("VR Only")
    if platform == "vr_supported":
        platforms1.append("VR Supported")
    return platforms1


class SteamItem(scrapy.Item):
    game_url = scrapy.Field(output_processor = TakeFirst())
    img_url = scrapy.Field(output_processor = TakeFirst())
    game_name = scrapy.Field(output_processor = TakeFirst())
    release_date = scrapy.Field(output_processor = TakeFirst())
    platforms = scrapy.Field(input_processor = MapCompose(get_platforms))
    rating = scrapy.Field(input_processor = MapCompose(remove_html), output_processor = TakeFirst())

