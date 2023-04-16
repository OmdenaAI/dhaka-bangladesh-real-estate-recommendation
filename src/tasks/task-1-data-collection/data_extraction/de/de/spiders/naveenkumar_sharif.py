import scrapy
from numpy import unicode

from ..items import SharifItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class DataExtractionSpider(scrapy.Spider):
    name = "naveenkumar_sharif"
    start_urls = ["https://sharif.com.bd/rent"]
    website_main_url = "https://sharif.com.bd/"

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        url_context_names = response.css("div.hot-page2-alp-con a::attr(href)").getall()
        url_properties = [url_context_names[i] for i in range(0, len(url_context_names)) if i % 2 == 0]
        current_url_list = [self.website_main_url + context_name for context_name in url_properties]

        for url in current_url_list:
            request = scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin,
                                     cb_kwargs=dict(property_url=url))
            yield request


        next_page = response.xpath('//div/ul/li/a[contains(@rel, "next")]').xpath('@href').get()
        yield response.follow(url=next_page, callback=self.parse, errback=self.errback_httpbin)


    def parse_details_page(self, response, property_url):

        item = SharifItem()
        description = response.css("div.d-flex.property-overview-data p::text").get()
        description = str(description).strip()
        item["description"] = description

        overview = response.css("li.property-overview-item strong::text").getall()
        input_overview = response.css("ul.list-unstyled.flex-fill li::text").getall()
        input_overview = [ele.strip() for ele in input_overview if ele.strip() != ""]

        for i in range(0, len(input_overview)):
            new_id = "_".join(input_overview[i].split(" "))
            item[(new_id).lower()] = overview[i]

        price = response.css("li.item-price.item-price-text.price-single-listing-text::text").get()
        price = str(price).strip()
        item["price"] = price

        features = response.css("ul.list-unstyled.clearfix li a::text").getall()
        features = [str(ele).strip() for ele in features]
        item["amenities"] = features

        title = response.css("div.page-title h1::text").get()
        item["title"] = title

        address = response.css("div.block-title-wrap.d-flex.justify-content-between.align-items-center h2 span::text")[0].get()
        address = address.split(",")
        address = [ele.strip() for ele in address if ele.strip() != ""]
        item["address"] = ",".join(address)

        item["property_url"] = property_url
        item["property_type"] = "Rent"

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
