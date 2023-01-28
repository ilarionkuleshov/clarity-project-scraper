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
        "ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310}
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
                f"NO FINANCIAL REPORTS FOR {self.finances_year} YEAR"
            )
            return
        # TODO page parsing

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

    def inject_status_and_exception_to_task(self, delivery_tag, status, exception=None):
        self.processing_tasks.set_status(delivery_tag, status)
        if exception:
            self.logger.error(exception)
            self.processing_tasks.set_exception(delivery_tag, exception)

    def validate_finances_url(self, url):
        furl_obj = furl(url)
        return (
            "current_year" in furl_obj.args
            and furl_obj.args["current_year"] == self.finances_year
        )
