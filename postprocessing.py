from tiktokapipy.api import TikTokAPI
import csv
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

# Now using a new TikTok library https://github.com/Russell-Newton/TikTokPy

# Normal GitHub Pages URL
# ghPagesURL = "https://conoro.github.io/tiktok-rss-flat/"

# Custom Domain
ghPagesURL = "https://tiktokrss.conoroneill.com/"

maxItems = 5

with open('subscriptions.csv') as f:
    cf = csv.DictReader(f, fieldnames=['username'])
    try:
        for row in cf:
            csvuser = row['username']

            print(f'Running for user \'{csvuser}\'')

            fg = FeedGenerator()
            fg.id('https://www.tiktok.com/@' + csvuser)
            fg.title(csvuser + ' TikTok')
            fg.author( {'name':'Conor ONeill','email':'conor@conoroneill.com'} )
            fg.link( href='http://tiktok.com', rel='alternate' )
            fg.logo(ghPagesURL + 'tiktok-rss.png')
            fg.subtitle('OK Boomer, all the latest TikToks from ' + csvuser)
            fg.link( href=ghPagesURL + 'rss/' + csvuser + '.xml', rel='self' )
            fg.language('en')

            # Set the last modification time for the feed to be the most recent post, else now.
            updated=None


            with TikTokAPI() as api:
#            with TikTokAPI(navigation_retries=3, navigation_timeout=60) as api:
                tiktokuser = api.user(csvuser)
                i = 0
                for video in tiktokuser.videos:
                    if i >= maxItems:
                        break
                    i = i + 1
                    # print(video.create_time, video.desc)
                    print("URL = " + "https://www.tiktok.com/@" + csvuser + "/video/" + str(video.id))
                    fe = fg.add_entry()
                    link = "https://tiktok.com/@" + csvuser + "/video/" + str(video.id)
                    fe.id(link)
                    ts = video.create_time
                    print(ts)
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
    except Exception:
        print("Some error")
        pass
