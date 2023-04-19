import scrapy
from ..items import RentsComBdItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class RentsComBdSpider(scrapy.Spider):
    name = "rents_spider"

    start_urls = [
        "https://rents.com.bd/all-properties/"
    ]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        property_urls = response.xpath('//*[@class="item-title"]/a/@href').getall()

        for url in property_urls:
            yield scrapy.Request(url=url, callback=self.parse_detail_page, errback=self.errback_httpbin)

        next_page = response.xpath(
            '//*[@class="pagination justify-content-center"]/li[@class="page-item"]/a/i[@class="houzez-icon icon-arrow-right-1"]/../@href').get()

        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse, errback=self.errback_httpbin)

    def parse_detail_page(self, response):

        item = RentsComBdItem()

        item['title'] = response.xpath('//*[@id="main-wrap"]/section[2]/div[1]/div/div[2]/div/h1/text()').get()
        item['purpose'] = response.xpath('//*[contains(text(), "Property Purpose")]/../text()').get()
        item['property_type'] = response.xpath('//*[contains(@class, "prop_type")]/text()').get()
        item['size'] = response.xpath('//*[contains(text(), "Property Size")]/../text()').get()
        item['bed'] = response.xpath('//*[text()="Bed: "]/../text()').get()
        item['bath'] = response.xpath('//*[text()="Bath: "]/../text()').get()
        item['balcony'] = response.xpath('//*[contains(text(), "Number of Balcony")]/../text()').get()
        item['parking'] = response.xpath('//*[contains(text(), "Parking")]/../text()').get()
        item['lift'] = response.xpath('//*[contains(text(), "Lift")]/../text()').get()
        item['floor'] = response.xpath('//*[text()="Floor: "]/../text()').get()
        item['unit'] = response.xpath('//*[text()="Unit: "]/../text()').get()
        item['unit_per_floor'] = response.xpath('//*[contains(text(), "Unit Per Floor")]/../text()').get()
        item['total_units'] = response.xpath('//*[contains(text(), "Total Units")]/../text()').get()
        item['price'] = response.xpath('//*[contains(text(), "Price:")]/../text()').get()
        item['service_charge'] = response.xpath('//*[contains(text(), "Service Charge:")]/../text()').get()
        item['year_built'] = response.xpath('//*[contains(text(), "Year Built:")]/../text()').get()
        item['garage_size'] = response.xpath('//*[contains(text(), "Garage Size")]/../text()').get()
        item['interior'] = response.xpath('//*[contains(text(), "Interior")]/../text()').get()
        item['basement'] = response.xpath('//*[contains(text(), "Basement:")]/../text()').get()
        item['building_registration_type'] = response.xpath(
            '//*[contains(text(), "Building Registration Type:")]/../text()').get()
        item['house_rules'] = response.xpath('//*[contains(text(), "House Rules")]/../text()').get()
        item['front_road_size'] = response.xpath('//*[contains(text(), "Front Road Size:")]/../text()').get()
        item['common_area_size'] = response.xpath('//*[contains(text(), "Common Area")]/../text()').get()
        item['nearby_landmark'] = response.xpath('//*[contains(text(), "Nearby Landmark:")]/../text()').get()
        try:
            item['preferred_tenant'] = response.xpath('//*[contains(text(), "Preferred Tenant")]/../text()').get()
        except:
            item['preferred_tenant'] = response.xpath('//*[contains(text(), "Preferred Tennant:")]/../text()').get()

        item['gas'] = response.xpath('//*[contains(text(), "Gas:")]/../text()').get()
        item['servant_room'] = response.xpath('//*[contains(text(), "Servant Room:")]/../text()').get()
        item['servant_washroom'] = response.xpath('//*[contains(text(), "Servant Washroom:")]/../text()').get()
        item['apartment_facing'] = response.xpath('//*[contains(text(), "Apartment Facing:")]/../text()').get()
        item['building_facing'] = response.xpath('//*[contains(text(), "Building Facing")]/../text()').get()
        item['property_url'] = response.url
        item['address'] = response.xpath(
            '//*[@id="property-address-wrap"]/div/div/ul/li[@class = "detail-address"]/span/text()').get() + ", " + response.xpath(
            '//*[@id="property-address-wrap"]/div/div/ul/li[@class = "detail-area"]/span/text()').get() + ", " + response.xpath(
            '//*[@id="property-address-wrap"]/div/div/ul/li[@class = "detail-city"]/span/text()').get()
        item['features'] = response.xpath('//*[@class="houzez-icon icon-check-circle-1 mr-2"]/../a/text()').getall()

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
