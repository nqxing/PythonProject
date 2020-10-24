import json
import hashlib
def generate_x_instagram_gis(rhx_gis, cursor, profile_id):
    params = {
        "id": profile_id,
        "first": 12,
        "after": cursor,
    }
    par = {"id":"10648256385","include_reel":True,"fetch_mutual":False,"first":24}
    json_params = json.dumps(par, separators=(',', ':'))
    print(json_params)
    values = "{}:{}".format(rhx_gis, json_params)
    print(values)
    return hashlib.md5(values.encode('utf-8')).hexdigest()
rhx_gis = 'e16783690c90d7b498a213632a028ddf'
cursor = 'QVFBVGwwMUswTWIycmF1SDRKZnNqc0U1dE0zYnY2VjVNUXhuaWtCRi1renV1TnpBZmI1bXJMYnZZR2xDbnY4bVRxWkNTT0M0NHEwMUtFdTdTZURTYVFrQQ=='
profile_id = '338228967'
a = generate_x_instagram_gis(rhx_gis,cursor,profile_id)
print(a)