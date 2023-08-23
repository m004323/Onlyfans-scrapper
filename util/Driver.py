# 5.07.2023

# General import
import os, time, ast, json, subprocess
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Driver:

    service = None
    options = None
    driver = None

    def __init__(self) -> None:
        
        self.service = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        os.system("TASKKILL /IM chrome.exe /F")
        os.system("CLS")

    def create(self, headless = False):

        if(headless):
            self.options.add_argument("headless")

        self.options.add_argument("--window-size=1280,1280")
        self.options.add_argument('--user-data-dir=C:/Users/'+os.getlogin()+'/AppData/Local/Google/Chrome/User Data')

        self.options.add_experimental_option("useAutomationExtension", True)
        self.options.add_experimental_option("excludeSwitches",["enable-automation"])
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-insecure-localhost')
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-notifications")

        # Create drover
        self.driver = webdriver.Chrome(options=self.options,  service=self.service)

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    def get_page(self, url, sleep=1, show_url=True):
        start_time = time.time()
        self.driver.get(url)
        time.sleep(sleep)
        while( self.page_has_loaded() == False ):
            time.sleep(sleep)
        if show_url:
            print("GET URL => ", url, " IN", time.strftime("%H:%M:%S",time.gmtime(time.time() - start_time) ))

    def page_is_loading(self):
        while True:
            x = self.driver.execute_script("return document.readyState")
            if x == "complete":
                return True
            else:
                yield False

    def scroll_page(self, sleep=1):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep)

    def get_soup(self):
        return BeautifulSoup(self.driver.page_source, "lxml")

    def donwload_image(self, url, path):
        wait = WebDriverWait(self.driver, 3)
        self.driver.get(url)
        self.driver.save_screenshot(path)

    def close(self): 
        print("Close driver")
        self.driver.close()
        self.driver.quit()
