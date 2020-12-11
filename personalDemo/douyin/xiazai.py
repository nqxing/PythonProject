import requests

url = 'https://ugcws.video.gtimg.com/uwMROfz2r57BIaQXGdGnC2dXPkUkRIJBQ0cfwk8ME3R3QUGD/gzc_1000035_0b53vibd4aacbiao5zgmt5pzpkwdh2vaepsa.f202110.mp4?sdtfrom=v3010&guid=13afba9b7625cf264ecfd2eb0b6b227e&vkey=FBEDAD040EA3DBF466F5192B54D562D5C0B486E09A1C8E7FB2A62A7021A5A8382EDCBD33317A99EF1F80E47907D39D2DA95A75B4409536E2637988419DCB7B2A7FFE3BE37ABE43652B2BC1CB9369CF15E70BA3B32D12DC8FCBAF6CDA168888116B09BDF96B56B06148CDFB6764B981DD7F7E161D07332E15123F348A93CC3CA4&platform=2'

img = requests.get(url)

print(img.status_code)

with open("1.mp4", "wb") as f:
    f.write(img.content)
# def get():
#     url = 'http://127.0.0.1:2222/api/douyin/parse?url=1233&name=nnn'
#     r = requests.get(url)
#     print(r.text)
#
# def post():
#     dict = {
#         'page' : 1,
#         'row' : 10
#     }
#     url = 'http://127.0.0.1:2222/test_1.0'
#     r = requests.post(url, data=dict)
#     print(r.text)
#
# # get()
# post()
# import json
# get_Data = 'age=122323&name=nnnnnn'
# get_Data = json.loads(get_Data)
# print(get_Data)