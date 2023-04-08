import scrapy
from ..items import PBazarItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class DataExtractionSpider(scrapy.Spider):
    name = "old_spider"
    start_urls = ["https://pbazaar.com/en/apartment-for-sale"]
    website_main_url = 'https://pbazaar.com/'

    #
    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        url_context_names = response.css('figure a.property-featured-image::attr(href)').getall()

        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]
        print('URL_CONTEXT_NAMES     ',url_context_names, '  current_url_list    ', current_url_list )

        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

        next_page = response.css('ul.pagination li.next-page a::attr(href)').get()
        print('Next page url',next_page)

        if next_page is not None:

            new_url = self.website_main_url + next_page
            yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)


    def parse_details_page(self, response):

        item = PBazarItem()
        item['price_per_sft'] = response.css("div.col-md-3 p.propertyHeader_heading strong::text").get()
        item['location'] = response.css("div.col-md-7 p.propertyHeader_details::text").get()
        item['floor'] = response.css('div.property-amenities:nth-child(1) strong::text').get()
        item['area'] = response.css('div.property-amenities:nth-child(2) strong::text').get()
        item['attach_bathrooms'] = response.css('div.property-amenities:nth-child(3) strong::text').get()
        item['bedrooms'] = response.css('div.property-amenities:nth-child(4) strong::text').get()
        item['common_bathrooms'] = response.css('div.property-amenities:nth-child(5) strong::text').get()
        item['floor_type'] = response.css('div.property-amenities:nth-child(9) strong::text').get()

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
