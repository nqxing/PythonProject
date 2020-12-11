import pymongo

# myclient = pymongo.MongoClient("mongodb://116.62.126.139:27017/")
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["aweme"]
mydb.authenticate('nqxing','mm.231798')