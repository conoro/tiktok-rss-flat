![TikTok RSS Logo](https://tiktokrss.conoroneill.com/favicon-32x32.png)
# TikTok RSS Using GitHub Actions

Generate usable RSS feeds from TikTok using GitHub Actions and GitHub Pages.


**NOTE March 2024: This seems to work again due to improvements in the original TikTok library. It requires an on-the-fly patch to that underlying TikTok library, which is hopefully only temporary**

## Setup for GitHub Actions
* To get your own instance running
    * Fork this repo
    * Make sure to enable Actions in the Actions tab
    * Enable GitHub Pages for your new repo
    * Get a value of ms_token from your TikTok account as follows:
        * Log into TikTok on Chrome desktop
        * View a user profile of someone you follow
        * Open Chrome DevTools with F12
        * Go to the Application Tab > Storage > Cookies > https://www.tiktok.com
        * Copy the cookie value of msToken
    * In the Settings Tab for your Repo, go to Secrets and Variables > Actions
    * Create a New Repository Secret:
        * Name = MS_TOKEN
        * Value = The value you got for msToken above 
    * Edit config.py to change `ghPagesURL` from "https://conoro.github.io/tiktok-rss-flat/" to your URL
    * Add the TikTok usernames that you like to subscriptions.csv

* It's set to run once every 4 hours and generates one RSS XML file per user in the rss output directory.
* You may need to update the msToken whenever your get GH Actions erros about TikTok returning an empty response

## Running locally as an alternative
* You need Python installed
* Then setup with:

```bash
pip install virtualenv
python -m venv venv
source venv\bin\activate
pip install -r requirements.txt
export MS_TOKEN="blah"
```

* Then run each time with:

```bash
source venv\bin\activate
python postprocessing.py
git commit -a -m "latest RSS"
git push origin main
```

## Feed Reading
* You then subscribe to each feed in [Feedly](https://www.feedly.com) or another feed reader using a GitHub Pages URL. Those URLs are constructed like so. E.g.:

    * TikTok User = iamtabithabrown
    * XML File = rss/iamtabithabrown.xml
    * Feedly Subscription URL = https://conoro.github.io/tiktok-rss-flat/rss/iamtabithabrown.xml
    * (Or in my case where I've set a custom domain for the GitHub Pages project called tiktokrss.conoroneill.com, the URL is https://tiktokrss.conoroneill.com/rss/iamtabithabrown.xml)

## Acknowledgements
This uses an unoffical [TikTokPy library](https://github.com/davidteather/TikTok-Api) to extract information about user videos from TikTok as JSON and generate RSS feeds for each user you are interested in.

Logo was created using the TikTok and RSS [Font Awesome](https://fontawesome.com/license/free) icons via CC BY 4.0 License

Copyright Conor O'Neill, 2021-2024 (conor@conoroneill.com)

License Apache 2.0

