import pymongo

myclient = pymongo.MongoClient("mongodb://116.62.126.139:27017/")
mydb = myclient["runoobdb"]
mycol = mydb["user"]

# mydict = {'_id':'PLAY_FENGJING', "name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com"}
#
# x = mycol.insert_one(mydict)
# print(x)

for x in mycol.find():
  print(x)