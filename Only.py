# 9.08.2023

# Class import
from util.Driver import Driver
from util.api import get_info_profile_scrape, scroll_to_end, dump_post, download_api_media

# General import
import time, json
from seleniumwire.utils import decode


# Main function to download all media
def download(url, name, prefix_api, scroll_all_page):

    # Init class driver
    driver = Driver()
    driver.create(False)

    # Get user page
    driver.get_page(url, sleep=10)

    # [main] Get info page
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            
            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            # Print info of user
            get_info_profile_scrape(json_data)

    # [main] Scroll
    if(scroll_all_page):
        scroll_to_end(driver.driver)
    else:
        pixel = 0
        for _ in range(5):
            driver.driver.execute_script(f"window.scrollTo({pixel}, document.body.scrollHeight + 500)")
            pixel += 500

    # [main] Get all reqeest 
    for req in driver.driver.requests:
        if "api2" in str(req.url) and prefix_api in str(req.url):

            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            # Extract data
            dump_post(json_data['list'])
        
    # Download all
    download_api_media(name, prefix_api.replace("?", ""))

    # End
    driver.close()

# Main function to downalod stories
def donwload_stories(url, name, prefix_api = "stories"):

    # Init class driver
    driver = Driver()
    driver.create(False)

    # Get user page
    driver.get_page(url, sleep=10)

    # [main] Get info page
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            
            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            # Print info of user
            get_info_profile_scrape(json_data)

    # Download all stories
    json_data = ""
    for req in driver.driver.requests:
        if "api2" in str(req.url) and prefix_api in str(req.url) and "highlights" not in str(req.url):

            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    # Check if there is stories
    if(json_data != ""):
        print(json_data)
        dump_post(json_data)
    else:
        print("Cant find any stories")

    # Download all
    download_api_media(name, prefix_api.replace("?", ""))

    # End
    driver.close()

# Main function download archive
def download_archive(url, name, prefix_api = "archived"):

    # Init class driver
    driver = Driver()
    driver.create(False)

    # Get user page
    driver.get_page(url, sleep=10)

    # [main] Get info page
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            
            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            # Print info of user
            get_info_profile_scrape(json_data)

    # Download all stories
    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):

            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    # Check if there is stories
    if(json_data != ""):
        print(json_data)
        dump_post(json_data['list'])
    else:
        print("Cant find any archived file")

    # Download all
    download_api_media(name, prefix_api.replace("?", ""))

    # End
    driver.close()

# Main function download streams
def download_streams(url, name, prefix_api = "streams"):

    # Init class driver
    driver = Driver()
    driver.create(False)

    # Get user page
    driver.get_page(url, sleep=10)

    # [main] Get info page
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            
            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            # Print info of user
            get_info_profile_scrape(json_data)

    # Download all stories
    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):

            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    # Check if there is stories
    if(json_data != ""):
        print(json_data)
        dump_post(json_data['list'])
    else:
        print("Cant find any streams")

    # Download all
    download_api_media(name, prefix_api.replace("?", ""))

    # End
    driver.close()

# Main get buttons
def download_buttons(url, name, prefix_api = "social/buttons"):

    # Init class driver
    driver = Driver()
    driver.create(False)

    # Get user page
    driver.get_page(url, sleep=10)

    # [main] Get info page
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            
            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            # Print info of user
            get_info_profile_scrape(json_data)

    # Download all stories
    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):

            # Get json data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            for i in range(len(json_data)):

                print(f" - Find ({json_data[i]['label']}) = {json_data[i]['url']}")

    # End
    driver.close()

# Main class script
class Only:

    # Variable
    username = ""

    # Costructor
    def __init__(self, username) -> None:
        self.username = username

    # [ function ]
    def make_login():
        driver = Driver()
        driver.create(False)
        driver.get_page(url="https://onlyfans.com/", sleep=999)

    def get_url(self):
        if(self.username != None and self.username != ""):
            return  "https://onlyfans.com/" + self.username

    def get_all_post(self):
        download(self.get_url(), self.username, "posts?", True)

    def get_all_media(self):
        download(self.get_url() + "/media", self.username, "medias?", True)

    def get_last_post(self):
        download(self.get_url(), self.username, "posts?", False)

    def get_last_media(self):
        download(self.get_url() + "/media", self.username, "medias?", False)

    def get_stories(self):
        donwload_stories(self.get_url(), self.username)

    def get_archived(self):
        download_archive(self.get_url() + "/archived", self.username)

    def get_streams(self):
        download_streams(self.get_url() + "/streams", self.username)

    def get_buttons(self):
        download_buttons(self.get_url() + "/streams", self.username)

