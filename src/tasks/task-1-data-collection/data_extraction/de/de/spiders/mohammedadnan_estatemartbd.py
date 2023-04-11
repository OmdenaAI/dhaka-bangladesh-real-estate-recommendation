import scrapy
#import libraries for using selenium in scrapy
import time
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By


class StartSpider(scrapy.Spider):
    name = "Estatemart"
    # "https://www.estatemartbd.com/en/145/full?search={%22page_num%22:0,%22v_search_option_79%22:%22Apartment%20-%22,%22v_search_option_64%22:%22%22,%22v_search_option_3%22:%22%22,%22v_search_option_36_from%22:%22%22,%22v_search_option_36_to%22:%22%22,%22v_search_option_20%22:%22%22,%22v_search_option_19%22:%22%22}",
    # "https://www.estatemartbd.com/en/145/full?search={%22page_num%22:0,%22v_search_option_79%22:%22House%20-%22,%22v_search_option_64%22:%22%22,%22v_search_option_3%22:%22%22,%22v_search_option_36_from%22:%22%22,%22v_search_option_36_to%22:%22%22,%22v_search_option_20%22:%22%22,%22v_search_option_19%22:%22%22}",
    # "https://www.estatemartbd.com/en/145/full?search={%22page_num%22:0,%22v_search_option_79%22:%22Land%20-%22,%22v_search_option_64%22:%22%22,%22v_search_option_3%22:%22%22,%22v_search_option_36_from%22:%22%22,%22v_search_option_36_to%22:%22%22,%22v_search_option_20%22:%22%22,%22v_search_option_19%22:%22%22}"
    
    start_urls=["https://www.estatemartbd.com/en/174/all_ads"]
    
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self,response):
        self.driver.get(response.url)
        while True:
            try:
                time.sleep(5)
                links = self.driver.find_elements(By.XPATH,'//*[@class="card"]/a[1]')
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                for link in links:
                    link=link.get_attribute("href")
                    yield scrapy.Request(url=link,callback = self.parse_data)
                next_page = self.driver.find_element(By.XPATH,"//ul[@class='pagination']/li[@class='active']//following-sibling::li[1]/a")
                # next_page_num=int(next_page.get_attribute("text"))
                next_page.click()
            except:
                break
        
        
    def parse_data(self,response):
        yield {
            "Name":response.css("div.card-body a h3::text").get(default = "N\A").replace("\n","").encode('utf-8'),
            "Location":response.css("div.details-info ul li span::text").get(default = "N\A"),
            "Bathrooms":[response.css("div.details-info").xpath(f"ul/li[{num}]/span/text()").get(default ="N\A") for num in range(0,11) if response.css("div.details-info").xpath(f"ul/li[{num}]/h4/text()").get()  == "Bathrooms:"],
            "Bedrooms":[response.css("div.details-info").xpath(f"ul/li[{num}]/span/text()").get(default ="N\A") for num in range(0,11) if response.css("div.details-info").xpath(f"ul/li[{num}]/h4/text()").get()  == "Bedrooms:"],
            "Size (in sqft)":[response.css("div.details-info").xpath(f"ul/li[{num}]/span/text()").get(default ="N\A") for num in range(0,11) if response.css("div.details-info").xpath(f"ul/li[{num}]/h4/text()").get()  == "Size:"],
            "Size Range (in sqft)":[response.css("div.details-info").xpath(f"ul/li[{num}]/span/text()").get(default ="N\A") for num in range(0,11) if response.css("div.details-info").xpath(f"ul/li[{num}]/h4/text()").get()  == "Size ( Range ):"],
            "Price per sqft":[response.css("div.details-info").xpath(f"ul/li[{num}]/span/text()").get(default ="N\A").replace("৳","") for num in range(0,11) if response.css("div.details-info").xpath(f"ul/li[{num}]/h4/text()").get()  == "Price Per SqFt:"],
            "Ownership type":  [response.css("div.details-info").xpath(f"ul/li[{num}]/span/text()").get(default ="N\A") for num in range(0,11) if response.css("div.details-info").xpath(f"ul/li[{num}]/h4/text()").get()  == "Ownership:"],
            "Features": [j.css("small::text").get(default = "N\A") for i in response.css("form.form_field") for j in i.css("li.input-field")],
            "Total price":response.css("div.rate-info h5::text").get(default = "N\A").replace(" ","").replace("\n","").replace("৳",""),
            "AD URL" : response.url

        }
    def closed(self, reason):
        self.driver.quit()

# AD URL : response.url



