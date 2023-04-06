import scrapy
from ..items import BpPropertyItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

# command to run the spider
# scrapy crawl bproperty_spider
class BpPropertySpider(scrapy.Spider):
    name = "bproperty_spider"
    start_urls = ["https://www.bproperty.com/en/bangladesh/properties-for-sale/",
                  "https://www.bproperty.com/en/bangladesh/properties-for-rent/"]
    website_main_url = "https://www.bproperty.com/"

    #
    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        url_context_names = response.css("li article div a._287661cb::attr(href)").getall()

        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]

        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

        next_page = response.xpath('//div/ul/li/a[contains(@title, "Next")]').xpath('@href').get()

        if next_page is not None:

            new_url = self.website_main_url+next_page
            yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)


    def parse_details_page(self, response):

        item = BpPropertyItem()
        item['price'] = response.css("span._105b8a67::text").get()
        item['location'] = response.css("div._1f0f1758::text").get()
        item['num_bed_rooms'] = response.css("span.fc2d1086::text").get()
        item['num_bath_rooms'] = response.css("span.fc2d1086::text").get()
        item['area'] = response.css("span.fc2d1086 span::text").get()
        item['building_type'] = response.css("ul._033281ab li span._812aa185::text").get()
        item['purpose'] = response.xpath('//span[contains(@aria-label, "Purpose")]/text()').get()
        item['amenities'] = '##'.join(response.css('div._40544a2f span._005a682a::text').getall())
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