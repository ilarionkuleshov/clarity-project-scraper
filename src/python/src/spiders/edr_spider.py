import re
from furl import furl

from scrapy import Request
from scrapy.spiders import SitemapSpider

from items import EdrItem
from pipelines import EdrDBPipeline
from rmq.utils import get_import_full_name


class EdrSpider(SitemapSpider):
    name = "edr"
    custom_settings = {
        "ITEM_PIPELINES": {
            get_import_full_name(EdrDBPipeline): 300
        }
    }

    def start_requests(self):
        yield Request(
            url="https://clarity-project.info/sitemap.xml",
            callback=self.parse_base_sitemap
        )

    def parse_base_sitemap(self, response):
        urls = re.findall(r"<loc>(.*?)</loc>", response.text)
        for url in urls:
            yield Request(
                url=url,
                callback=self.parse_sitemap
            )

    def parse_sitemap(self, response):
        body = str(self._get_sitemap_body(response))
        urls = re.findall(r"<loc>(.*?)</loc>", body)
        for url in urls:
            edr = self.get_edr_from_url(url)
            if edr:
                self.logger.info(f"Parsed new edr: {edr}")
                yield EdrItem({"edr": edr})

    @staticmethod
    def get_edr_from_url(url):
        furl_obj = furl(url)
        url_segments = furl_obj.path.segments
        if (
            len(url_segments) == 2
            and url_segments[0] == "edr"
            and url_segments[1].isdigit()
        ):
            return url_segments[1].strip()
        else:
            return None
