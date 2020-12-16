import scrapy
import os
from time import sleep
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy_selenium.items import DribbbleItem

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# import logger

base_dir = os.path.join(os.path.dirname(__file__), '..', '..')

def scroll(driver, timeout):
    last_height= driver.execute_script('return document.body.scrollHeight')
    MAX_SCROLL = 10
    i = 0

    while i <= MAX_SCROLL:
        # scroll down to bottom
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        # wait to load page
        sleep(timeout)
        # calculate new height
        new_height = driver.execute_script('return document.body.scrollHeight')

        # check if there is pop up
        try: 
            WebDriverWait(driver,7).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.dismiss()
            print('pop up dismissed')
        except TimeoutException:
            print('no pop is present')
            

        if new_height == last_height:
            break
        last_height = new_height



class DribbblerSpider(scrapy.Spider):
    name = 'dribbble'
    allowed_domains = ['dribbble.com']
    start_urls = ['https://dribbble.com/designers']


    def parse(self, response):
        # set chrome options
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--headless")

        # set patrh for chrome driver
        chrome_driver_path = os.path.abspath(os.path.join(base_dir, 'chromedriver'))
        driver = Chrome(chrome_options = chrome_options, executable_path = chrome_driver_path)
        driver.get('https://dribbble.com/designers')

        # scroll to load all pages
        scroll(driver, 5)

        scrapy_selector = Selector(text = driver.page_source)
        for card in scrapy_selector.css('div.hiring-card-details-heading'): 
            loader = ItemLoader(item = DribbbleItem(), selector = card) 
            loader.add_xpath('name', ".//h3/text()")
            loader.add_xpath('location', ".//span/p[not(contains(.,'USD'))]/text()")
            yield loader.load_item()






