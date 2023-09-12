# 9.08.2023

# Import
import json, requests, time, os, sys, json
from concurrent.futures import ThreadPoolExecutor

def get_info_profile_scrape(json_data):
    user_data = {
        'name': json_data['name'],
        'user': json_data['username'],
        'id': json_data['id'],
        'n_posts': json_data['postsCount'],
        'n_photos': json_data['photosCount'],
        'n_videos': json_data['videosCount'],
        'n_audio': json_data['audiosCount'],
        '*n_medias': json_data['mediasCount'],
        'join_data': str(json_data['joinDate']).split("T")[0]
    } 
    print("Info page =>", user_data)

def scroll_to_end(driver, sleep_load = 0.6):
    counter = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")
        counter+=1
        time.sleep(sleep_load)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")
            time.sleep(sleep_load)
            break
        last_height = new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")
        time.sleep(sleep_load)
    print("Reach end page")
    return True

arr_media = []
def dump_post(radice):

    if(len(radice) != 0):
        for i in range(len(radice)):
            for j in range(len(radice[i]['media'])):
                url = ""
                
                try: url = radice[i]['media'][j]['files']['source']['url']
                except:
                    try: url = radice[i]['media'][j]['source']['source']
                    except: url = None
                    
                if(radice[i]['media'][j]['type'] == "photo"):
                    arr_media.append({
                        'id': radice[i]['media'][j]['id'],
                        'url': url,
                        'is_video': False,
                    })

                else:
                    arr_media.append({
                        'id': radice[i]['media'][j]['id'],
                        'url': url,
                        'is_video': True,
                    })

    else:
        print("ERROR [dump_post] ")

def download_single_media(media, file_name):
    if(not os.path.isfile(file_name)):
        print(f" - Download ({media['id']}) => [ {arr_media.index(media) + 1} / {len(arr_media)} ]")

        if(media['url'] != None and "http" in media['url']):
            r = requests.get(media['url'])
            if(r.status_code == 200):
                open(file_name, "wb").write(r.content)
            else:
                print(f"ERROR [{media['id']}] => {r.status_code}")
        else:
            print("Unlock content")
    else:
        print("Skip")

def download_api_media(user, folder_name):

    global arr_media
    print("Medias find => ", len(arr_media))
    path_folder = "data/" + user + "/" + folder_name 
    os.makedirs(path_folder, exist_ok=True)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for media in arr_media:
            file_name = ""
            if(media['is_video']): 
                file_name = path_folder + "/" + str(media['id']) + ".mp4"
            else: 
                file_name = path_folder + "/" + str(media['id']) + ".jpg"
            executor.submit(download_single_media, media, file_name)
            time.sleep(0.1)
    arr_media = []

def dump_media_chat(radice):
    for media in radice:
        url = ""    
        try: url = media['files']['source']['url'] # For api Stories
        except:
            try: url = media['source']['source'] # For api Post and media
            except: url = None
                    
        if(media['type'] == "photo"):
            arr_media.append({
                'id': media['id'],
                'url': url,
                'is_video': False,
            })
        else:
            arr_media.append({
                'id': media['id'],
                'url': url,
                'is_video': True,
            })

        
