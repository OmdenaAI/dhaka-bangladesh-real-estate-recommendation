from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import selenium
import scrapy
from ..items import RealestatescrapperItem



class StartSpider(scrapy.Spider):

    name = "testing"
    start_urls = ["https://www.bdhousing.com/"]
    main_url = "https://www.bdhousing.com"

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self,response):

          
        try:
            i = 1
            while True:
                try:
                    time.sleep(5)
                    self.driver.get(response.url)
                    city = self.driver.find_element(By.ID , "benSearch")
                    button = self.driver.find_element(By.XPATH ,'//*[@id="benSearch"]/button')

                    city.find_element(By.XPATH ,f'//*[@id="post_r_city"]/option[{i}]').click()
                    button.click()
                        
                    while True:
                        try:
                            time.sleep(5)
                            u = self.driver.current_url
                            print(f"page {i},{u}")
                            all_urls = self.driver.find_elements(By.XPATH ,'//*[@class="listing-list-photo"]/a')
                                
                            for url in all_urls:
                                url = url.get_attribute("href")    
                                yield scrapy.Request(url = url, callback = self.parse_details)

                            
                            next_page = self.driver.find_element(By.XPATH, '//*[@id="ct-js-wrapper"]/div[4]/section/div/div[3]/div[2]/div[2]/div/div/ul/li[4]/a')
                            next_page.click()
                        except:
                            break
                    i+=1

                except:
                    break 
                
                

        except:
            pass

        
        try:
            i = 1
            while True:
                try:
                    time.sleep(5)
                    self.driver.get(response.url)
                    next_item = self.driver.find_element(By.XPATH, '//*[@id="ct-js-wrapper"]/div[4]/div[1]/div/div/div/div/div/ul/li[2]/a')
                    next_item.click()
                    city = self.driver.find_element(By.ID , "benSearch")
                    button = self.driver.find_element(By.XPATH ,'//*[@id="benSearch"]/button')

                    city.find_element(By.XPATH ,f'//*[@id="post_r_city"]/option[{i}]').click()
                    button.click()
                        
                    while True:
                        try:
                            time.sleep(5)
                            u = self.driver.current_url
                            print(f"page {i},{u}")
                            all_urls = self.driver.find_elements(By.XPATH ,'//*[@class="listing-list-photo"]/a')
                                
                            for url in all_urls:
                                url = url.get_attribute("href")    
                                yield scrapy.Request(url = url, callback = self.parse_details)

                            
                            next_page = self.driver.find_element(By.XPATH, '//*[@id="ct-js-wrapper"]/div[4]/section/div/div[3]/div[2]/div[2]/div/div/ul/li[4]/a')
                            next_page.click()   
                        except:
                            break
                    i+=1

                except:
                    break 
                
                

        except:
            pass
        
           

    def parse_details(self,response):
        item = RealestatescrapperItem()

        details = [f'//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[{i}]/span' for i in range(1,15)]
        #print(details[1])
        
            
        item["property_name"] = response.xpath(details[0]+'/text()').get().strip()
        item["property_type"] = response.xpath(details[1]+'/text()').get()
        item["sale_rent"] = response.xpath(details[2]+'/text()').get()

        item["location"] = response.xpath(details[3]+'/text()').get()

        item["size"] = response.xpath(details[5]+'/text()').get()

        if response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[9]/label/text()').get() == "Bedroom : ":
            item["bedroom"] = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[9]/span/text()').get()

        if response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[10]/label/text()').get() == "Baths : ":
            item["bathroom"] = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[10]/span/text()').get()

        if response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[12]/label/text()').get() == "Garages: ":
            item["parking"] = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[12]/span/text()').get().strip()

        if response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[14]/label/text()').get() == "Furnishing: ":   
            item["furnishing"] = response.xpath('//*[@id="ct-js-wrapper"]/div[4]/section[2]/div/div[2]/div/div[1]/div[1]/section[2]/div/div/div[2]/div/ul/li[14]/span/text()').get()
        
        item["amenities"] = [b.strip() for i, b in enumerate(response.css("div.row.content_areamMid div label::text").getall()) if i%2 != 0 ]
        item["url"] = response.url
        item["price"] = response.css("span.ct-productID.ct-fw-600::text").get().strip()

        yield item
            


#//*[@id="post_r_city"]/option[1]
#//*[@id="post_r_city"]/option[2]