import logging

from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.utils.project import get_project_settings

from twisted.enterprise import adbapi
from MySQLdb.cursors import DictCursor

from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import insert

from items import EdrItem
from database.models import Finances


class EdrDBPipeline:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.project_settings = get_project_settings()
        self.pending_items = 0

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_idle, signal=signals.spider_idle)
        return o

    def open_spider(self, spider):
        self.db_connection_pool = adbapi.ConnectionPool(
            "MySQLdb",
            host=self.project_settings.get("DB_HOST"),
            port=self.project_settings.getint("DB_PORT"),
            user=self.project_settings.get("DB_USERNAME"),
            passwd=self.project_settings.get("DB_PASSWORD"),
            db=self.project_settings.get("DB_DATABASE"),
            charset="utf8mb4",
            use_unicode=True,
            cursorclass=DictCursor,
            cp_reconnect=True,
            cp_max=1
        )

    def close_spider(self, spider):
        self.db_connection_pool.close()

    def spider_idle(self, spider):
        if self.pending_items > 0:
            raise DontCloseSpider

    def process_item(self, item, spider):
        if isinstance(item, EdrItem):
            d = self.db_connection_pool.runQuery(
                self.compile_and_stringify_statement(
                    insert(Finances).values(item).prefix_with("IGNORE")
                )
            )
            d.addCallback(self.item_stored)
            d.addErrback(self.errback)
            self.pending_items += 1
        else:
            self.logger.warning("Undefined item instance")
        return item

    def item_stored(self, _):
        self.pending_items -= 1

    def errback(self, failure):
        self.logger.error(failure.getErrorMessage())

    @staticmethod
    def compile_and_stringify_statement(stmt):
        return str(
            stmt.compile(
                compile_kwargs={"literal_binds": True},
                dialect=mysql.dialect()
            )
        )
