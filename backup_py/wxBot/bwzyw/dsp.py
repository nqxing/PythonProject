import requests

url = 'https://analyse.layzz.cn//lyz/miniMsgUnLoadAnalyse'
headers = {
    'Referer': 'https://appservice.qq.com/1110141096/1.0.0/page-frame.html',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; 16th Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045008 Mobile Safari/537.36 QQ/MiniApp',
    'content-type': 'application/json',
    'Host': 'analyse.layzz.cn'
}
links = 'https://b23.tv/av95473051'
dict = {
	"code":"060bf7148abefedc4538b360e184e142",
	"programType":88,
	"link":links,
	"nickName":"",
	"avatarUrl":"",
	"reqSource":1
}
r = requests.post(url, headers=headers, json=dict)
print(r.text)