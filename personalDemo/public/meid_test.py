import requests

def get_token():
    payload_access_token={
        'grant_type':'client_credential',
        'appid':'wx783e5537bd7ee69b',
        'secret':'d56b169fa56b790e9e959b80d6a81e7c'
    }
    token_url='https://api.weixin.qq.com/cgi-bin/token'
    r=requests.get(token_url,params=payload_access_token)
    print(r.text)
    dict_result= (r.json())
    return dict_result['access_token']

token = "32_rznDznZDxU5CJ6ajKxTR2Khe4KNTQgV0RvaUV7E06U10PoJkOMpl4CDhH07V97pGvLof9mLoN-oBUZOnZOKD3jI9AC8l070RHXoANR1-c0mBLXhd-VZ6UcFty8_gk2oWCpdp2hS08LJOIC1iJSCgADAXGQ"
# token = get_token()

#获取上传文件的media_ID
#群发图片的时候，必须使用该api提供的media_ID
def get_media_ID(path):
    img_url='https://api.weixin.qq.com/cgi-bin/material/add_material'
    payload_img={
        'access_token':token,
        'type':'image'
    }
    data ={'media':open(path,'rb')}
    r=requests.post(url=img_url,params=payload_img,files=data)
    dict =r.json()
    return dict['media_id']

# print(get_media_ID(r"E:\1.jpg"))