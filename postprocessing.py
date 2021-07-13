from TikTokApi import TikTokApi
import csv
from feedgen.feed import FeedGenerator


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
        fg.logo('http://ex.com/logo.jpg')
        fg.subtitle('OK Boomer, all the latest TikToks from' + user)
        fg.link( href=' https://cdn.jsdelivr.net/gh/conoro/tiktok-rss-flat/rss/' + user + '.xml', rel='self' )
        fg.language('en')

        for tiktok in tiktoks:
            fe = fg.add_entry()
            link = "https://www.tiktok.com/@" + user + "/video/" + tiktok['id']
            fe.id(link)
            fe.title(tiktok['desc'])
            fe.link(href=link)
            fe.description("<img src='" + tiktok['video']['originCover'] + "' />")

        fg.rss_file('rss/' + user + '.xml') # Write the RSS feed to a file
