import pymongo
client = pymongo.MongoClient(host='localhost',port=27017)
db = client.test
collection = db.students
result = collection.find_one({'id':'20170101'}) #查询返回一条数据
print(result)
lists = collection.find({'id':'20170101'}) #查询返回全部数据
for list in lists:
    print(list)
    print(list['_id'])