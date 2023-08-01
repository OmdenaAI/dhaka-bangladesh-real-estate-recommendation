import scrapy
from ..items import PropertysalebdItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class PropertySalebdSpider(scrapy.Spider):
    name = "propertySalebd_spider"
    start_urls = [
        'https://www.propertysalebd.com/listing-search?type=sale&city-id=&area-id=&property-type=&property-id=',
        'https://www.propertysalebd.com/listing-search?type=rent&city-id=&area-id=&property-type=&property-id='
    ]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        property_urls = response.xpath(
            '//*[@id="ct-js-wrapper"]/section/div/div/div/div[2]/div[6]/div/div/div/a/@href').getall()

        for url in property_urls:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

        next_page = response.xpath(
            '//*[@id="ct-js-wrapper"]/section/div/div/div/div[2]/div/div/div/ul/li/a[@rel = "next"]/@href').get()

        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse, errback=self.errback_httpbin)

    def parse_details_page(self, response):

        item = PropertysalebdItem()

        item['title'] = response.xpath('//*[@id="ct-js-wrapper"]/div[3]/div/div/div[1]/h1/text()').get()
        item['property_name'] = response.xpath('//*[contains(text(), "Property Name")]/../../td[2]/text()').get()
        item['property_type'] = response.xpath('//*[contains(text(), "Property Type")]/../../td[2]/text()').get()
        item['property_for'] = response.xpath('//*[contains(text(), "Property For")]/../../td[2]/text()').get()
        item['location'] = response.xpath('//*[contains(text(), "Location")]/../../td[2]/text()').get()
        item['address'] = response.xpath('//*[contains(text(), "Address")]/../../td[2]/text()').get()
        item['construction_status'] = response.xpath(
            '//*[contains(text(), "Construction Status")]/../../td[2]/text()').get()
        item['property_size'] = response.xpath('//*[contains(text(), "Property Size")]/../../td[2]/text()').get()
        item['price_per_sqft_or_katha_or_dcml'] = response.xpath(
            '//*[contains(text(), "Price Per")]/../../td[2]/text()').get()
        item['monthly_rent'] = response.xpath('//*[contains(text(), "Monthly Rent")]/../../td[2]/text()').get()
        item['total_price'] = response.xpath('//*[contains(text(), "Total Price")]/../../td[2]/text()').get()
        item['deposit'] = response.xpath('//*[contains(text(), "Deposit")]/../../td[2]/text()').get()
        item['transaction_type'] = response.xpath('//*[contains(text(), "Transaction Type")]/../../td[2]/text()').get()
        item['bedroom'] = response.xpath('//*[contains(text(), "Bed Room")]/../../td[2]/text()').get()
        item['balconies'] = response.xpath('//*[contains(text(), "Balconies")]/../../td[2]/text()').get()
        item['bathroom'] = response.xpath('//*[contains(text(), "Bath Room")]/../../td[2]/text()').get()
        item['floor_number'] = response.xpath('//*[contains(text(), "Floor Number")]/../../td[2]/text()').get()
        item['garages'] = response.xpath('//*[contains(text(), "Garages")]/../../td[2]/text()').get()
        item['total_floor'] = response.xpath('//*[contains(text(), "Total Floor")]/../../td[2]/text()').get()
        item['furnishing'] = response.xpath('//*[contains(text(), "Furnishing")]/../../td[2]/text()').get()
        item['facing'] = response.xpath('//*[contains(text(), "Facing")]/../../td[2]/text()').get()
        item['land_area'] = response.xpath('//*[contains(text(), "Land Area")]/../../td[2]/text()').get()
        item['handover_date'] = response.xpath('//*[contains(text(), "Handover Date")]/../../td[2]/text()').get()
        item['available_from'] = response.xpath('//*[contains(text(), "Available From")]/../../td[2]/text()').get()
        item['amenities'] = response.xpath(
            '//*[@id="ct-js-wrapper"]/main/div/div/div[1]/div[4]/div/ul/li/span/text()').getall()
        item['facilities_nearby'] = response.xpath(
            '//*[@id="ct-js-wrapper"]/main/div/div/div[1]/div/div/div/h3/text()').getall()
        item['description'] = response.xpath(
            '//*[@id="ct-js-wrapper"]/main/div/div/div[1]/div[3]/p/text()').get().encode("utf-8")
        item['property_url'] = response.url

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