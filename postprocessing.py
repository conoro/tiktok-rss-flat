from TikTokApi import TikTokApi

api = TikTokApi.get_instance()

count = 5

tiktoks = api.byUsername("iamtabithabrown", count=count)

outputFile = open("tabitha.txt", "w")


for tiktok in tiktoks:
    print(tiktok)
    outputFile.write(tiktok)

outputFile.close()
