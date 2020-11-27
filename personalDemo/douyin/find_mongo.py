import pymongo
import json

myclient = pymongo.MongoClient("mongodb://116.62.126.139:27017/")
mydb = myclient["aweme"]       #test-db是数据库名称
mydb.authenticate('nqxing','mm.231798')

# poi_query = {"city_code": "350800"}
# mycol = mydb['poi_'].find(poi_query, {"_id": 0})

mycol = mydb['recomm'].find()
# mydict = {'_id':'PLAY_FENGJING', "name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com"}
#
# x = mycol.insert_one(mydict)
# print(x)

# ddd = {
#     "_id" : "PLAY_611000",
#     "res": {"city_code": "611000", "city_name": "商洛市", "switch_options": [{"ranks": [{"rank_name": "风景名胜", "rank_code": "PLAY_FENGJING", "ranks": None}], "rank_name": "游玩", "rank_code": "PLAY"}, {"rank_code": "FOOD", "ranks": [{"rank_code": "FOOD_CHUANCAI", "ranks": None, "rank_name": "川菜"}, {"rank_name": "美食", "rank_code": "FOOD_FOOD", "ranks": None}, {"rank_code": "FOOD_SHAOKAO", "ranks": None, "rank_name": "烧烤"}, {"ranks": None, "rank_name": "饮品", "rank_code": "FOOD_YINPIN"}, {"rank_name": "火锅", "rank_code": "FOOD_HOUGUO", "ranks": None}, {"rank_name": "小吃快餐", "rank_code": "FOOD_XIAOCHI", "ranks": None}, {"ranks": None, "rank_name": "面包甜点", "rank_code": "FOOD_MIANBAO"}], "rank_name": "全部美食"}, {"ranks": [{"rank_name": "丽人", "rank_code": "LIFE_LIREN", "ranks": None}, {"rank_name": "购物", "rank_code": "LIFE_GOUWU", "ranks": None}, {"rank_name": "本地玩乐", "rank_code": "LIFE_XIUYU", "ranks": None}, {"rank_name": "运动健身", "rank_code": "LIFE_YUNDONG", "ranks": None}], "rank_name": "休闲娱乐", "rank_code": "LIFE"}], "updated_at": 1606137675}
#
# }
#
#
# mycol.save(ddd)

# for x in mycol.find({},{"_id": 0}):
#     print('-----------------------------------------------------')
#     print(json.dumps(x, ensure_ascii=False))

for x in mycol:
    print('-----------------------------------------------------')
    print(x)

# myquery = {"_id": "PLAY_611000"}
# mydoc = mycol.find(myquery, {"_id": 0})
# print(mydoc)
# for x in mydoc:
#     print(x)

# print(mycol.find().count())