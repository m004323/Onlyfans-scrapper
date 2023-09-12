# 9.08.2023 -> 12.09.2023

# Class import
from util.Driver import Driver
from util.api import get_info_profile_scrape, scroll_to_end, dump_post, download_api_media, dump_media_chat

# General import
import time, json
from seleniumwire.utils import decode
from rich.console import Console

# Variable
console = Console()


def download(url, name, prefix_api, scroll_all_page):

    console.log("[red]GET DRIVER")
    driver = Driver()
    driver.create(headless = False)
    driver.get_page(url, sleep=10)

    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            console.log("[blue]FIND API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    console.log("[green]SCROOL TO THE END")
    if(scroll_all_page):
        scroll_to_end(driver.driver)
    else:
        pixel = 0
        for _ in range(5):
            driver.driver.execute_script(f"window.scrollTo({pixel}, document.body.scrollHeight + 500)")
            pixel += 500

    console.log("[green]DUMP")
    for req in driver.driver.requests:
        if "api2" in str(req.url) and prefix_api in str(req.url):
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            dump_post(json_data['list'])

    console.log("[red]DOWNLOAd")
    download_api_media(name, prefix_api.replace("?", ""))
    driver.close()

def donwload_stories(url, name, prefix_api = "stories"):

    console.log("[red]GET DRIVER")
    driver = Driver()
    driver.create(headless = False)
    driver.get_page(url, sleep=10)
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            console.log("[blue]FIND API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    json_data = ""
    for req in driver.driver.requests:
        if "api2" in str(req.url) and prefix_api in str(req.url) and "highlights" not in str(req.url):
            console.log("[blue]GET API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    if(json_data != ""):
        console.log("[green]DUMP")
        dump_post(json_data)
    else:
        print("Cant find any stories")

    console.log("[red]DOWNLOAd")
    download_api_media(name, prefix_api.replace("?", ""))
    driver.close()

def download_archive(url, name, prefix_api = "archived"):

    console.log("[red]GET DRIVER")
    driver = Driver()
    driver.create(False)
    driver.get_page(url, sleep=10)
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            console.log("[blue]FIND API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):
            console.log("[blue]GET API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    if(json_data != ""):
        console.log("[green]DUMP")
        dump_post(json_data['list'])
    else:
        print("Cant find any archived file")

    console.log("[red]DOWNLOAd")
    download_api_media(name, prefix_api.replace("?", ""))
    driver.close()

def download_streams(url, name, prefix_api = "streams"):

    console.log("[red]GET DRIVER")
    driver = Driver()
    driver.create(False)
    driver.get_page(url, sleep=10)
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            console.log("[blue]FIND API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):
            console.log("[blue]GET API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    if(json_data != ""):
        console.log("[green]DUMP")
        dump_post(json_data['list'])
    else:
        print("Cant find any streams")

    console.log("[red]DOWNLOAd")
    download_api_media(name, prefix_api.replace("?", ""))
    driver.close()

def download_buttons(url, name, prefix_api = "social/buttons"):

    console.log("[red]GET DRIVER")
    driver = Driver()
    driver.create(False)
    driver.get_page(url, sleep=10)

    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name) in str(req.url):
            console.log("[blue]FIND API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)
            get_info_profile_scrape(json_data)

    json_data = ""
    for req in driver.driver.requests:
        if prefix_api in str(req.url):
            console.log("[blue]GET API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            console.log("[red]DOWNLOAd")
            for i in range(len(json_data)):
                console.log(f"Find ({json_data[i]['label']}) = {json_data[i]['url']}")

    driver.close()

def download_chat(id_chat):

    console.log("[red]GET DRIVER")
    driver = Driver()
    driver.create(headless=False)
    driver.get_page(f"https://onlyfans.com/my/chats/chat/{id_chat}/", sleep=10)

    console.log("SCROLL TO THE TOP !! ")
    time.sleep(3)
    console.log("IF TOP OF THE PAGE, PRESS ANY KEY")
    msg = input("")

    for req in driver.driver.requests:
        if "v2/chats/" in str(req.url):
            console.log("[blue]FIND API")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

            console.log("[green]DUMP")
            if req.url == f"https://onlyfans.com/api2/v2/chats/{id_chat}?skip_users=all":
                dump_media_chat(json_data['lastMessage']['media'])
            else:
                for msg in json_data['list']:
                    dump_media_chat(msg['media'])

    console.log("[red]DOWNLOAd")
    download_api_media(user="chat", folder_name=id_chat)
    driver.close()

class Only:

    # Variable
    username = ""

    # Costructor
    def __init__(self, username) -> None:
        self.username = username

    # [ function ]
    def make_login(self):
        driver = Driver()
        driver.create(False)
        driver.get_page(url="https://onlyfans.com/", sleep=999)

    def get_url(self):
        if(self.username != None and self.username != ""):
            return f"https://onlyfans.com/{self.username}"

    def get_all_post(self):
        console.log("=> [yellow]GET ALL POST")
        download(
            url = self.get_url(), 
            name = self.username, 
            prefix_api = "posts?", 
            scroll_all_page = True
        )

    def get_all_media(self):
        console.log("=> [yellow]GET ALL MEDIA")
        download(
            url = self.get_url() + "/media", 
            name = self.username, 
            prefix_api = "medias?", 
            scroll_all_page = True
        )

    def get_last_post(self):
        console.log("=> [yellow]GET LAST POST")
        download(
            url = self.get_url(), 
            name = self.username, 
            prefix_api = "posts?", 
            scroll_all_page = False
        )

    def get_last_media(self):
        console.log("=> [yellow]GET LAST MEDIA")
        download(
            url = self.get_url() + "/media", 
            name = self.username, 
            prefix_api = "medias?", 
            scroll_all_page = False
        )

    def get_stories(self):
        console.log("=> [yellow]GET STORIES")
        donwload_stories(
            url = self.get_url(), 
            name = self.username
        )

    def get_archived(self):
        console.log("=> [yellow]GET ARCHIVIED")
        download_archive(
            url = self.get_url() + "/archived", 
            name = self.username
        )

    def get_streams(self):
        console.log("=> [yellow]GET STREAMS")
        download_streams(
            url = self.get_url() + "/streams", 
            name = self.username
        )

    def get_buttons(self):
        console.log("=> [yellow]GET BUTTON")
        download_buttons(
            url = self.get_url() + "/button", 
            name = self.username
        )

    def get_chat(self, id_chat):
        console.log("=> [yellow]GET CHAT")
        download_chat(
            id_chat=id_chat
        )
