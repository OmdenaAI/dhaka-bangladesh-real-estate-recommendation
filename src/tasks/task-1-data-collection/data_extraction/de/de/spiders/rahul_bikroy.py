import scrapy
from ..items import BikroyItem #BpPropertyItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re
# command to run the spider
# scrapy crawl bproperty_spider
class BikroySpider(scrapy.Spider):
    name = "bikroy"
    start_urls = ["https://bikroy.com/en/ads/dhaka/property"]
    website_main_url = "https://www.bikroy.com/"
    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        url_context_names = response.css("ul.list--3NxGO a.card-link--3ssYv::attr(href)").getall()
        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]
        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)
        for i in range(3, 647):
            new_url = f"https://bikroy.com/en/ads/dhaka/property?page={i}"
            yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)
    def parse_details_page(self, response):
        item = BikroyItem()
        item['commercial_type'] = False
        price=response.css("div.amount--3NTpl::text").get()
        if price:
            item['price'] = price
        for i in range(1,10):
            # info is just the pairs i.e. ["location","dhaka"]
            try:
                info = response.css(f"#app-wrapper > div.container--3Gaei.all > div.main-section--34CB3 > div:nth-child(2) > div.details-section--2ggRy > div.justify-content-flex-start--1Xozy.align-items-normal--vaTgD.flex-wrap-nowrap--3IpfJ.flex-direction-row--27fh1.flex--3fKk1 > div > div.sm-col-12--30zDS.lg-col-8--3483a.block--3v-Ow > div > div.section--PpGYD > div.ad-meta--17Bqm.justify-content-flex-start--1Xozy.align-items-normal--vaTgD.flex-wrap-wrap--2PCx8.flex-direction-row--27fh1.flex--3fKk1 > div:nth-child({i}) > div.word-break--2nyVq::text").getall()
                if re.search(r"[Aa]ddress",info[0]):
                    item['location'] = str(info[1])
                if re.search(r"[Ss]ize",info[0]):
                    item["area"] = info[1]
                if re.search(r"[Bb]ed",info[0]):
                    item["num_bed_rooms"] = info[1]
                if re.search(r"[Bb]ath",info[0]):
                    item["num_bath_rooms"] = info[1]
                if re.search(r"[Ss]tatus",info[0]):
                    item["completion_status"] = info[1]
                if re.search(r"[Ff]acing",info[0]):
                    item["facing"] = info[1]
                if re.search(r"[cC]ommertial",info[1]):
                    item['commercial_type'] = True
                if re.search(r"[Tt]ype",info[0]):
                    item["building_type"] = info[1]
            except:
                break
        item['property_url'] = response.request.url
        property_description = " ".join(response.css('ul > div > p::text').getall())
        if property_description is None or len(property_description) == 0:
            item['property_description'] = ""
        else:
            item['property_description'] = property_description
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
