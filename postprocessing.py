from TikTokApi import TikTokApi
import csv
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

# Normal GitHub Pages URL
# ghPagesURL = "https://conoro.github.io/tiktok-rss-flat/"


# Custom Domain
# ghPagesURL = "https://tiktokrss.conoroneill.com/"
ghPagesURL = "https://fuska.github.io/tiktok-rss-flat/"
    
api = TikTokApi.get_instance()

count = 10

with open('subscriptions.csv') as f:
    cf = csv.DictReader(f, fieldnames=['username'])
    for row in cf:
        user = row['username']

        print (user)

        tiktoks = api.byUsername(user, count=count)
        
        fg = FeedGenerator()
        fg.id('https://www.tiktok.com/@' + user)
        fg.title(user + ' TikTok')
        fg.author( {'name':'Conor ONeill','email':'conor@conoroneill.com'} )
        fg.link( href='http://tiktok.com', rel='alternate' )
        fg.logo(ghPagesURL + '/tiktok-rss.png')
        fg.subtitle('OK Boomer, all the latest TikToks from ' + user)
        fg.link( href=ghPagesURL + 'rss/' + user + '.xml', rel='self' )
        fg.language('en')

        for tiktok in tiktoks:
            fe = fg.add_entry()
            link = "https://www.tiktok.com/@" + user + "/video/" + tiktok['id']
            fe.id(link)
            fe.published(datetime.fromtimestamp(tiktok['createTime'], timezone.utc))
            fe.title(tiktok['desc'])
            fe.link(href=link)
            fe.description("<img src='" + tiktok['video']['originCover'] + "' />")

        fg.rss_file('rss/' + user + '.xml') # Write the RSS feed to a file
