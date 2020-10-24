#-*- coding:utf-8 -*-
from pyquery import PyQuery as pq

with open('html.txt', encoding='utf-8') as read_file:
    content = read_file.read().strip()

html = content
# print(html)
print('-----------------------------')
# html = requests.get(url, headers = headers)
# html.encoding = 'gbk'
# items = pq(html)('.m-itemlist div div:nth-child(1) div').items()
items = pq(html)('.m-itemlist .g-clearfix .items .item').items()
# print(items)
for item in items:
    # pic_url = item('.pic-box-inner .pic a img').attr('src')
    items_pic = "http:" + item('.pic-box-inner .pic .pic-link .img').attr('data-src')
    items_price = item('.price').text()
    items_sales = item('.deal-cnt').text()
    items_name = item('.J_ClickStat').text()
    shop_name = item('.shopname').text()
    shop_address = item('.location').text()
    print(items_pic, items_price, items_sales, items_name, shop_name, shop_address)