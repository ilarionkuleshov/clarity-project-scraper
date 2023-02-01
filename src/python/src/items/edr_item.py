from scrapy import Field
from rmq.items import RMQItem


class EdrItem(RMQItem):
    edr = Field()
