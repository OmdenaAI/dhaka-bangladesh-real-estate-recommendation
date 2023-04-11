import scrapy
from ..items import BpPropertyItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class BpPropertySpider(scrapy.Spider):
    name = "bproperty_spider"
    start_urls = ["https://www.bproperty.com/en/bangladesh/properties-for-sale/",
                  "https://www.bproperty.com/en/bangladesh/properties-for-rent/",
                  "https://www.bproperty.com/en/bangladesh/commercial-for-sale/",
                  "https://www.bproperty.com/en/bangladesh/commercial-for-rent/"]


    website_main_url = "https://www.bproperty.com/"

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        url_context_names = response.css("li article div a._287661cb::attr(href)").getall()

        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]
        commercial_type = "commercial" in response.url
        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page,meta={"commercial_type":commercial_type}, errback=self.errback_httpbin)

        next_page = response.xpath('//div/ul/li/a[contains(@title, "Next")]').xpath('@href').get()

        if next_page is not None:

            new_url = self.website_main_url+next_page
            yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)


    def parse_details_page(self, response):

        item = BpPropertyItem()
        item['commercial_type'] = response.request.meta['commercial_type']
        item['property_url'] = response.request.url
        item['property_description'] = response.css("div.daabbebb div div._208d68ae h1.fcca24e0::text").get()
        item['property_overview'] = response.xpath('string(//span[@class="_2a806e1e"])').get()
        item['price'] = response.css("span._105b8a67::text").get()
        item['location'] = response.css("div._1f0f1758::text").get()
        item['num_bed_rooms'] = response.css("span.fc2d1086::text").get()
        item['num_bath_rooms'] = response.css("span.fc2d1086::text").get()
        item['area'] = response.css("span.fc2d1086 span::text").get()
        item['building_type'] = response.css("ul._033281ab li span._812aa185::text").get()
        item['purpose'] = response.xpath('//span[contains(@aria-label, "Purpose")]/text()').get()
        amenities = '##'.join(response.css('div._40544a2f span._005a682a::text').getall())

        if amenities is None or len(amenities.strip()) == 0:
            item['amenities'] = ""

        else:
            amenities_list = amenities.replace("##:", ":").split("##")
            amenities_dict = {}
            for amenity in amenities_list:
                if ':' in amenity:
                    current_amenity = amenity.split(":")
                    amenities_dict[current_amenity[0]] = current_amenity[1]
                else:
                    amenities_dict[amenity] = "yes"

            item['amenities'] = amenities_dict
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

