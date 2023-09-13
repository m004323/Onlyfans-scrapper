# 9.08.2023 -> 12.09.2023

# Class import
from util.Driver import Driver
from util.api import get_creator, dump_post, donwload_medias, dump_chat

# General import
import time, json, sys
from seleniumwire.utils import decode
from rich.console import Console

# Variable
console = Console()

# Init
console.log("[blue]Get driver")
driver = Driver()
driver.create(headless = False)


# [ func ]
def find_api_creator(creator_name):

    json_data = ""

    # Try to find https://onlyfans.com/api2/v2/users/{xxx}
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(creator_name) in str(req.url):

            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    if json_data != "":
        get_creator(radice=json_data, msg="creator")
    else:
        console.log("[red]ERROR [yellow](find_api_creator)")
        #sys.exit(0)

def find_api_by_prefix(name_api, show_url=False):

    arr_json_data = []

    # Try to find https://onlyfans.com/api2/v2/xxxxx
    for req in driver.driver.requests:
        if "api2" in str(req.url) and str(name_api) in str(req.url):

            if(show_url): console.log(f"[blue]FIND API [white]=> [green]{req.url}")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))

            arr_json_data.append({
                'url': req.url,
                'data': json.loads(response_body)
            })

    if len(arr_json_data) > 0:
        return arr_json_data
    else:
        console.log("[red]ERROR [yellow](find_api_creator)")
        sys.exit(0)

def find_api_me():

    json_data = find_api_by_prefix(name_api="users/me")[0]['data']
    get_creator(radice=json_data, msg="me")


def download(url, name, prefix_api, scroll_all_page):
    
    driver.get_page(url, sleep=10)
    find_api_me()
    find_api_creator(creator_name=name)

    if(scroll_all_page):
        driver.scroll_to_end()

    # Scroll only 5 time to load api
    else:
        driver.scroll_to_end(max_scroll=5)

    # Try find api match with "prefix_api" and dump all data
    for succ_req in find_api_by_prefix(name_api=prefix_api):
        dump_post(radice = succ_req['data']['list'])
        
    donwload_medias(name, prefix_api.replace("?", ""))

    driver.close()

def donwload_stories(url, name, prefix_api = "stories"):

    driver.get_page(url, sleep=10)
    find_api_me()
    find_api_creator(creator_name=name)

    # Custom "find_api_by_prefix"
    json_data = ""
    for req in driver.driver.requests:
        if "api2" in str(req.url) and prefix_api in str(req.url) and "highlights" not in str(req.url):

            console.log(f"[blue]FIND API [white]=> [green]{req.url}")
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            json_data = json.loads(response_body)

    if(json_data != ""):

        dump_post(radice=json_data)
        donwload_medias(folder_name=name, sub_folder=prefix_api.replace("?", ""))

    else:
        console.log("[red]ERROR [yellow](Cant find any stories)")
        sys.exit(0)

    driver.close()

def download_archive(url, name, prefix_api = "archived"):

    driver.get_page(url, sleep=10)
    find_api_me()
    find_api_creator(creator_name=name)

    # Try find api match with "prefix_api"
    json_succ_req = find_api_by_prefix(name_api=prefix_api)[0]['data']

    dump_post(radice = json_succ_req['list'])
    donwload_medias(folder_name=name, sub_folder=prefix_api.replace("?", ""))

    driver.close()

def download_streams(url, name, prefix_api = "streams"):

    driver.get_page(url, sleep=10)
    find_api_me()
    find_api_creator(creator_name=name)

    # Try find api match with "prefix_api"
    json_succ_req = find_api_by_prefix(name_api=prefix_api)[0]['data']

    dump_post(json_succ_req['list'])
    donwload_medias(name, prefix_api.replace("?", ""))

    driver.close()

def download_social_buttons(url, name, prefix_api = "social/buttons"):

    driver.get_page(url, sleep=10)
    find_api_me()
    find_api_creator(creator_name=name)

    # Custom "find_api_by_prefix"
    json_data = find_api_by_prefix(name_api=prefix_api)[0]['data']

    # Get url and name of the button 
    if str(json_data) != "[]":
        for i in range(len(json_data)):
            console.log(f"[blue]Find [white]([yellow]{json_data[i]['label']}[white]) = [red]{json_data[i]['url']}")
    else:
        console.log("[red]ERROR\INFO [yellow]no data for this profile")

    driver.close()

def download_chat(id_chat):

    driver.get_page(f"https://onlyfans.com/my/chats/chat/{id_chat}/", sleep=10)

    console.log("SCROLL TO THE TOP !! ")
    time.sleep(3)
    console.log("IF TOP OF THE PAGE, PRESS ANY KEY")
    msg = input("")

    # For all valid req in api xxx
    for req in find_api_by_prefix(name_api="chats"):

        # For only first one
        if req['url'] == f"https://onlyfans.com/api2/v2/chats/{id_chat}?skip_users=all":
            dump_chat(req['data']['lastMessage']['media'])

        # all other
        else:
            for msg in req['data']['list']:
                dump_chat(msg['media'])

    donwload_medias(user="chat", folder_name=id_chat)

    driver.close()


# [ class ]
class Only:

    username = ""

    def __init__(self, username) -> None:
        self.username = username

    def make_login(self):
        driver = Driver()
        driver.create(False)
        driver.get_page(url="https://onlyfans.com/", sleep=999)

    def get_url(self):
        if(self.username != None and self.username != ""):
            return f"https://onlyfans.com/{self.username}"

    def get_all_post(self):
        console.log("[yellow]GET ALL POST")
        download(
            url = self.get_url(), 
            name = self.username, 
            prefix_api = "posts?", 
            scroll_all_page = True
        )

    def get_all_media(self):
        console.log("[yellow]GET ALL MEDIA")
        download(
            url = self.get_url() + "/media", 
            name = self.username, 
            prefix_api = "medias?", 
            scroll_all_page = True
        )

    def get_last_post(self):
        console.log("[yellow]GET LAST POST")
        download(
            url = self.get_url(), 
            name = self.username, 
            prefix_api = "posts?", 
            scroll_all_page = False
        )

    def get_last_media(self):
        console.log("[yellow]GET LAST MEDIA")
        download(
            url = self.get_url() + "/media", 
            name = self.username, 
            prefix_api = "medias?", 
            scroll_all_page = False
        )

    def get_stories(self):
        console.log("[yellow]GET STORIES")
        donwload_stories(
            url = self.get_url(), 
            name = self.username
        )

    def get_archived(self):
        console.log("[yellow]GET ARCHIVIED")
        download_archive(
            url = self.get_url() + "/archived", 
            name = self.username
        )

    def get_streams(self):
        console.log("[yellow]GET STREAMS")
        download_streams(
            url = self.get_url() + "/streams", 
            name = self.username
        )

    def get_social_buttons(self):
        console.log("[yellow]GET BUTTON")
        download_social_buttons(
            url = self.get_url(), 
            name = self.username
        )

    def get_chat(self, id_chat):
        console.log("[yellow]GET CHAT")
        download_chat(
            id_chat=id_chat
        )
