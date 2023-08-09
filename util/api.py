# 9.08.2023

# Import
import json, requests, time, os, sys, json
from concurrent.futures import ThreadPoolExecutor

# Function to get info user page
def get_info_profile_scrape(json_data):

    # Get info
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

# Function to scrool to end of page
def scroll_to_end(driver, sleep_load = 0.6):

    # Variable
    counter = 0

    # Get first height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:

        # Scroll some bug
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")

        # Sleep and print scroll
        counter+=1
        time.sleep(sleep_load)

        # Get new height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Check if it is the end of the page
        if new_height == last_height:

            # Fa un'ultimo scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")
            time.sleep(sleep_load)

            # Fine loop
            break

        # Update last eight
        last_height = new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 500);")
        time.sleep(sleep_load)

    # End
    print("Reach end page")
    return True


# Variable with all info of medias
arr_media = []

# Function to extract info of media from json data
def dump_post(radice):

    # If there is something in json
    if(len(radice) != 0):

        # For all item in reels_media
        for i in range(len(radice)):
            #print("ID => ", radice[i]['id'])
            #print("LEN => ", len(radice))

            for j in range(len(radice[i]['media'])):
                #print("TYPE => ", radice[i]['media'][j]['type'] )

                # Get url if full not present
                url = ""
                
                try: url = radice[i]['media'][j]['files']['source']['url'] # For api Stories
                except:
                    try: url = radice[i]['media'][j]['source']['source'] # For api Post and media
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

# Function to download a single media and save to folder
def download_single_media(media, file_name):

    # Check if file already exist
    if(not os.path.isfile(file_name)):

        # Download it
        print(f" - Download ({media['id']}) => [ {arr_media.index(media) + 1} / {len(arr_media)} ]")

        if(media['url'] != None and "http" in media['url']):
            r = requests.get(media['url'])

            # Check response is valid and save content
            if(r.status_code == 200):
                open(file_name, "wb").write(r.content)
            else:
                print(f"ERROR [{media['id']}] => {r.status_code}")

        else:
            print("Unlock content")

    else:
        print("Skip")

# Loop function to download all media from arr_media
def download_api_media(user, folder_name):

    # Variable
    global arr_media

    # Save as json
    #with open(f"data_{folder_name}.json", 'w') as f:
    #    json.dump(arr_media, f)
    print("Medias find => ", len(arr_media))

    # Create path folder for download
    path_folder = "data/" + user + "/" + folder_name 
    os.makedirs(path_folder, exist_ok=True)

    # For all media find
    with ThreadPoolExecutor(max_workers=10) as executor:
        for media in arr_media:

            # Check if video or image 
            file_name = ""
            if(media['is_video']): 
                file_name = path_folder + "/" + str(media['id']) + ".mp4"
            else: 
                file_name = path_folder + "/" + str(media['id']) + ".jpg"

            # Download element
            executor.submit(download_single_media, media, file_name)
            time.sleep(0.1)

    # Clean arr
    arr_media = []
        