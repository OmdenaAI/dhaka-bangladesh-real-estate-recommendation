import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from ..items import TheToLetItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class TheToLetSpider(scrapy.Spider):
    name = 'TheToLet'

    start_urls = ['https://www.thetolet.com/en/property-listing']

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        for _ in range(0, 100):
            total_div = self.driver.find_elements(By.XPATH, '//*[@id="wrapper"]/div[4]/div/div[1]/div/div')
            count_2 = len(total_div)
            self.driver.execute_script("arguments[0].scrollIntoView();", total_div[-1])
            link = self.driver.find_element(By.XPATH,
                                            f'//*[@id="wrapper"]/div[4]/div/div[1]/div/div[{str(count_2)}]/div/div')

            link.click()
            time.sleep(5)

        property_post_listing_urls = self.driver.find_elements(By.XPATH,
                                                               '//*[@id="wrapper"]/div[4]/div/div[1]/div/div/a')

        for url in property_post_listing_urls:
            url = url.get_attribute('href')
            yield scrapy.Request(url=url, callback=self.parse_detail_page, errback=self.errback_httpbin)

    def parse_detail_page(self, response):
        item = TheToLetItem()

        title = response.xpath('//*[@id="titlebar"]/div/div/div/div[1]/div/div/h2//text()').get().strip("\n")
        item['title'] = title

        property_basic_info_list = response.css('ul.property-main-features').get().replace('<li>', '').replace(
            '</li>\n',
            '').replace(
            '<ul class="property-main-features">\n', '').replace('<span>', ':').replace('</span>', ',').replace('</ul>',
                                                                                                                '').replace(
            ' ', '')[:-1] + ''
        item['basic_info'] = dict(item.split(':') for item in property_basic_info_list.split(','))

        address_list_str = ' '.join(
            response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/ul[3]//text()').getall()).strip("\n").replace('\n',
                                                                                                                   ' , ')
        full_address_str = address_list_str + ' , ' + ' '.join(
            response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/ul[2]//text()').getall()).strip("\n")

        item['address'] = address_list_str + full_address_str
        item['price_per_month'] = ''.join(
            response.xpath('//*[@id="titlebar"]/div/div/div/div[2]/div[1]//text()').getall()).replace('\n', '')

        item['type'] = ' '.join(title.split(' ')[:2])
        item['purpose'] = title.split(' ')[:3][2]
        item['amenities'] = ''.join(
            response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/ul[6]//text()').getall()).strip('\n').replace('\n',
                                                                                                                   ',')
        item['description'] = ''.join(
            response.xpath('//*[@id="wrapper"]/div[5]/div/div[3]/div/div[1]//text()').getall()).strip("\n").replace(
            '\n', ', ').replace('Show More', '').encode('utf-8')
        item['price_negotiable'] = self.price_negotiable_checker(
            response.xpath('//*[@id="titlebar"]/div/div/div/div[2]/div[2]//text()').get().replace('\n', ''))

        item['property_url'] = response.url

        yield item

    def price_negotiable_checker(self, price_type):
        flag = price_type.find('Negotiable')
        if flag == -1:
            return "No"
        else:
            return "Yes"

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

