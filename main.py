#!/usr/bin/env python
""""
Downloads top wallpapers from r/wallpapers and saves them to ~/.wallpapers

Intended usage (run as user, not root):
0 * * * * /usr/local/bin/redditwallpaper_delayed
*/5 * * * * /usr/local/bin/change_wallpaper
"""

import argparse
import os
import re
import requests
from urllib.parse import urlparse

# Copy-pasted from stackoverflow ":D"
import time
from threading import Lock
mutex = Lock()
nextTime = [0.0]
def RateLimited(limit=None):
    def decorate(func):
        global nextTime
        def rateLimitedFunction(*args,**kargs):
            mutex.acquire()
            maxPerSecond = limit
            if not maxPerSecond:
                if hasattr(args[0], 'ratelimit'):
                    maxPerSecond = getattr(args[0], 'ratelimit')
                else:
                    maxPerSecond = 1 # Default value
            minInterval = 1.0 / float(maxPerSecond)
            leftToWait = nextTime[0] - time.perf_counter()
            nextTime[0] = max(nextTime[0], time.perf_counter())+minInterval
            mutex.release()
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            return ret
        return rateLimitedFunction
    return decorate

s = requests.Session()
s.headers = {'user-agent': 'redditwallpaper/0.2.0'}
wallpaper_folder = os.path.join(os.path.expanduser("~"), ".wallpapers")

@RateLimited(0.5)
def fetch(url):
    r = s.get(url)
    if r.status_code != 200:
        print ('Not working, abort mission')
        os.exit(1)
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
    r = s.get(url)
    data = r.json()
    for c in data['data']['children']:
        url = (c['data']['url'])
        if re.match('.*\.(jpg|png)', url):
            fname = os.path.basename(urlparse(url).path)
            #print (url, fname)
            path = os.path.join(wallpaper_folder, fname)
            if not os.path.isfile(path):
                print ("Fetching", url)
                fetch(url)
            else:
                print ("Skipping", fname)

def main():
    parser = argparse.ArgumentParser(description='Downloads images from reddit')
    parser.add_argument('--freq', default='day', help='hour, day, week, month, year or all')
    parser.add_argument('--subreddit', default='wallpapers')

    args = parser.parse_args()

    reddit_json_url = 'https://www.reddit.com/r/' + args.subreddit + '/top.json?sort=top&t=' + args.freq
    print (reddit_json_url)
    fetch_images(reddit_json_url)

if __name__ == '__main__':
    main()
