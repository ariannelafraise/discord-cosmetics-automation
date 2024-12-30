import requests
import random
from dotenv import load_dotenv
import os
import time
import argparse

load_dotenv()

TOKEN=os.getenv('TOKEN')

BASE_URL = "https://discord.com/api/v9"
USER_URL = BASE_URL + "/users/@me"
COLLECTIBLES_URL = USER_URL + "/collectibles-purchases"
PROFILE_URL = USER_URL + "/profile"

CHANGE_AVATAR_DECORATION = False
CHANGE_PROFILE_EFFECT = False

def fetch_collectibles():
    headers = {'authorization': TOKEN, 'accept': '*/*'}
    return requests.get(COLLECTIBLES_URL, headers=headers).json()

def select_random_cosmetics(collectibles):
    if len(collectibles) <= 0:
        raise ValueError("No collectibles.")
    
    avatar_decoration = None
    profile_effect = None
    count = 0

    while profile_effect is None or avatar_decoration is None:
        if count > len(collectibles):
            break

        item = random.choice(collectibles)
        match item['items'][0]['type']:
            case 0:
                avatar_decoration = {
                    'avatar_decoration_id': item['items'][0]['id'],
                    'avatar_decoration_sku_id': item['items'][0]['sku_id']
                }

            case 1:
                profile_effect = {'profile_effect_id': item['items'][0]['id']}
        
        count+=1
    
    return (avatar_decoration, profile_effect)

def apply_cosmetics(avatar_decoration, profile_effect):
    if avatar_decoration is None and profile_effect is None:
        raise ValueError("No cosmetics.")

    headers = {
        'authorization': TOKEN,
        'accept': '*/*',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 10.1; Win64; x64) AppleWebKit/535.34 (KHTML, like Gecko) Chrome/51.0.2970.145 Safari/601',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3M7IFU7IFdpbmRvd3MgTlQgMTAuMTsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM1LjM0IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzUxLjAuMjk3MC4xNDUgU2FmYXJpLzYwMSJ9',
    }

    if avatar_decoration and CHANGE_AVATAR_DECORATION:
        requests.patch(USER_URL, headers=headers, json=avatar_decoration)
    if profile_effect and CHANGE_PROFILE_EFFECT:
        requests.patch(PROFILE_URL, headers=headers, json=profile_effect)

def execute():
    print("[Fetching cosmetics...]")
    try:
        collectibles = fetch_collectibles()
    except requests.exceptions.RequestException as e:
        print(e, "Aborting.")
        return

    print("[Selecting random cosmetics...]")
    try:
        selected = select_random_cosmetics(collectibles)
    except ValueError as e:
        print(e, "Aborting.")
        return

    print("[Sending changes to Discord...]")
    try:
        apply_cosmetics(*selected)
    except ValueError as e:
        print(e, "Aborting.")
        return
    except requests.exceptions.RequestException as e:
        print(e, "Aborting.")
        return

def check_loop_arg(value):
    try:
        checked_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected integer, got {type(value)}")
    if checked_value < 15:
        raise argparse.ArgumentTypeError(f"value must be greater than 15.")
    return checked_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--version', help="see the current version number", action='version', version="DCA v1.0")

    parser.add_argument('-l', '--loop', type=check_loop_arg, help="enable loop mode for a given number of seconds")

    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument('-a', '--avatar-decorations', help="enable switching between avatar decorations", action="store_true")
    target.add_argument('-p', '--profile-effects', help="enable switching between profile effects", action="store_true")
    target.add_argument('-b', '--change-both', help="enable switching between profile effects AND avatar decorations", action="store_true")

    args = parser.parse_args()

    if args.avatar_decorations:
        CHANGE_AVATAR_DECORATION = True
        CHANGE_PROFILE_EFFECT = False

    if args.profile_effects:
        CHANGE_AVATAR_DECORATION = False
        CHANGE_PROFILE_EFFECT = True

    if args.change_both:
        CHANGE_AVATAR_DECORATION = True
        CHANGE_PROFILE_EFFECT = True

    if args.loop:
        try:
            while True:
                execute()
                print(f"Waiting {args.loop} seconds")
                time.sleep(args.loop)
        except KeyboardInterrupt:
            print("bye!")   
    else:
        execute()