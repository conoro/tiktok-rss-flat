![TikTok RSS Logo](https://tiktokrss.conoroneill.com/favicon-32x32.png)
# TikTok RSS Using GitHub OCTO Flat Data


** NOTE March 2024: This can work locally again due to improvements in the original TikTok library. But a small issue means it can only run on your local machine. You need to install everything and then edit tiktok.py to change line 203 from headless=True to headless=False. I'll see if I can get it running on GH Actions in the coming week **

* Generate usable RSS feeds from TikTok using GitHub Actions and GitHub Pages.

* This uses an unoffical [TikTokPy library](https://github.com/davidteather/TikTok-Api) to extract information about user videos from TikTok as JSON and generate RSS feeds for each user you are interested in.

* To get your own instance running
    * Fork this repo 
    * Copy config-example.py to config.py and follow instructions for changing ms_token 
    * Enable GitHub Pages for your new repo
    * Change the `ghPagesURL` in config.py from "https://conoro.github.io/tiktok-rss-flat/" to your URL
    * Add the TikTok usernames that you like to subscriptions.csv
    * Make sure to enable Actions in the Actions tab 

* It's set to run once per hour and generates one RSS XML file per user in the rss output directory.

* You then subscribe to each feed in [Feedly](https://www.feedly.com) or another feed reader using a GitHub Pages URL. Those URLs are constructed like so. E.g.:

    * TikTok User = iamtabithabrown
    * XML File = rss/iamtabithabrown.xml
    * Feedly Subscription URL = https://conoro.github.io/tiktok-rss-flat/rss/iamtabithabrown.xml
    * (Or in my case where I've set a custom domain for the GitHub Pages project called tiktokrss.conoroneill.com, the URL is https://tiktokrss.conoroneill.com/rss/iamtabithabrown.xml)

Logo was created using the TikTok and RSS [Font Awesome](https://fontawesome.com/license/free) icons via CC BY 4.0 License

Copyright Conor O'Neill, 2021 (conor@conoroneill.com)

License Apache 2.0

