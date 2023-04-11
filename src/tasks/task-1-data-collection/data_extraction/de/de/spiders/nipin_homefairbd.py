# importing the required libraries
import scrapy
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class PropertySpider(scrapy.Spider):

    '''The name of the spider is 'HomeFairBD' and it is used by Scrapy to 
    identify the spider when running the spider from the command line or when 
    setting up a spider to run automatically in a Scrapy project. The spider 
    will start crawling the website from the start_urls. The variable 
    'website_main_url' is useful when building URLs for subsequent requests 
    during the scraping process.'''
    
    name = 'HomeFairBD'
    start_urls = ["https://homefairbd.com/listing"]
    website_main_url = "https://homefairbd.com/"

    def parse(self, response):

        '''The function parse is defined and it takes two parameters - self and 
        response. self refers to the instance of the DataExtractionSpider class, and
        response represents the response received after making a request to a URL. 
        self.logger.info logs a message that is useful for debugging and tracking 
        the progress of the spider.  'response.url' returns the URL of the current 
        page, and the response.xpath() method extracts the href attribute of the 
        first link.The getall() method is used to return all the matching values as
        a list.'''

        self.logger.info('Parse function called on %s', response.url)
        content_url_list = response.xpath('//h5[@class ="mobiletitle"]/a/@href').getall()
        
        
        for url in content_url_list:
            '''The 'for loop' iterates through the content_url_list that contains the
            names of the links present in the response object. 'scrapy.Request'
            creates a new request and this method takes several parameters (URL of the
            page to be requested, the callback function to be called after the 
            response is received, the error callback function to be called in case of 
            an error, and metadata to be passed along with the request). 'yield'
            keyword is used to return the request object to the Scrapy engine'''

            yield scrapy.Request(url=url, callback=self.parse_details_page, errback=self.errback_httpbin)

        next_page = response.xpath('//ul[@class="pagination"]/li/a[@rel="next"]/@href').get()
        '''The above command selects the URL of the next page from the response object of the current page. 
        The value of the href attribute is stored in the next_page variable.'''
        
        if next_page is not None:
            '''This block of code checks the availability of next page. 
            'response.follow()' method is used to send a request to the next page 
            and call the parse() method to parse the response.'''
            
            yield response.follow(url=next_page, callback=self.parse,errback = self.errback_httpbin)


    def parse_details_page(self, response):

        '''The parse_details_page method is responsible for extracting information 
        from the details page of a property and returning a Python dictionary 
        containing the extracted information.'''

        balcony = response.xpath('/html/body/div[5]/div/div[1]/div[1]/div/ul/li[7]//text()').get()
       
        # getting information from the description
        details_list = response.xpath('/html/body/div[5]/div/div[1]/div[1]/p//text()').getall()
       
        # converting details_list into a string
        details_str = ' '.join(details_list)
       
       # searching the presence of various utilities in description using regex
        utilities = re.findall(r'\b(?:electricity|water|generator|lift|parking|drawing|dining|balcony)\b', details_str, re.IGNORECASE)
        utilities.append(balcony)
        
        #extracting the title
        title = response.xpath('/html/body/div[4]/div[2]/div/div/div[2]/h1[1]/a//text()').get()
        
        #checking in title whether the property is for sale or rent 
        rent_or_sale = re.findall(r"\b(sold|sale|rent)\b", title, re.IGNORECASE)
        
        # if sale or rent information not given in title, then it will search sale or rent in the description 
        if not rent_or_sale:
            rent_or_sale = re.findall(r"\b(sold|sale|rent)\b", details_str, re.IGNORECASE)
        
        if rent_or_sale:
            rent_or_sale = rent_or_sale[0]
        if rent_or_sale == 'sold':
            rent_or_sale = 'sale'
        '''The above 'if' statement is used to pick up only the first entry of sale or 
        rent insted of all multiple entries of these words in description. If rent or 
        sale is not found then it will also not return error. Second'if' statement is 
        used to replace the word sold by sale. '''

    
        ''''yield{}' constructs a Python dictionary with the extracted information.''' 
              
        yield {'title': response.xpath('/html/body/div[4]/div[2]/div/div/div[2]/h1[1]/a//text()').getall(), 
        'building_type' : response.xpath('/html/body/div[5]/div/div[1]/div[1]/div/ul/li[1]//text()').getall(),
        'area': response.xpath('/html/body/div[5]/div/div[1]/div[1]/div/ul/li[2]//text()').getall(),
        'num_bed' : response.xpath('/html/body/div[5]/div/div[1]/div[1]/div/ul/li[3]//text()').getall(),
        'num_bath': response.xpath('/html/body/div[5]/div/div[1]/div[1]/div/ul/li[4]//text()').getall(),
        'location': response.xpath('/html/body/div[4]/div[2]/div/div/div[2]/p[2]/a//text()').getall(),
        'price': response.xpath('/html/body/div[4]/div[2]/div/div/div[2]/h1[2]//text()').getall(),
        'amenities': utilities,
        'purpose' : rent_or_sale,
        'listing_url' : response.url}
    

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

            