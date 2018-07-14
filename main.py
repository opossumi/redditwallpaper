#!/usr/bin/env python
""""
Downloads top wallpapers from r/wallpapers and saves them to ~/.wallpapers

Intended usage (in crontab):
HOME=/home/user
0 * * * * /usr/local/bin/redditwallpaper_delayed
*/5 * * * * /usr/local/bin/change_wallpaper
"""

import argparse
import os
import re
import requests
from urllib.parse import urlparse

headers = {'user-agent': 'redditwallpaper/0.1.0'}
wallpaper_folder = os.path.join(os.path.expanduser("~"), ".wallpapers")

def fetch(url):
    r = requests.get(url, headers=headers)
    if not r.headers['content-type'] in ('image/jpeg', 'image/png', 'image/bmp'):
        return False

    fname = os.path.basename(urlparse(url).path)
    if 'content-disposition' in r.headers:
        fname = os.path.basename(headers['content-disposition'])
    path = os.path.join(wallpaper_folder, fname)

    if os.path.isfile(path):
        return False

    with open(path, 'wb') as fout:
        fout.write(r.content)

    return True

def fetch_images(url):
    r = requests.get(url, headers=headers)
    data = r.json()
    for c in data['data']['children']:
        for img in c['data']['preview']['images']:
            url = img['source']['url']
            fname = os.path.basename(urlparse(url).path)
            path = os.path.join(wallpaper_folder, fname)
            if not os.path.isfile(path):
                print ("Fetching", url)
                fetch(img['source']['url'])
            else:
                print ("Skipping", fname)

def main():
    parser = argparse.ArgumentParser(description='Downloads images from reddit')
    parser.add_argument('--freq', default='day', help='hour, day, week, month, year or all')
    parser.add_argument('--subreddit', default='wallpapers')

    args = parser.parse_args()

    reddit_json_url = 'http://www.reddit.com/r/' + args.subreddit + '/top.json?sort=top&t=' + args.freq
    fetch_images(reddit_json_url)

if __name__ == '__main__':
    main()
