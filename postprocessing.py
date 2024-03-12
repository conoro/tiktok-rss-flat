import asyncio
import csv
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
#from tiktokapipy.api import TikTokAPI
from TikTokApi import TikTokApi
import config

# Normal GitHub Pages URL
# ghPagesURL = "https://conoro.github.io/tiktok-rss-flat/"

# Custom Domain
ghPagesURL = config.ghPagesURL

api = TikTokApi()

ms_token = config.ms_token

async def user_videos():

    with open('subscriptions.csv') as f:
        cf = csv.DictReader(f, fieldnames=['username'])
        for row in cf:
            user = row['username']

            print(f'Running for user \'{user}\'')

#           user = "therock"
            fg = FeedGenerator()
            fg.id('https://www.tiktok.com/@' + user)
            fg.title(user + ' TikTok')
            fg.author( {'name':'Conor ONeill','email':'conor@conoroneill.com'} )
            fg.link( href='http://tiktok.com', rel='alternate' )
            fg.logo(ghPagesURL + 'tiktok-rss.png')
            fg.subtitle('OK Boomer, all the latest TikToks from ' + user)
            fg.link( href=ghPagesURL + 'rss/' + user + '.xml', rel='self' )
            fg.language('en')

            # Set the last modification time for the feed to be the most recent post, else now.
            updated=None
            
            async with TikTokApi() as api:
                await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
                ttuser = api.user(user)
                user_data = await ttuser.info()
                print(user_data)

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
                        fe.description(video.as_dict['desc'][0:255])
                    else:
                        fe.description( "No Description")        
                fg.updated(updated)
                fg.atom_file('rss/' + user + '.xml', pretty=True) # Write the RSS feed to a file
                    #print(video)
                    #print(video.as_dict)


if __name__ == "__main__":
    asyncio.run(user_videos())


'''
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
        fg.logo(ghPagesURL + 'tiktok-rss.png')
        fg.subtitle('OK Boomer, all the latest TikToks from ' + user)
        fg.link( href=ghPagesURL + 'rss/' + user + '.xml', rel='self' )
        fg.language('en')

        # Set the last modification time for the feed to be the most recent post, else now.
        updated=None

        for tiktok in api.user(username=user).videos(count=count):
            fe = fg.add_entry()
            link = "https://tiktok.com/@" + user + "/video/" + tiktok.id
            fe.id(link)
            ts = datetime.fromtimestamp(tiktok.as_dict['createTime'], timezone.utc)
            fe.published(ts)
            fe.updated(ts)
            updated = max(ts, updated) if updated else ts
            fe.title(tiktok.as_dict['desc'])
            fe.link(href=link)
            fe.description("<img src='" + tiktok.as_dict['video']['cover'] + "' />")

        fg.updated(updated)

        fg.atom_file('rss/' + user + '.xml', pretty=True) # Write the RSS feed to a file
'''

'''
def run(csvuser):
    try:
        fg = FeedGenerator()
        fg.id('https://tiktok.com/@' + csvuser)
        fg.title(csvuser + ' TikTok')
        fg.author( {'name':'Conor ONeill','email':'conor@conoroneill.com'} )
        fg.link( href='http://tiktok.com', rel='alternate' )
        fg.logo(ghPagesURL + 'tiktok-rss.png')
        fg.subtitle('OK Boomer, all the latest TikToks from ' + csvuser)
        fg.link( href=ghPagesURL + 'rss/' + csvuser + '.xml', rel='self' )
        fg.language('en')

        # Set the last modification time for the feed to be the most recent post, else now.
        updated=None

        with TikTokAPI(navigation_retries=3, navigation_timeout=60, args=["--disable-gpu", "--single-process"]) as api:


            tiktokuser = api.user(csvuser, video_limit=maxItems)
            print(tiktokuser, flush=True)

            for video in tiktokuser.videos:

                logger.debug(video.create_time.strftime("%m/%d/%Y, %H:%M:%S") + ": " + video.desc)
                logger.debug("URL = " + "https://tiktok.com/@" + csvuser + "/video/" + str(video.id))
                print(video.create_time.strftime("%m/%d/%Y, %H:%M:%S") + ": " + video.desc)
                print("URL = " + "https://tiktok.com/@" + csvuser + "/video/" + str(video.id))
                fe = fg.add_entry()
                link = "https://tiktok.com/@" + csvuser + "/video/" + str(video.id)
                fe.id(link)
                ts = video.create_time
                logger.debug(ts)
                fe.published(ts)
                fe.updated(ts)
                updated = max(ts, updated) if updated else ts
                if video.desc:
                    fe.title(video.desc[0:255])
                else:
                  fe.title("No Title")
                fe.link(href=link)
                # fe.description("<img src='" + tiktok.as_dict['video']['cover'] + "' />")
                if video.desc:
                    fe.description(video.desc)
                else:
                    fe.description( "No Description")
                #print(fg.rss_str(pretty=True))

        fg.updated(updated)
        fg.atom_file('rss/' + csvuser + '.xml', pretty=True) # Write the RSS feed to a file
    except Exception as e:
        logger.error(f"Error: {e}")
        pass

with open('subscriptions.csv') as f:

    for row in csv.DictReader(f, fieldnames=['username']):
        print(row['username'])
        run(row['username'])

'''