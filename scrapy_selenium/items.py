# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field, Item
from scrapy.loader.processors import MapCompose, TakeFirst, Identity

def remove_char(text):
    text = text.replace('|',',').strip('\n').strip()
    return text



class DribbbleItem(Item):
    name = Field(
        input_processor = MapCompose(remove_char),
        output_processor = Identity()
    )
    location = Field(
        input_processor = MapCompose(str.strip),
        output_processor = Identity()
    )
    
