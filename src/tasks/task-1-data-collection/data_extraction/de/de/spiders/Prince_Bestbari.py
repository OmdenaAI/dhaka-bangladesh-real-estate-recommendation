import scrapy 
import requests


class BariScraper(scrapy.Spider):
    name = "Property_Bari"
    
    page_urlAppartment = [f"https://bestbari.com/property-type/apartment/page/{i}"  for i in range(2,20) if requests.get(f"https://bestbari.com/property-type/apartment/page/{i}").status_code == 200]
    page_urlCommercial = [f"https://bestbari.com/property-type/commercial/page/{i}"  for i in range(2,20) if requests.get(f"https://bestbari.com/property-type/commercial/page/{i}").status_code == 200]

    start = ["https://bestbari.com/property-type/apartment/",
                  "https://bestbari.com/property-type/house/",
                  "https://bestbari.com/property-type/commercial/",
                  "https://bestbari.com/property-type/rent/"]

    start_urls = start+page_urlAppartment+page_urlCommercial
                  

    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    print(start_urls)

    def parse_details_page(self):
        page_urlAppartment = [f"https://bestbari.com/property-type/apartment/page/{i}"  for i in range(2,20) if requests.get(f"https://bestbari.com/property-type/apartment/page/{i}").status_code == 200] 
        page_urlCommercial = [f"https://bestbari.com/property-type/commercial/page/{i}"  for i in range(2,20) if requests.get(f"https://bestbari.com/property-type/commercial/page/{i}").status_code == 200]
        return page_urlAppartment, page_urlCommercial

    def parse(self, response):
        for links in response.css('a.elementor-post__read-more::attr(href)'):
            yield response.follow(links.get(), callback=self.parse_categories,headers={'User-Agent': self.user_agent})


    def parse_categories(self, response):       
            yield{
                "Property_name": response.css('h1.jet-listing-dynamic-field__content::text').get(),
                "Property_Type": response.xpath('//*[@id="overview"]/div/div/div/div[4]/div/div/div/div/strong').get().replace('<strong>', '').replace('</strong>', ''),
                "Bedrooms": response.xpath('//*[@id="overview"]/div/div/div/div[5]/div/div/div/div/strong').get().replace('<strong>', '').replace('</strong>', ''),
                "bathrooms": response.xpath('//*[@id="overview"]/div/div/div/div[6]/div/div/div/div/strong').get().replace('<strong>', '').replace('</strong>', ''),
                "Garages": response.xpath('//*[@id="overview"]/div/div/div/div[7]/div/div/div/div/strong').get().replace('<strong>', '').replace('</strong>', ''),
                "Sq_Ft": response.xpath('//*[@id="overview"]/div/div/div/div[8]/div/div/div/div/strong').get().replace('<strong>', '').replace('</strong>', ''),
                "year_built": response.xpath('//*[@id="overview"]/div/div/div/div[9]/div/div/div/div/strong').get().replace('<strong>', '').replace('</strong>', ''),
                "AD URL" : response.url,
                "features": response.css('div.jet-check-list.jet-check-list--columns-2 div::text').getall()
                }

    




    
             
