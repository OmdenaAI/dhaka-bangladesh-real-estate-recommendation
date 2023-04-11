import scrapy


class StartSpider(scrapy.Spider):
    name = "bikrisohoj"
    start_urls = ["https://www.bikrisohoj.com/ads/property"]

    def parse(self,response):
        links = response.css("a.myButton::attr(href)")
        for link in links:
            yield scrapy.Request(link.get(),callback = self.parse_data)
            

        next_page = [response.xpath(f"/html/body/div[3]/div/div[1]/nav[2]/ul/li[{i}]/a").attrib['href'] for i in range(0,10)if response.xpath(f"/html/body/div[3]/div/div[1]/nav[2]/ul/li[{i}]/a/text()").get() == 'Next »' ]
        if next_page:
            yield response.follow(next_page[0],callback = self.parse)

       
        
    def parse_data(self,response):
        yield{
            "Name" : response.xpath("/html/body/div[3]/div/div[2]/div[1]/h1/text()").get().encode("utf-8"),
            "Location":response.xpath("/html/body/div[3]/div/div[2]/div[1]/p/span[2]/text()").get(),
            "Description":response.xpath("/html/body/div[3]/div/div[2]/pre/text()").get().encode("utf-8") ,
            "Ad posted time":response.xpath("/html/body/div[3]/div/div[2]/div[1]/p/text()[2]").get(),
            "Price":response.css("span.amount::text").get(),
            "AD URL" : response.url

        }


# name : response.xpath("/html/body/div[3]/div/div[2]/div[1]/h1/text()").get()
#location : response.xpath("/html/body/div[3]/div/div[2]/div[1]/p/span[2]/text()")
# description : response.xpath("/html/body/div[3]/div/div[2]/pre/text()").get() 
# price : response.css("span.amount::text").get()
# ad posted time : response.xpath("/html/body/div[3]/div/div[2]/div[1]/p/text()[2]").get()
# next_page : response.css("a.page-link::attr(href)").get()

# AD URL : response.url

