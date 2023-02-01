import json
from furl import furl

from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.project import get_project_settings

from rmq.spiders import TaskToMultipleResultsSpider
from rmq.pipelines import ItemProducerPipeline
from rmq.utils import TaskStatusCodes
from rmq.utils.decorators import rmq_callback, rmq_errback
from rmq.utils import get_import_full_name

from items import FinancesItem


class FinancesSpider(TaskToMultipleResultsSpider):
    name = "finances"
    custom_settings = {
        "ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310},
        "DOWNLOAD_HANDLERS": {
            "http": "utils.handlers.RotatingProxiesDownloadHandler",
            "https": "utils.handlers.RotatingProxiesDownloadHandler"
        },
        "ROTATING_PROXIES_DOWNLOADER_HANDLER_AUTO_CLOSE_CACHED_CONNECTIONS_ENABLED": False,
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": None,
            "middlewares.HttpProxyMiddleware": 543,
            "middlewares.CustomRetryMiddleware": 100,
        }
    }

    def __init__(self):
        super().__init__()
        settings = get_project_settings()
        self.task_queue_name = settings.get("FINANCES_TASKS")
        self.result_queue_name = settings.get("FINANCES_RESULTS")
        self.finances_year = settings.get("FINANCES_YEAR")

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        return Request(
            url=f"https://clarity-project.info/edr/{data['edr']}/finances?current_year={self.finances_year}",
            meta={
                "finances_id": data["id"],
                "delivery_tag": _delivery_tag
            },
            callback=self.parse_finances,
            errback=self.errback,
            dont_filter=True
        )

    @rmq_callback
    def parse_finances(self, response):
        if not self.validate_finances_url(response.url):
            self.inject_status_and_exception_to_task(
                response.meta.get("delivery_tag"),
                TaskStatusCodes.ERROR.value,
                f"NO FINANCIAL REPORTS FOR {self.finances_year} YEAR",
                is_warn=True
            )
            return
        if response.meta.get("exception"):
            self.inject_status_and_exception_to_task(
                response.meta.get("delivery_tag"),
                TaskStatusCodes.ERROR.value,
                response.meta["exception"]
            )
            return
        try:
            row_1012_start, row_1012_end = self.get_finances_periods(response, "1012")
            row_1195_start, row_1195_end = self.get_finances_periods(response, "1195")
            row_1495_start, row_1495_end = self.get_finances_periods(response, "1495")
            row_1595_start, row_1595_end = self.get_finances_periods(response, "1595")
            row_1621_start, row_1621_end = self.get_finances_periods(response, "1621")
            row_1695_start, row_1695_end = self.get_finances_periods(response, "1695")
            row_1900_start, row_1900_end = self.get_finances_periods(response, "1900")
            row_2000_start, row_2000_end = self.get_finances_periods(response, "2000")
            row_2280_start, row_2280_end = self.get_finances_periods(response, "2280")
            row_2350_start, row_2350_end = self.get_finances_periods(response, "2350")
            yield FinancesItem(
                {
                    "id": response.meta.get("finances_id"),
                    "url": response.url,
                    "units": "грн",
                    "row_1012_start": row_1012_start,
                    "row_1012_end": row_1012_end,
                    "row_1195_start": row_1195_start,
                    "row_1195_end": row_1195_end,
                    "row_1495_start": row_1495_start,
                    "row_1495_end": row_1495_end,
                    "row_1595_start": row_1595_start,
                    "row_1595_end": row_1595_end,
                    "row_1621_start": row_1621_start,
                    "row_1621_end": row_1621_end,
                    "row_1695_start": row_1695_start,
                    "row_1695_end": row_1695_end,
                    "row_1900_start": row_1900_start,
                    "row_1900_end": row_1900_end,
                    "row_2000_start": row_2000_start,
                    "row_2000_end": row_2000_end,
                    "row_2280_start": row_2280_start,
                    "row_2280_end": row_2280_end,
                    "row_2350_start": row_2350_start,
                    "row_2350_end": row_2350_end
                }
            )
            self.logger.info(f"Parsed finances: {response.url}")
        except Exception as e:
            self.inject_status_and_exception_to_task(
                response.meta.get("delivery_tag"),
                TaskStatusCodes.ERROR.value,
                str(e)
            )

    def get_finances_periods(self, response, row_code):
        for table in response.xpath("//div[@class='entity-content']/table"):
            row_code_index = self.get_column_index_by_text(table, "Код рядка")
            start_period_index = (
                self.get_column_index_by_text(table, "На початок звітного")
                or self.get_column_index_by_text(table, "За звітний період")
            )
            end_period_index = (
                self.get_column_index_by_text(table, "На кінець звітного")
                or self.get_column_index_by_text(table, "За аналогічний період попереднього року")
            )
            if None in [row_code_index, start_period_index, end_period_index]:
                continue
            start_period = self.get_cell_value_by_code_and_index(
                table, row_code_index, row_code, start_period_index
            )
            end_period = self.get_cell_value_by_code_and_index(
                table, row_code_index, row_code, end_period_index
            )
            if start_period is not None or end_period is not None:
                start_period_units = self.get_table_units(table, start_period_index)
                end_period_units = self.get_table_units(table, end_period_index)
                return [
                    self.format_finances_period(start_period, start_period_units),
                    self.format_finances_period(end_period, end_period_units)
                ]
            else:
                continue
        return [None, None]

    @rmq_errback
    def errback(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            error_message = f"HttpError. URL: {response.url} (status: {response.status})"
        else:
            error_message = f"Failed to reach 200 response after retries. URL: {failure.request.url}"
        self.inject_status_and_exception_to_task(
            failure.request.meta.get("delivery_tag"),
            TaskStatusCodes.ERROR.value,
            error_message
        )

    def inject_status_and_exception_to_task(self, delivery_tag, status, exception=None, is_warn=False):
        self.processing_tasks.set_status(delivery_tag, status)
        if exception:
            if is_warn:
                self.logger.warn(exception)
            else:
                self.logger.error(exception)
            self.processing_tasks.set_exception(delivery_tag, exception)

    def validate_finances_url(self, url):
        furl_obj = furl(url)
        return (
            "current_year" in furl_obj.args
            and furl_obj.args["current_year"] == self.finances_year
        )

    @staticmethod
    def get_column_index_by_text(table, text):
        column_index = table.xpath(
            "count(thead/tr/th[contains(text(), $text)]/preceding-sibling::th)",
            text=text
        ).get()
        if column_index is not None and column_index != "0.0":
            return int(float(column_index)) + 1
        return None

    @staticmethod
    def get_cell_value_by_code_and_index(table, code_index, code, column_index):
        return table.xpath(
            "tbody/tr[td[$code_index and text()=$code]]/td[$column_index]/text()",
            code_index=code_index,
            code=code,
            column_index=column_index
        ).get()

    @staticmethod
    def format_finances_period(finances_period, units):
        try:
            period_value = float(finances_period.strip().replace(" ", ""))
        except:
            period_value = None
        if period_value is not None and units is not None:
            if units == "грн":
                return period_value
            elif units == "тис. грн":
                return 1000 * period_value
            else:
                raise Exception(f"Unsupported units: {units}")
        return None

    @staticmethod
    def get_table_units(table, column_index):
        units = table.xpath(
            "thead/tr/th[$index]/span[@class='nobr']/text()",
            index=column_index
        ).get(default="").strip()
        return units if units else None
