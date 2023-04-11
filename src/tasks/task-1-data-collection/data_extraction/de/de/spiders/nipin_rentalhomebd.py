'''Importing the necessary libraries'''
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class DataExtractionSpider(scrapy.Spider):

    '''The name of the spider is 'housing_info' and it is used by Scrapy to identify the spider when running the spider 
    from the command line or when setting up a spider to run automatically in a Scrapy project. The spider will start 
    crawling the website from the start_urls. The variable 'website_main_url' is useful when building URLs for subsequent
    requests during the scraping process.'''

    name = "housing_info"
    start_urls = ["http://www.rentalhomebd.com/properties?page=1"]
    website_main_url = "http://www.rentalhomebd.com/"

    
    def parse(self, response):
        '''The function parse is defined and it takes two parameters - self and response. self refers to the instance of the
        DataExtractionSpider class, and response represents the response received after making a request to a URL. self.logger.info 
        logs a message that is useful for debugging and tracking the progress of the spider.  'response.url' returns the URL of the 
        current page, and the response.xpath() method extracts the href attribute of the first link.The getall() method is used 
        to return all the matching values as a list.'''
         
        self.logger.info('Parse function called on %s', response.url)
        next_page_url =response.url
        url_context_names = response.xpath('//*[@id="grid-image"]/a[1]/@href').getall()
        
   
        for url in url_context_names:
            '''The 'for loop' iterates through the url_context_names list that contains the context names of the links present 
            in the response object. If the URL doesn't contain "http", then "http://" prefix is added to the URL. 'scrapy.Request'
            creates a new request and this method takes several parameters (URL of the page to be requested, the callback function 
            to be called after the response is received, the error callback function to be called in case of an error, and 
            metadata to be passed along with the request). 'yield' keyword is used to return the request object to the Scrapy 
            engine'''

            if 'http' not in url:
                url = 'http://'+url
            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin, meta = {'url': next_page_url})


        next_page_url = response.xpath('//ul[@class="pagination"]/li/a[@rel="next"]/@href').get()
        '''The above command selects the URL of the next page from the response object of the current page. 
        The value of the href attribute is stored in the next_page_url variable.'''

        
        if next_page_url is not None:
            '''This block of code checks the availability of next page.The print command is a debugging step that  can help 
            verify that the correct URL is being extracted and followed. response.follow() method is used to send a request to 
            the next page and call the parse() method to parse the response.'''

            print(next_page_url)


            yield response.follow(url=next_page_url, callback=self.parse,errback = self.errback_httpbin, meta = {'url': next_page_url})

    def parse_details_page(self, response):

        '''The parse_details_page method is responsible for extracting information from the details page of a property and 
        returning a Python dictionary containing the extracted information. The details of the property are extraxted from 
        the details page, blank or whitespace elements are removed, and cleaned-up list is stored in the details_cleaned variable.
        'yield{}' constructs a Python dictionary with the extracted information.'''
        
        
        details_list = response.xpath('//*[@id="property-details"]/div[2]/div[2]//text()'.strip()).getall()
        
        
        details_cleaned = []
        for key, item in enumerate(details_list):
            if item:
                details_cleaned.append(item.strip())

           
        yield {'title': response.xpath('//*[@id="property-details"]/nav/div/div[1]/h4//text()').get(), 
        'num_bed' : response.xpath('//*[@id="property-details"]/nav/div/div[1]/p[1]/span[2]//text()').get(),
        'num_bath': response.xpath('//*[@id="property-details"]/nav/div/div[1]/p[1]/span[3]//text()').get(),
        'area': response.xpath('//*[@id="property-details"]/nav/div/div[1]/p[1]/span[1]//text()').get(),
        'amenities' : response.xpath('//*[@id="property-details"]/div[@class="features-box"]/div/div/p/text()').getall(),
        'location' : response.xpath('//*[@id="property-details"]/nav/div/div[1]/p[2]//text()').get(),
        'building_type' : response.xpath('//*[@id="property-details"]/div[1]/div/table/tbody/tr[1]/td[2]//text()').get(),
        'purpose' : response.xpath('//*[@id="property-details"]/div[1]/div/table/tbody/tr[2]/td[2]//text()').get(),
        'price_in_BDT' : response.xpath('//*[@id="property-details"]/nav/div/div[2]/h4/text()').get(),
        'details' : details_cleaned[3:],
        'listing_url': response.url}
        

        
    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

        '''This method in a Scrapy Spider is called when there is an error in processing a request. The method logs the error 
        details using Scrapy's logger and takes the failed request as an argument.'''

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)