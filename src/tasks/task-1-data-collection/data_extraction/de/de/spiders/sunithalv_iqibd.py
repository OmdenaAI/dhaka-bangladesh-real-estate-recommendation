import scrapy
from ..items import iqibdPropsItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class PropScrapingSpider(scrapy.Spider):
    name = "iqibd_spider"
    allowed_domains = ["iqibd.com"]
    start_urls = ["https://iqibd.com/properties?type=sale&k=&city_id=&location=&category_id=&bedroom=&bathroom=&floor=&category_id=&min_price=&max_price=",
                  "https://iqibd.com/properties?type=rent&k=&city_id=&location=&category_id=&bedroom=&bathroom=&floor="]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        properties = response.xpath("//div[@class='data-listing mt-2']/div/div[@class='colm10 property-item']")
        # Iterate through each property and get the details for each property
        for property in properties:
            link = property.xpath(".//a[@class='linkdetail']/@href").get()
            yield response.follow(url=link, callback=self.parse_property, errback=self.errback_httpbin)
        # Get the link from the href attribute for pagination
        next_page_url = response.xpath("//a[@aria-label='Next »']").xpath('@href').get()
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse, errback=self.errback_httpbin)

    # To parse the property details page
    def parse_property(self, response):
        item = iqibdPropsItem()
        item['property_link'] = response.request.url
        item['price'] = response.xpath("//p[@class='pricehouse']/text()").get().encode('utf-8')
        item['location'] = (response.xpath("//p[@class='addresshouse']//text()").getall()[1]).strip()
        # Get property details from the Overview table
        details_table = response.xpath("//table[contains(@class,'table')]//tr")
        for row in details_table:
            if row.xpath("./td[1]/text()").get().strip() == 'Category':
                item['building_type'] = row.xpath("./td[2]/strong/text()").get()
            if row.xpath("./td[1]/text()").get().strip() == 'Property Size':
                item['area'] = row.xpath("./td[2]/strong/text()").get()
            if row.xpath("./td[1]/text()").get().strip() == 'Bedroom':
                item['num_bed_rooms'] = row.xpath("./td[2]/strong/text()").get()
            if row.xpath("./td[1]/text()").get().strip() == 'Bathroom':
                item['num_bath_rooms'] = row.xpath("./td[2]/strong/text()").get()
            if row.xpath("./td[1]/text()").get().strip() == 'Floor':
                item['floor'] = row.xpath("./td[2]/strong/text()").get()

        # Get property details from the Description
        property_details = response.xpath("//*[contains(@class,'list-unstyled')]")
        if property_details:
            for details in property_details:
                detail_key = details.xpath('./strong/text()').get().split(':')[0].strip()
                detail_value = details.xpath('./span/text()').get().strip()
                if detail_key == 'Property Size':
                    item['area'] = detail_value
                elif detail_key == 'Land Size' or detail_key == 'Land Area':
                    item['land_size'] = detail_value
                elif detail_key == 'Bedrooms':
                    item['num_bed_rooms'] = detail_value
                elif detail_key == 'Bathrooms':
                    item['num_bath_rooms'] = detail_value
                elif detail_key == 'Garage':
                    item['garage'] = detail_value
                elif detail_key == 'Year Built':
                    item['year_built'] = detail_value
                elif detail_key == 'Property Status':
                    item['status'] = detail_value
                elif 'Balcony' in detail_key:
                    item['num_balcony'] = detail_value
                elif detail_key == 'Interior':
                    item['interior'] = detail_value
                elif detail_key == 'Floor':
                    item['floor'] = detail_value
                elif detail_key == 'Unit':
                    item['unit'] = detail_value
                elif detail_key == 'Servant Room':
                    item['servant_room'] = detail_value
        else:
            # In some details pages the details are present inside a single <p> tag
            property_details = response.xpath("(//div[@class='row'])[5]/div/p//text()").getall()
            if property_details:
                for details in property_details:
                    if len(details.split(':')) == 2:
                        detail_key = details.split(':')[0].strip()
                        detail_value = details.split(':')[1].strip()
                        if detail_key == 'Property Size':
                            item['area'] = detail_value
                        elif detail_key == 'Land Size' or detail_key == 'Land Area':
                            item['land_size'] = detail_value
                        elif detail_key == 'Bedrooms':
                            item['num_bed_rooms'] = detail_value
                        elif detail_key == 'Bathrooms':
                            item['num_bath_rooms'] = detail_value
                        elif detail_key == 'Garage':
                            item['garage'] = detail_value
                        elif detail_key == 'Year Built':
                            item['year_built'] = detail_value
                        elif detail_key == 'Property Status':
                            item['status'] = detail_value
                        elif 'Balcony' in detail_key:
                            item['num_balcony'] = detail_value
                        elif detail_key == 'Interior':
                            item['interior'] = detail_value
                        elif detail_key == 'Floor':
                            item['floor'] = detail_value
                        elif detail_key == 'Unit':
                            item['unit'] = detail_value
                        elif detail_key == 'Servant Room':
                            item['servant_room'] = detail_value

        # Get list of amenities and set to Y if present
        features = response.xpath("(//div[@class='row'])[6]//p//text()").getall()
        for feature in features:
            feature_val = feature.strip()
            if feature_val == 'Wifi':
                item['wifi'] = 'Y'
            elif feature_val == 'Parking':
                item['parking'] = 'Y'
            elif feature_val == 'Swimming pool':
                item['swimming_pool'] = 'Y'
            elif feature_val == 'Balcony':
                item['balcony'] = 'Y'
            elif feature_val == 'Garden':
                item['garden'] = 'Y'
            elif feature_val == 'Security':
                item['security'] = 'Y'
            elif feature_val == 'Fitness center':
                item['fitness_center'] = 'Y'
            elif feature_val == 'Air Conditioning':
                item['air_conditioning'] = 'Y'
            elif feature_val == 'Central Heating':
                item['central_heating'] = 'Y'
            elif feature_val == 'Pets Allow':
                item['pets_allow'] = 'Y'
            elif feature_val == 'CCTV Camera':
                item['cctv'] = 'Y'
            elif feature_val == 'Elevator':
                item['elevator'] = 'Y'
            elif feature_val == 'Emergency Stairs':
                item['emergency_stairs'] = 'Y'
            elif feature_val == 'Generator':
                item['generator'] = 'Y'
            elif feature_val == 'Reception':
                item['reception'] = 'Y'
            elif feature_val == 'TV Cable':
                item['tv_cable'] = 'Y'
            elif feature_val == 'Government Gas':
                item['government_gas'] = 'Y'

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