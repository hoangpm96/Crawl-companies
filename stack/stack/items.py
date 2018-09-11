from scrapy.item import Item, Field


class StackItem(Item):
    name = Field()
    address = Field()
    agent = Field()
    phone = Field()
    href_ = Field()