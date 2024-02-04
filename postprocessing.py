import csv
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
from tiktokapipy.api import TikTokAPI
import logging

#now we will Create and configure logger
logging.basicConfig(filename="std.log",
					format='%(asctime)s %(message)s',
					filemode='w', encoding='utf-8')

#Let us Create an object
logger=logging.getLogger()

#Now we are going to Set the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Now using a new TikTok library https://github.com/Russell-Newton/TikTokPy

# Normal GitHub Pages URL
# ghPagesURL = "https://conoro.github.io/tiktok-rss-flat/"

# Custom Domain
ghPagesURL = "https://rededemuseus.github.io/tiktok-rss-flat/"

maxItems = 5


def run(csvuser):
    try:
        fg = FeedGenerator()
        fg.id('https://tiktok.com/@' + csvuser)
        fg.title(csvuser + ' TikTok')
        fg.author( {'name':'Conor ONeill','email':'conor@conoroneill.com'} )
        fg.link( href='http://tiktok.com', rel='alternate' )
        fg.logo(ghPagesURL + 'tiktok-rss.png')
        fg.subtitle('All the latest TikToks from ' + csvuser)
        fg.link( href=ghPagesURL + 'rss/' + csvuser + '.xml', rel='self' )
        fg.language('en')

        # Set the last modification time for the feed to be the most recent post, else now.
        updated=None

        print("Step 5", flush=True)

        with TikTokAPI(navigation_retries=3, navigation_timeout=60, args=["--disable-gpu", "--single-process"]) as api:

            print("Step 6", flush=True)

            tiktokuser = api.user(csvuser, video_limit=maxItems)
            print(tiktokuser, flush=True)

            for video in tiktokuser.videos:
                print("Step 7", flush=True)

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

