import scrapy

from ..items import PropertyFinderBDItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class DataExtractionSpider(scrapy.Spider):
    name = "naveenkumar_propertyfinderbd"
    start_urls = ["https://propertyfinderbd.com/sale-properties", "https://propertyfinderbd.com/rent-properties"]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        url_context_names = response.css("div.col-md-4.mb-3.item a::attr(href)").getall()

        for url in url_context_names:
            request = scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin,
                                     cb_kwargs=dict(main_url=response.url,property_url=url))
            yield request

        next_page = response.xpath('//div/ul/li/a[contains(@rel, "next")]').xpath('@href').get()
        yield response.follow(url=next_page, callback=self.parse, errback=self.errback_httpbin)



    def parse_details_page(self, response, main_url, property_url):

        item = PropertyFinderBDItem()
        title = response.css("div.container h4.title.font::text").get()
        item["property_url"] = property_url
        item["title"] = title.strip()
        if "sale" in main_url.lower():
            item["rent_or_sale"] = "Sale"
        elif "rent" in main_url.lower():
            item["rent_or_sale"] = "Rent"

        rows = response.css("table.table.table-hover tr")
        for row in rows:
            id = row.css("td.font::text")[0].get()
            new_id = "_".join(id.split(" "))
            try:
                output = str(row.css("td.font::text")[1].get())
            except:
                output = str(row.css("td.font span.badge.badge-dark::text").get())
            item[new_id.lower()] = output.strip()

        yield item

    def errback_httpbin(self, failure):
        # logs failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)
