import scrapy
from ..items import RealstateItem
from scrapy.spidermiddlewares.httperror import HttpError
# from items import RealstateItem
from twisted.internet.error import TimeoutError, TCPTimedOutError
from twisted.internet.error import DNSLookupError
 





class Spider2Spider(scrapy.Spider):
    name= "spider2"
    allowed_domains=['www.bdstall.com']
    page_number=2
    start_urls = ['https://www.bdstall.com/apartment/']
 
    

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        urlsContext = response.xpath('/html/body/div[4]/div/div[2]/form/div[4]/a/@href').getall()

        # currentUrlList= [self.mainUrl + context for context in urlsContext]

        for url in urlsContext:
            yield scrapy.Request(url=url, callback=self.parse_details)
        
        
        nextPage = 'https://www.bdstall.com/apartment/'+ str(Spider2Spider.page_number) + '/'



        if Spider2Spider.page_number <=3:
            Spider2Spider.page_number += 1
            yield response.follow (nextPage, callback=self.parse)
        
     

       


    def parse_details(self, response):
        
        item = RealstateItem()
        
        # itt=[]
        # it=response.xpath('//*[@id="main-wrapper"]/section/div/div/div[1]/div[1]/div/div[2]/div[2]/a/text()').getall()
        # for to in it:
        #     to=to.strip()
        #     if to :
        #         itt.append(to)

        # item['PropertyType']= itt

        its=response.xpath('//div[@class="product-desc-feature"]//tr')
        item['Amenities']= [ ]
        key=response.xpath('//div[@class="product-desc-feature"]//tr/th/text()').getall()
        value=response.xpath('//div[@class="product-desc-feature"]//tr/td/text()').getall()

        for i,j in enumerate(key):
            k1={'Updated','Seller Location','Project Type','Drawing','Dining','Veranda','Kitchen','Car Parking','Lift','Generator'}
            if j in k1:
             item['Amenities'].append(value[i+5])
        print(item['Amenities'])
        

            # print(i,j)
            # print(value[i])

        


        

        item['PropertyType']=response.xpath('//div[@class="product-desc-feature"]//tr[4]/td/a/text()').get()
        
        


        item['Size']=response.xpath('//div[@class="product-desc-feature"]//tr[9]/td/text()').get()
        # item['Bathroom']=response.xpath('//*[@id="roomFeats"]/div/div/span[substring(text(),1,8)="Bathroom"]/text()').get()
        item['Bathroom']=response.xpath('//div[@class="product-desc-feature"]//tr/td[substring(text(),3,10)="Bathroom"]/text()').getall()
        
        # it3=response.xpath('//*[@id="main-wrapper"]/section/div/div/div[2]/div/div[1]/div/span/text()').getall()
        # stringVal3 = "For Rent"
        # val= 't '
        item['Status']=response.xpath('//div[@class="product-desc-feature"]//tr[5]/td/text()').get()
        
        item['Location']=response.xpath('//div[@class="product-desc-feature"]//tr[10]/td/text()').get()
        
        itt3=response.xpath('//div[@class="product-desc-feature"]//tr/td/span/text()').get().replace('৳','')
    
        itt3 = itt3.replace(',','').strip()
        item['PricePerMonth']=itt3
        
        item['Bed']=response.xpath('//div[@class="product-desc-feature"]//tr/td[substring(text(),3,5)="Bed"]/text()').getall()       
        


        it=response.xpath('//div[@class="s-top"]/p/text()').getall()
        itt=[]
        for to in it:
            to=to.strip()
            if to:
                itt.append(to)
        item['Description']=itt
        # item['NearByLocation']=response.xpath('//*[@id="nearPlace"]/div/div/span/text()').getall()

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
        

        

   



 