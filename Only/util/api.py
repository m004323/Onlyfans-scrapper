# 9.08.2023 -> 12.09-2023

# Import
import requests, time, os
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor

# Variable
console = Console()
arr_media = []


# [ func ]
def get_creator(radice, msg):

    user_data = {
        'name': radice['name'],
        'user': radice['username'],
        'id': radice['id'],
        'n_posts': radice['postsCount'],
        'n_photos': radice['photosCount'],
        'n_videos': radice['videosCount'],
        'n_audio': radice['audiosCount'],
        '*n_medias': radice['mediasCount'],
        'join_data': str(radice['joinDate']).split("T")[0]
    } 

    console.log(f"[blue]Info [green]{msg} [white]=> [cyan]{user_data}")


def dump_post(radice):

    if(len(radice) != 0):
        for i in range(len(radice)):
            for j in range(len(radice[i]['media'])):

                url = ""
                try: 
                    url = radice[i]['media'][j]['files']['source']['url']
                except:
                    try: 
                        url = radice[i]['media'][j]['source']['source']
                    except: 
                        url = None

                if radice[i]['media'][j]['type'] == "photo": 
                    arr_media.append({
                        'id': radice[i]['media'][j]['id'],
                        'url': url,'is_video': False
                    })

                else: 
                    arr_media.append({
                        'id': radice[i]['media'][j]['id'],
                        'url': url, 
                        'is_video': True
                    })

    else:
        console.log("[red] ERROR [dump_post] ")

def dump_chat(radice):

    for media in radice:
        if media['canView']:

            print("..")

            if media['type'] == "photo": 
                arr_media.append({
                    'id': media['id'],
                    'url': media['src'],
                    'is_video': False
                })
            else: 
                arr_media.append({
                    'id': media['id'],
                    'url': media['src'],
                    'is_video': True
                })


def donwload_media(media, file_name):

    if(not os.path.isfile(file_name)):
        console.log(f"Download ({media['id']}) => [ {arr_media.index(media) + 1} / {len(arr_media)} ]")

        if media['url'] != None and "http" in media['url']:
            r = requests.get(media['url'])

            if(r.status_code == 200):
                open(file_name, "wb").write(r.content)
            
            else:
                console.log(f"[red] ERROR [{media['id']}] => {r.status_code}")
        
        else:
            console.log("[cyan]Unlock content")
    
    else:
        console.log("[cyan]Skip")

def donwload_medias(folder_name, sub_folder):

    global arr_media

    # Create folder
    console.log(f"[blue]Medias find => [red]{len(arr_media)}")
    path_folder = "data/" + folder_name + "/" + sub_folder 
    os.makedirs(path_folder, exist_ok=True)

    # Download all media in array medias
    with ThreadPoolExecutor(max_workers=10) as executor:
        for media in arr_media:

            file_name = ""

            if(media['is_video']): 
                file_name = path_folder + "/" + str(media['id']) + ".mp4"
            else: 
                file_name = path_folder + "/" + str(media['id']) + ".jpg"

            executor.submit(donwload_media, media, file_name)
            time.sleep(0.1)

    # Clean array
    arr_media = []

