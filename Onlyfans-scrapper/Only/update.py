# 13.09.2023

# General import
import os, requests, zipfile, time
from rich.console import Console

# Class import
from Only.util.os import copyTree, rem_folder

# Variable
console = Console()


# Get main and base folder
main = os.path.abspath(os.path.dirname(__file__))
base = "\\".join(main.split("\\")[:-1])

def get_install_version():
    about = {}
    with open(os.path.join(main, '__version__.py'), 'r', encoding='utf-8') as f:
        exec(f.read(), about)
    return about['__version__']

def main_update():

    # Get last version from req
    json = requests.get("https://api.github.com/repos/ghost6446/Onlyfans-scrapper/releases").json()[0]
    stargazers_count = requests.get("https://api.github.com/repos/ghost6446/Onlyfans-scrapper").json()['stargazers_count']
    last_version = json['name']
    version_note = json['body']

    if get_install_version() != last_version:

        os.makedirs("temp", exist_ok=True)
        console.log(f"[green]Need to update to [white]=> [red]{last_version}")
        
        down_count = json['assets'][0]['download_count']
        down_name = json['assets'][0]['name']
        down_url = json['assets'][0]['browser_download_url']
        percentual_stars = round(stargazers_count / down_count * 100, 2)

        down_msg_obj = {'name': down_name, 'n_download': down_count, 'msg': version_note}
        console.log(f"Last version {down_msg_obj}")

        r = requests.get(down_url)
        open(f"temp/{down_name}", "wb").write(r.content)

        console.log("[green]Extract file")
        with zipfile.ZipFile(f"temp/{down_name}", "a") as zip:
            zip.extractall("")

        os.rename("Onlyfans-scrapper-main", "Onlyfans-scrapper")
        copyTree(src=os.path.join(base, down_name.split(".")[0].replace("-main", "")) + "\\", dst=base + "\\")

        console.log("[green]Clean ...")
        rem_folder("temp")
        rem_folder("Onlyfans-scrapper")

    else:
        console.log("[red]Everything up to date")
    
    print("\n")
    console.log(f"[red]Only was downloaded [yellow]{down_count} [red]times, but only [yellow]{percentual_stars} [red]of You(!) have starred it. \n\
        [cyan]Help the repository grow today, by leaving a [yellow]star [cyan]on it and sharing it to others online!")
    time.sleep(10)