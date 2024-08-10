import os
import asyncio
import csv
import time
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
#from tiktokapipy.api import TikTokAPI
from TikTokApi import TikTokApi
import config
from playwright.async_api import async_playwright, Playwright
from pathlib import Path
from urllib.parse import urlparse


# Edit config.py to change your URLs
ghRawURL = config.ghRawURL

api = TikTokApi()

ms_token = os.environ.get(
    "MS_TOKEN", None
)

async def runscreenshot(playwright: Playwright, url, screenshotpath):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = await chromium.launch()
    page = await browser.new_page()
    await page.goto(url)
    # Save the screenshot
    await page.screenshot(path=screenshotpath, quality = 20, type = 'jpeg')
    await browser.close()

async def user_videos():

    with open('subscriptions.csv') as f:
        cf = csv.DictReader(f, fieldnames=['username'])
        for row in cf:
            user = row['username']

            print(f'Running for user \'{user}\'')

            fg = FeedGenerator()
            fg.id('https://www.tiktok.com/@' + user)
            fg.title(user + ' TikTok')
            fg.author( {'name':'Conor ONeill','email':'conor@conoroneill.com'} )
            fg.link( href='http://tiktok.com', rel='alternate' )
            fg.logo(ghRawURL + 'tiktok-rss.png')
            fg.subtitle('OK Boomer, all the latest TikToks from ' + user)
            fg.link( href=ghRawURL + 'rss/' + user + '.xml', rel='self' )
            fg.language('en')

            # Set the last modification time for the feed to be the most recent post, else now.
            updated=None
            
            async with TikTokApi() as api:
                await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
                ttuser = api.user(user)
                try:
                    user_data = await ttuser.info()
                    #print(user_data)

                    async for video in ttuser.videos(count=10):
                        fe = fg.add_entry()
                        link = "https://tiktok.com/@" + user + "/video/" + video.id
                        fe.id(link)
                        ts = datetime.fromtimestamp(video.as_dict['createTime'], timezone.utc)
                        fe.published(ts)
                        fe.updated(ts)
                        updated = max(ts, updated) if updated else ts
                        if video.as_dict['desc']:
                            fe.title(video.as_dict['desc'][0:255])
                        else:
                            fe.title("No Title")
                        fe.link(href=link)
                        if video.as_dict['desc']:
                            content = video.as_dict['desc'][0:255]
                        else:
                            content = "No Description"
                        if video.as_dict['video']['cover']:
                            videourl = video.as_dict['video']['cover']
                            parsed_url = urlparse(videourl)
                            path_segments = parsed_url.path.split('/')
                            last_segment = [seg for seg in path_segments if seg][-1]

                            screenshotsubpath = "thumbnails/" + user + "/screenshot_" + last_segment + ".jpg"
                            screenshotpath = os.path.dirname(os.path.realpath(__file__)) + "/" + screenshotsubpath
                            if not os.path.isfile(screenshotpath):
                                async with async_playwright() as playwright:
                                    await runscreenshot(playwright, videourl, screenshotpath)
                            screenshoturl =  ghRawURL + screenshotsubpath
                            content = '<img src="' + screenshoturl + '" / > ' + content    
                            #content = screenshoturl + ' ' + content    
                            #content = '<media:content url="' + screenshoturl + '" type="image/jpeg" medium="image"> ' + content 
                            #content = '<![CDATA[<img src="' + screenshoturl + '" />]]> ' + content

                        fe.content(content)
                    fg.updated(updated)
                    fg.rss_file('rss/' + user + '.xml', pretty=True) # Write the RSS feed to a file
                        #print(video)
                        #print(video.as_dict)
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    asyncio.run(user_videos())
