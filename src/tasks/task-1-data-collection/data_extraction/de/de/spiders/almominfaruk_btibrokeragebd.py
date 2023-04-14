import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from ..items import BtibrokeragebdItem
from twisted.internet.error import TimeoutError, TCPTimedOutError
from twisted.internet.error import DNSLookupError





class BtibrokeragebdSpider(scrapy.Spider):
    name= "btibrokeragebd"
    start_urls = ['https://btibrokeragebd.com/properties']
 
    

    def parse(self, response):
        urlsContext = response.xpath('//*[@id="main-wrap"]/section[2]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div/a/@href').getall()

        # currentUrlList= [self.mainUrl + context for context in urlsContext]

        for url in urlsContext:
            yield scrapy.Request(url=url, callback=self.parse_details)
        

        count=2
        while True:
            nextPage = response.xpath('//*[@id="main-wrap"]/section[2]/div/div[2]/div[1]/div[3]/nav/ul/li[3]/a/@href').get()
            if nextPage is not None:
                # newUrl =self.mainUrl+nextPage
                yield response.follow(url=nextPage, callback=self.parse)
            else:
                break
        
     

       


    def parse_details(self, response):
        item = ToleterItem()
        itt=[]
        it=response.xpath('//*[@id="main-wrapper"]/section/div/div/div[1]/div[1]/div/div[2]/div[2]/a/text()').getall()
        for to in it:
            to=to.strip()
            if to :
                itt.append(to)

        item['PropertyType']= itt

        it2=response.xpath('//*[@id="roomFeats"]/div/div/span/text()').getall()
        stringVal = "Bathrooms:"
        stringVal2 = "Bedrooms:"
        item['Amenities']= [ x for x in it2 if stringVal not in x and stringVal2 not in x]



        

        # item['Amenities']=response.xpath('//*[@id="roomFeats"]/div/div/span/text()').getall()
        
        item['Bedroom']=response.xpath('//*[@id="roomFeats"]/div/div/span[substring(text(),1,7)="Bedroom"]/text()').get()
        item['Bathroom']=response.xpath('//*[@id="roomFeats"]/div/div/span[substring(text(),1,8)="Bathroom"]/text()').get()
        item['MainFeatures']=response.xpath('//*[@id="mainFeats"]/div/div/span/text()').getall()
        
        it3=response.xpath('//*[@id="main-wrapper"]/section/div/div/div[2]/div/div[1]/div/span/text()').getall()
        stringVal3 = "For Rent"
        val= 't '
        item['Status']=[(x.strip("'Status': ") + val if stringVal3 in x else x.strip("'Status': ")) for x in it3 ]
        
        # item['Floors']=box.response.xpath('//*[@id="mainFeats"]/div/div[3]/span/text()').get().strip("'Floors': ")
        item['PricePerMonth']=response.xpath('//*[@id="main-wrapper"]/section/div/div/div[1]/div[1]/div/h3[2]/text()').get()
        item['Location']=response.xpath('//*[@id="main-wrapper"]/section/div/div/div[1]/div[1]/div/span/text()').get().encode('utf-8')
        item['Description']=response.xpath('//*[@id="clTwo"]/div/p//text()').getall()
        item['NearByLocation']=response.xpath('//*[@id="nearPlace"]/div/div/span/text()').getall()

        item['url']=response.url
        

        yield item

        


def errback_httpbin(self, failure):
    self.logger.error(repr(failure))

    if failure.check(HttpError):
        response = failure.value.response
        self.logger.error ('HttpError occured on %s', response.url)

    elif failure.check(DNSLookupError):
        request= failure.request
        self.logger.error('DNSLookuoError occured on %s', request.url)

    elif failure.check(TimeoutError, TCPTimedOutError):
        request= failure.request
        self.logger.error('TCPTimedOutError occured on %s', request.url)
        

        

   



 