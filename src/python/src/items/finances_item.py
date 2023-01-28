from scrapy import Field
from rmq.items import RMQItem


class FinancesItem(RMQItem):
    id = Field()
    url = Field()

    row_1012_start = Field()
    row_1012_end = Field()

    row_1195_start = Field()
    row_1195_end = Field()

    row_1495_start = Field()
    row_1495_end = Field()

    row_1595_start = Field()
    row_1595_end = Field()

    row_1621_start = Field()
    row_1621_end = Field()

    row_1695_start = Field()
    row_1695_end = Field()

    row_1900_start = Field()
    row_1900_end = Field()

    row_2000_start = Field()
    row_2000_end = Field()

    row_2280_start = Field()
    row_2280_end = Field()

    row_2350_start = Field()
    row_2350_end = Field()
