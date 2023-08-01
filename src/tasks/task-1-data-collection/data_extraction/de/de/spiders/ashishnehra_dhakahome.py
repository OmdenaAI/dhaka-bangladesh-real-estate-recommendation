import scrapy
from ..items import ashSpiderItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class DataExtractionSpider(scrapy.Spider):
    name = "de_spider"
    start_urls = ["https://dhakahome.com/apartment/",
                  "https://dhakahome.com/to-let/",
                  "https://dhakahome.com/serviced-apartment/"]
    website_main_url = "https://dhakahome.com/"

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        url_context_names = response.css("div div div div h2 a::attr(href)").getall()

        for url in url_context_names:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

        next_page = response.xpath('//nav/ul/li/a[contains(@rel, "Next")]').xpath('@href').get()

        if next_page is not None:
            new_url = next_page
            yield response.follow(url=new_url, callback=self.parse, errback=self.errback_httpbin)

    def parse_details_page(self, response):

        item = ashSpiderItem()
        item['location'] = response.xpath('//*[@id="property-address-wrap"]/div/div[2]/ul/li[1]/span/text()').get()

        detail = response.xpath('//*[@id="property-detail-wrap"]/div/div[2]/div/ul//text()').getall()

        for i in range(len(detail)):
            if detail[i] == 'Property Status:':
                item["pstatus"] = detail[i + 2].strip()

        for i in range(len(detail)):
            if detail[i] == 'Price:':
                if item["pstatus"] == "Serviced Apartment(Rent)":
                    item["price"] = detail[i + 2].strip() + detail[i + 3].strip()

                elif (detail[i + 2] == 'Package') or (detail[i + 2].strip()[0] != '৳'):
                    item["price"] = detail[i + 3].strip()
                else:
                    item["price"] = detail[i + 2].strip()

            if detail[i] == 'Property Size:':
                item["area"] = detail[i + 2].strip()
            if detail[i] == 'Bedrooms:':
                item["bedrooms"] = detail[i + 2].strip()
            if detail[i] == 'Bathrooms:':
                item["bathrooms"] = detail[i + 2].strip()
            if detail[i] == 'Garage:':
                item["garage"] = detail[i + 2].strip()
            if detail[i] == 'Property Type:':
                item["ptype"] = detail[i + 2].strip()

        item["url"] = response.url

        amenity = response.xpath('//*[@id="property-features-wrap"]/div/div[2]/ul/li/a//text()')
        data = []
        for selector in amenity:
            data.append(selector.extract())
        print(data)
        item["amenities"] = data

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
