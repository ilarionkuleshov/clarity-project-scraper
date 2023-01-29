from scrapy.downloadermiddlewares.retry import get_retry_request


class CustomRetryMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        middleware.max_retries = crawler.settings.getint("MAX_RETRIES")
        return middleware

    def process_response(self, request, response, spider):
        retry_conditions = [
            len(response.xpath("//a[contains(@href, 'http://com.clarityapp.pro/landing?utm_source=clarity&utm_medium=organic&utm_campaign=blk&utm_content=bb')]")) > 0
        ]
        if any(retry_conditions):
            retry_request = get_retry_request(
                request,
                reason="BLOCKED response",
                spider=spider,
                max_retry_times=self.max_retries,
                priority_adjust=0,
            )
            if retry_request:
                retry_request.meta["close_cached_connections"] = True
                return retry_request
            else:
                raise Exception(f"received BLOCKED responses {self.max_retries + 1} times")
        return response
