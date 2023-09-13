# Onlyfans downloader

Script to download media and posts from creators on OnlyFans.

<h3>DISCLAIMERS:</h3>
<ul>
    <li>
        This tool is not affiliated, associated, or partnered with OnlyFans in any way. We are not authorized, endorsed, or sponsored by OnlyFans. All OnlyFans trademarks remain the property of Fenix International Limited.
    </li>
    <li>
        This is a theoritical program only and is for educational purposes. If you choose to use it then it may or may not work. You solely accept full responsability and indemnify the creator, hostors, contributors and all other involved persons from any any all responsability.
    </li>
<h3>

## Installation

Install requirement

```bash
    pip install -r requirements.txt
```

## Run Locally

Clone the project

```bash
  python Run.py
```

## Usage/Examples

```python
    [START]
    from Only import Only
    on = Only("creator_name")
    # Only of first launch -> on.make_login()

    [OTHER FUNC]
    on.get_all_post()
    on.get_last_post()
  
    on.get_all_media()
    on.get_last_media()

    on.get_stories()
    on.get_archived()
    on.get_streams()
    on.get_social_buttons()

```

## ERROR [NO MEDIA]
TO FIX NOT ALL MEDIA FIND: go to util\api.py find function "scroll_to_end" and change variable "sleep_load" until he can get to the bottom of the page, after that go to only.py and change driver.create(False) to driver.create (True) to remove headless of browser to test it and see what it do.


## Tutorial
https://www.youtube.com/watch?v=e6h13W3mVhA&t=48s

## Authors

- [@Ghost6446](https://www.github.com/Ghost6446)
