import scrapy
from ..items import BtibrokeragebdItem





class BtibrokeragebdSpider(scrapy.Spider):
    name= "btibrokeragebd"
    start_urls = ['https://btibrokeragebd.com/properties']
 
    count=2
    total_listing=0
    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        urlsContext = response.xpath('//*[@id="main-wrap"]/section/div/div[2]/div[1]/div[2]/div/div/div/div[2]/h2/a/@href').getall()

        for url in urlsContext:
            yield scrapy.Request(url=url, callback=self.parse_details,meta={'page':response.url})
        
        total_listing = response.xpath('//*[@id="main-wrap"]/section[2]/div/div[2]/div[1]/div[1]/div/div[1]/text()').get()
        if total_listing:
            total_listing=total_listing.replace('Properties', '').strip()
        else:
            total_listing = response.xpath('//*[@id="main-wrap"]/section/div/div[2]/div[1]/div[1]/div/div[1]/strong/text()').get().replace('Results Found', '').strip()
        pages= int(int(total_listing)/12)+1
        count=self.count
        while count<=pages:
            nextPage= f'https://btibrokeragebd.com/search-results/page/{count}/?label%5B0%5D&type%5B0%5D&status%5B0%5D&bedrooms&location%5B0%5D&min-area&max-area'
            yield response.follow(url=nextPage, callback=self.parse)
            count+=1      
     

       


    def parse_details(self, response):
        item = BtibrokeragebdItem()
        item['amenities'] = response.xpath('//*[@id="property-features-wrap"]/div/div[2]/ul/li/a/text()').getall()
        item['price'] = response.xpath('//*[@id="main-wrap"]/section/div[1]/div/div[2]/ul/li/text()').get()
        if item['price']:
            replaceable = ['BDT', ' ', ',','Total']
            for r in replaceable:
                item['price'] = item['price'].replace(r, '')
        item['location'] = response.xpath('//*[@id="main-wrap"]/section/div[1]/div/address/text()').get()
        room_counter=1
        total_bathrooms = 0
        while True:
            counter=str(room_counter)
            room=response.xpath('//*[@id="property-detail-wrap"]/div/div[2]/div/ul/li['+ counter+']/span/text()').get()
            if room:
                if 'bedroom' in room.lower() or 'bedrooms' in room.lower():
                    item['num_bed_rooms'] = response.xpath('//*[@id="property-detail-wrap"]/div/div[2]/div/ul/li['+ counter+']/span/text()').get()
                    if item['num_bed_rooms']: 
                        item['num_bed_rooms']=int(item['num_bed_rooms'].replace('Bedrooms', '').replace('Bedroom', '').strip())
                    else:
                        item['num_bed_rooms'] = 0
                elif 'Bath' in room or 'Baths' in room:
                    attach_bathrooms = response.xpath('//ul[@class="list-3-cols list-unstyled"]/li['+ counter+']/span/text()').get()
                    counter=str(room_counter+1)
                    common_bathrooms=response.xpath('//ul[@class="list-3-cols list-unstyled"]/li['+ counter+']/span/text()').get()
                    
                    if attach_bathrooms or common_bathrooms:
                        try:
                            attach_bathrooms = int(attach_bathrooms.replace('Attached Baths', '').replace('Attached Bath', '').strip())
                        except:
                            attach_bathrooms = 0
                        try:
                            common_bathrooms = int(common_bathrooms.replace('Common Baths', '').replace('Common Bath', '').strip())
                        except:
                            common_bathrooms = 0
                        total_bathrooms = int(attach_bathrooms) + int(common_bathrooms)
                        break
            else:
                break
            room_counter+=1
        if not total_bathrooms:
            total_bathrooms = 0
        item['num_bath_rooms'] = total_bathrooms
        item['area'] = response.xpath('//*[@id="property-detail-wrap"]/div/div[2]/div/ul/li[1]/span/text()').get()
        item['building_type'] = response.xpath('//*[@id="main-wrap"]/section/div[1]/div/div[3]/a[1]/text()').get()
        purpose= response.xpath('//*[@id="main-wrap"]/section/div[1]/div/div[3]/a[2]/text()').get()
        item['purpose']=''
        if purpose:
            purpose = purpose.strip()
            if purpose == 'Buy':
                purpose = 'For Sale'
            else:
                purpose = 'For Rent'
            item['purpose'] = purpose
        item['property_description']= response.xpath('//*[@id="property-description-wrap"]/div/div[2]/p/text()').getall()
        if not item['property_description']:
            item['property_description']= response.xpath('//*[@id="property-description-wrap"]/div/div[2]/div/div/p/text()').getall()
            if not item['property_description']:
                item['property_description']= response.xpath('//*[@id="property-description-wrap"]/div/div/p/text()').getall()
        if item['property_description']:
            item['property_description'] = ' '.join(item['property_description'])
            item['property_description'] = item['property_description'].replace('\r', '').replace('\n', '').replace('\t', '').replace(',', ' ').strip()
        item['property_url'] = response.url
        yield item

        

        

        

   



 