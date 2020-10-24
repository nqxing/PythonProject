import requests
import xlwt
headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36'
        }
dict = {"type":"free","bigType":"17112917BDorMpYt","smallType":"","keyWord":"","pageSize":1000,"pageNumber":1,"sort":"zonghe"}

r = requests.post('http://demo.3dmomoda.com:3000/model/queryModels', headers = headers, data=dict).json()
book = xlwt.Workbook()  # 新建一个excel对象
sheet = book.add_sheet('机房')  # 添加一个sheet页
sheet.write(0, 0, '名称')
sheet.write(0, 1, 'id')
sheet.write(0, 2, '模型url')
mlist = r['content']['list']
for i in range(len(mlist)):
    name = mlist[i]['name']
    model_id = mlist[i]['modelId']
    model_url = 'http://model.3dmomoda.com/models/{}/0/gltf/'.format(mlist[i]['modelId'])
    sheet.write(i+1, 0, name)
    sheet.write(i+1, 1, model_id)
    sheet.write(i+1, 2, model_url)
book.save('免费模型-机房.xls')
