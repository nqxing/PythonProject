from xpinyin import Pinyin
import requests
import pymongo
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

myclient = pymongo.MongoClient("mongodb://116.62.126.139:27017/")
mydb = myclient["aweme"]
mydb.authenticate('nqxing','mm.231798')

headers = {
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

text = '''北京：110000，天津：120000，河北：130000，山西：140000，内蒙古：150000，辽宁：210000，吉林：220000，黑龙江：230000，上海：310000，江苏：320000，浙江：330000，安徽：340000，福建：350000，江西：360000，山东：370000，河南：410000，湖北：420000，湖南：430000，广东：440000，广西：450000，海南：460000，重庆：500000，四川：510000，贵州：520000，云南：530000，西藏：540000，陕西：610000，甘肃：620000，青海：630000，宁夏：640000，新疆：650000，香港：810000，澳门：820000'''

# def parse(res):
#     res = res.result()
#     print(res['msg'])

def gen_province(province_name, code, province_pinyin):
    if province_name in '北京天津上海重庆香港澳门':
        city_code = '{}0000'.format(code)
        rank_codes = get_rank_info(city_code, province_pinyin, province_name)
        if rank_codes:
            for rank_code in rank_codes:
                state = get_poi_list(city_code, rank_code, province_pinyin)
                if state:
                    print('{}[{}_{}]数据抓取完毕~'.format(province_name, rank_code, city_code))
                else:
                    print('{}[{}_{}]数据抓取出错!!!'.format(province_name, rank_code, city_code))
    else:
        for i in range(1, 25):
            if i < 10:
                city_code = '{}0{}00'.format(code, i)
            else:
                city_code = '{}{}00'.format(code, i)
            print(city_code)
            rank_codes = get_rank_info(city_code, province_pinyin, province_name)
            if rank_codes:
                for rank_code in rank_codes:
                    state = get_poi_list(city_code, rank_code, province_pinyin)
                    if state:
                        print('{}[{}_{}]数据抓取完毕~'.format(province_name, rank_code, city_code))
                    else:
                        print('{}[{}_{}]数据抓取出错!!!'.format(province_name, rank_code, city_code))

def get_rank_info(city_code, province_pinyin, province_name):
    rank_codes = []
    url = 'https://aweme.snssdk.com/aweme/v1/poi/rank/v2/info/?city_code={}&rank_code=PLAY_FENGJING'.format(city_code)
    res = requests.get(url, headers=headers).json()
    if res['rank_poi_list'] and res['poi_rank_info']['switch_options']:
        poi_rank_info = res['poi_rank_info']
        city_code = poi_rank_info['city_code']
        city_name = poi_rank_info['city_name']
        switch_options = poi_rank_info['switch_options']
        updated_at = poi_rank_info['updated_at']
        rank_info_dict = {
            "_id": "RANK_{}".format(city_code),
            "city_code": "{}".format(city_code),
            "city_name": city_name,
            "switch_options": switch_options,
            "updated_at": updated_at
        }
        mydb["rank_info"].save(rank_info_dict)
        province_dict = {
            "_id": "PRO_{}".format(city_code),
            "city_code": "{}".format(city_code),
            "city_name": city_name,
            "province_name": province_name,
            "province_pinyin": province_pinyin
        }
        mydb["provinces"].save(province_dict)
        for sw in switch_options:
            for s in sw['ranks']:
                rank_codes.append(s['rank_code'])
    return rank_codes

def get_poi_list(city_code, rank_code, province_pinyin):
    url = 'https://aweme.snssdk.com/aweme/v1/poi/rank/v2/info/?city_code={}&rank_code={}'.format(city_code, rank_code)
    res = requests.get(url, headers=headers).json()
    if res['rank_poi_list'] and res['poi_rank_banner']:
        rank_poi_list = []
        for poi in res['rank_poi_list']:
            poi_info = poi['poi_info']
            address_info = poi_info.setdefault("address_info", {})
            business_area_name = poi_info.setdefault("business_area_name", None)
            cover_url = poi_info['cover'].setdefault("url_list", [])[0]
            latitude = poi_info.setdefault("latitude", None)
            longitude = poi_info.setdefault("longitude", None)
            option_name = poi_info.setdefault("option_name", None)
            poi_name = poi_info.setdefault("poi_name", None)
            poi_rank_desc = poi_info.setdefault("poi_rank_desc", None)
            rank_score = poi_info.setdefault("rank_score", None)
            rating = poi_info.setdefault("rating", None)
            poi_dict = {
                "address_info": address_info,
                "business_area_name": business_area_name,
                "cover_url": cover_url,
                "latitude": latitude,
                "longitude": longitude,
                "option_name": option_name,
                "poi_name": poi_name,
                "poi_rank_desc": poi_rank_desc,
                "rank_score": rank_score,
                "rating": rating
            }
            rank_poi_list.append(poi_dict)
        poi_info_dict = {
            "_id": "POI_{}_{}".format(rank_code, city_code),
            "city_code": "{}".format(city_code),
            "rank_code": rank_code,
            "banner_url": res['poi_rank_banner']['banner_url']['url_list'][0],
            "description": res['poi_rank_banner']['description'],
            "explanation": res['poi_rank_banner']['explanation'],
            "title": res['poi_rank_banner']['title'],
            "rank_poi_list": rank_poi_list
        }
        mydb["poi_{}".format(province_pinyin)].save(poi_info_dict)
        return True
    else:
        return False
def main():
    pool = ThreadPoolExecutor(8)
    pin = Pinyin()
    lists = text.split('，')
    for l in lists:
        province_name = l.split('：')[0]
        code = l.split('：')[1][:2]
        province_pinyin = pin.get_pinyin(province_name, "")
        pool.submit(gen_province, province_name, code, province_pinyin)

main()
