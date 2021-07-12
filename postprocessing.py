from TikTokApi import TikTokApi
import json

api = TikTokApi.get_instance()

count = 5

tiktoks = api.byUsername("iamtabithabrown", count=count)

with open('tabitha.json', 'w') as jsonfile:
    json.dump(tiktoks, jsonfile)
