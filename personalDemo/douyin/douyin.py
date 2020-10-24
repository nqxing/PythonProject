# -*- encoding: utf-8 -*-
'''
@file    :   douyin.py
@Time    :   2019/08/24 10:16:18
@AuThor  :   [url=mailto:ermao@52pojie.cn]ermao@52pojie.cn[/url]
@version :   1.0
@Desc    :   抖音去水印解析
'''

# start
from flask import Flask, jsonify, request
import requests
import re

app = Flask(__name__)

header = {
    'User-Agent':
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Mobile Safari/537.36'
}


@app.route('/api')
def index():
    res = {'Hello': 'API !'}
    return jsonify(res)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'NOT FOUND'}), 404


@app.route('/api/douyin/parse')
def Video_parsing():
    if 'id' in request.args and len(request.args['id']) == 19:
        res = get_video(request.args['id'])
    elif 'url' in request.args and 'douyin.com' in request.args['url']:
        res = get_id(request.args['url'])
    else:
        res = {'error': 'Invalid Parameter'}
    return res


def get_id(url):
    try:
        r = requests.head(url)
        id = re.findall(r'/video/(\d{19})/', r.headers['Location'])[0]
        res = get_video(id)
        return res
    except Exception:
        return {'error': 'Invalid URL'}


def get_video(id):
    html = requests.get('https://www.iesdouyin.com/share/video/' + id +
                        '/?mid',
                        headers=header).text
    dytk_re = re.findall(r'dytk: "(\w{64})"', html)
    try:
        dtyk = dytk_re[0]
        res_json = requests.get(
            'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' +
            id + '&dytk=' + dtyk).json()
        temp_url = res_json['item_list'][0]['video']['play_addr']['url_list'][0]
        r = requests.head(temp_url, headers=header)
        real_addr = r.headers['Location']
        if '/video/m/' in real_addr:
            res = {
                'id': id,
                'uri': res_json['item_list'][0]['video']['vid'],
                'desc': res_json['item_list'][0]['desc'],
                'pic': res_json['item_list'][0]['video']['origin_cover']['url_list'][0],
                'gif': res_json['item_list'][0]['video']['dynamic_cover']['url_list'][0],
                'play_addr': real_addr
            }
            return res
    except Exception:
        return {'error': 'An exception occurred'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2222)