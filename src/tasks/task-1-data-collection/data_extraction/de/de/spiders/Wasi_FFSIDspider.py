import scrapy
from ..items import FFSIDItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

# scrapy crawl FFSID_spider
class FFSIDSpider(scrapy.Spider):
    name = "FFSID_spider"
    start_urls = ["https://flatforsaleindhaka.com/?ct_ct_status=featured&search-listings=true/"]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        url_context_names = response.xpath('//li/div/div/header/h4/a/@href').getall()

        current_url_list = [context_name for context_name in url_context_names]

        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

        next_page = response.xpath("//li[@id='next-page-link']/a/@href").get()

        if next_page is not None:
            new_url = next_page
            yield response.follow(url=new_url, callback=self.parse, errback=self.errback_httpbin)

    def parse_details_page(self, response):

        item = FFSIDItem()
        item['property_url'] = response.request.url
        item['price'] = response.css("span.listing-price::text").get()
        item['location'] = response.xpath('//div/article/header/p/text()').get()
        spans = response.xpath('//*[@id="main-content"]/div[2]/article/ul[1]/li/span')

        for span in spans:
            span_text = span.xpath('./text()').get()
            if 'Bed' in span_text:
                item['beds'] = span.xpath('./following-sibling::span[1]/text()').get()
            elif 'Bath' in span_text:
                item['baths'] = span.xpath('./following-sibling::span[1]/text()').get()
            elif 'Parking' in span_text:
                item['parking'] = span.xpath('./following-sibling::span[1]/text()').get()
            elif 'Per' in span_text:
                item['price_per_sqft'] = span.xpath('./following-sibling::span[1]/text()').get()
            elif 'Sq Ft' in span_text.strip():
                item['sqft'] = span.xpath('./following-sibling::span[1]/text()').get()
            elif 'ID' in span_text:
                item['pid'] = span.xpath('./following-sibling::span[1]/text()').get()
            elif 'Type' in span_text:
                item['property_type'] = span.xpath('./following-sibling::span[1]/text()').get()

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