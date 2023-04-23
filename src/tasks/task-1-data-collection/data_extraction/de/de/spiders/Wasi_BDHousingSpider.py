import scrapy
from ..items import BdHousingItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class BDHousingSpider(scrapy.Spider):
    name = "BDHousing_spider"
    start_urls = ['https://www.bdhousing.com/homes/listings/Sale/',
                  'https://www.bdhousing.com/homes/listings/Rent'
                  ]


    website_main_url = "https://www.bdhousing.com"

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        # url_context_names = response.xpath('//div[2]/div/div[1]/a/@href').getall()
        url_context_names = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div/div/a/@href').getall()

        current_url_list = [self.website_main_url + context_name for context_name in url_context_names]
        for url in current_url_list:
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin,meta={'page':response.url})

        next_page = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section/div/div[3]/div[2]/div[2]/div/div/ul/li[4]/a/@href').get()
        if not next_page:
            next_page = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section/div/div[3]/div[2]/div[2]/div/div/ul/li[2]/a/@href').get()
        if url_context_names:
            new_url=new_url = self.website_main_url+next_page
            yield response.follow(url=new_url, callback=self.parse,errback = self.errback_httpbin)


    def parse_details_page(self, response):
        page=response.meta['page']
        item = BdHousingItem()
        item['property_url'] = response.url
        item['price'] = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[1]/div[1]/div/div/p[2]/span/text()').get()
        if 'call for' in item['price'].lower():
            item['price'] = None
        elif  item['price']:
            item['price'] = item['price'].replace('BDT','').strip()
        labels = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li/label')

        for label in labels:
            label_text = label.xpath('./text()').get()
            if 'Location' in label_text:
                item['location'] = label.xpath('./following-sibling::span/text()').get()
            elif 'Baths' in label_text:
                item['baths'] = label.xpath('./following-sibling::span/text()').get()
                if item['baths']:
                    item['baths']=item['baths'].strip()
            elif 'Bedroom' in label_text:
                item['bedroom'] = label.xpath('./following-sibling::span/text()').get()
                if item['bedroom']:
                    item['bedroom']=item['bedroom'].strip()
            elif 'Property Size' in label_text:
                item['area'] = label.xpath('./following-sibling::span/text()').get()
                if item['area']:
                    item['area']=item['area'].strip()
            elif 'Balconies' in label_text:
                item['balconies'] = label.xpath('./following-sibling::span/text()').get()
                if item['balconies']:
                    item['balconies']=item['balconies'].strip()
            elif 'Property For' in label_text:
                item['purpose'] = label.xpath('./following-sibling::span/text()').get()
            elif 'Property Type' in label_text:
                item['property_type'] = label.xpath('./following-sibling::span/text()').get()
        total_amenities = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[3]/div/div[2]/div/label/text()').getall()
        item['amenities'] = []
        for amenities in total_amenities:
            if amenities.strip():
                item['amenities'].append(amenities.strip())
       

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