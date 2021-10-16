from TikTokApi import TikTokApi
import json

api = TikTokApi.get_instance()

count = 1

tiktoks = api.by_username("iamtabithabrown", count=count)

jsonString = json.dumps(tiktoks)
jsonFile = open("tiktok_example_data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

for tiktok in tiktoks:
   # print(tiktok)
    print(tiktok['video']['cover'])
    