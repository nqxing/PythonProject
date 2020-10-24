import requests
dict = {
    "type": "wz",
    "hero_id": "154",
    "hero_name": "花木兰",
    "skin_url": "https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/154/154-bigskin-1.jpg",
    "skin_name": "花木兰 传说之刃",
}
r = requests.post("http://127.0.0.1:8000/wall/", data=dict)
print(r.status_code)
print(r.text)