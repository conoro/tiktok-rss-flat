# TikTok RSS Using GitHub OCTO Flat Data
* Generate usable RSS feeds from TikTok using [GitHub OCTO Flat Data](https://octo.github.com/projects/flat-data) and GitHub Actions.

* This uses the unoffical [TikTokApi Python library](https://github.com/davidteather/TikTok-Api) to extract information about user videos from TikTok as JSON and generate RSS feeds for each user you are interested in.

* Just clone the repo to get your own instance running.

* You simply add the TikTok usernames you like to subscriptions.csv

* It's set to run once per hour and generates one RSS XML file per user in the rss output directory.

* You then subscribe to each feed in [Feedly](https://www.feedly.com) or similar using a JSDelivr URL. Those URLs are constructed like so. E.g.:

    * TikTok User = iamtabithabrown
    * XML File = rss/iamtabithabrown.xml
    * Feedly Subscription URL = https://cdn.jsdelivr.net/gh/conoro/tiktok-rss-flat/rss/iamtabithabrown.xml


Logo created using several [Font Awesome](https://fontawesome.com/license/free) icons via CC BY 4.0 License

Copyright Conor O'Neill, 2021 (conor@conoroneill.com)

License Apache 2.0

