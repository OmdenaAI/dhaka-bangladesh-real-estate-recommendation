import scrapy


class ApexPropertySpider(scrapy.Spider):

    name = "apex_property"
    allowed_domains = ['www.apexproperty.com.bd']
    start_urls = ['https://www.apexproperty.com.bd/search?country=227&region=7779071&page=1']

    def parse(self, response):

        # Select the parent div element that contains each property listing
        listings = response.xpath("//*[@class='col-md-6']")

        data = []
        # Extract the title, link, price, and currency of each property listing
        for i, listing in enumerate(listings):
            price = listing.xpath(".//h3[@class='pro__price']//span[2]/text()").get()
            currency = listing.xpath(".//h3[@class='pro__price']//span[1]/text()").get()
            property_size = listing.xpath(".//ul[@class='pro__meta']//li[1]/span/text()").get()
            beds = listing.xpath(".//ul[@class='pro__meta']//li[2]/span/text()").get()

            # Return a dictionary containing the extracted data for each property listing
            data.append({
                'price': price,
                'currency': currency,
                'property_size': property_size,
                'beds': beds
            })

        yield {'data': data}

        # Check if the "Next" button exists
        next_button = response.xpath("//ul[@id='yw0']/li[9]/a")
        if next_button:
            # If the "Next" button exists and it's not the last page, generate the next URL dynamically and make a request to it
            next_page_url = next_button.attrib['href']
            if next_page_url == "javascript: void(0);":
                # If the "Next" button is disabled, we have reached the last page
                yield self.data
            else:
                next_page_num = int(next_page_url.split('=')[-1])
                next_url = f'https://www.apexproperty.com.bd/search?country=227&region=7779071&page={next_page_num}'
                yield scrapy.Request(url=next_url, callback=self.parse)
        else:
            # If the "Next" button does not exist, we have reached the end of the pages
            self.log('No more pages to scrape')
