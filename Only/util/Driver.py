# 5.07.2023 -> 12.09.2023

# General import
import os, time, subprocess, sys
from sys import platform
from bs4 import BeautifulSoup

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from rich.console import Console

# Variable
console = Console()

class Driver:

    service = None
    options = None
    driver = None

    def __init__(self) -> None:

        self.service = Service(ChromeDriverManager().install())

        self.options = webdriver.ChromeOptions()

        # For linux
        console.log("[green]Close all instance of chrome")
        if platform == "linux" or platform == "linux2":
            try: subprocess.check_output("kill -9 chrome.exe",  shell=True, creationflags=0x08000000) 
            except: pass

        # For win
        elif platform == "win32":
            try: subprocess.check_output("TASKKILL /IM chrome.exe /F",  shell=True, creationflags= 0x08000000) 
            except: pass
            
    def create(self, headless=False, minimize=False):

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

        self.driver = webdriver.Chrome(options=self.options,  service=self.service)
    
        if(minimize):
            self.driver.minimize_window()

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    def get_page(self, url, sleep=1):
        try:
            self.driver.get(url)
            time.sleep(sleep)

            while self.page_has_loaded() == False: 
                time.sleep(sleep)
        except:
            console.log("[red]Cant get the page")
            sys.exit(0)

    def get_soup(self):
        return BeautifulSoup(self.driver.page_source, "lxml")

    def scroll_to_end(self, sleep_load = 1, max_scroll=999):
        scroll_count = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            console.log(f"[blue]Scroll [red][{scroll_count}]")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")
            scroll_count+=1

            time.sleep(sleep_load)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")
                time.sleep(sleep_load)
                break

            if scroll_count == max_scroll:
                break

            last_height = new_height
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")
            time.sleep(sleep_load)

        console.log("[green]End reach")
    
    def close(self): 
        console.log("[red]Close driver")

        self.driver.close()
        self.driver.quit()
