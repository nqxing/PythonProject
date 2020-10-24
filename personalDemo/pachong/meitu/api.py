from flask import Flask, jsonify, request
import json
import pymysql
from random import randint  # 随机函数
import traceback

# 106.13.81.161  localhost
host = 'localhost'
pwd = 'BKKPHbkkpn3v76y461yt8ncn0'

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'NOT FOUND'}), 404

@app.route("/meitu/zuixin", methods=["GET"])
def zuixin():
    db = pymysql.connect(host=host, user='root', password=pwd, port=3306,
                         db='meitu')  # 连接数据库
    cursor = db.cursor()
    return_dict = {'code': 200, 'msg': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.get_data() is None:
        return_dict['code'] = 400
        return_dict['msg'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    try:
        if 'page' in request.args and 'row' in request.args:
            page = int(request.args['page'])# 传参，前面的是变量，括号里面是key
            row = int(request.args['row'])
            row_list = []
            if row == 20:
                sqls = ''' select cname, beg_id from meitulu_f WHERE id != 5 '''
                cursor.execute(sqls)
                beg_ids = cursor.fetchall()
                # db.close()
                for beg_id in beg_ids:
                    sqlss = ''' select * from meitulu WHERE classify = "{}" AND id >= {} limit {}'''.format(beg_id[0], beg_id[1], page)
                    cursor.execute(sqlss)
                    t = cursor.fetchall()
                    r = t[-1]
                    a_rows = {}
                    a_rows['id'] = r[0]
                    a_rows['title'] = r[1]
                    a_rows['num'] = r[2]
                    a_rows['jigou'] = r[3]
                    a_rows['mote'] = r[4]
                    a_rows['tags'] = r[5]
                    purls = r[6].split('0.jpg')
                    a_rows['purl'] = '{}1.jpg'.format(purls[0])
                    row_list.append(a_rows)
                return_dict['result'] = row_list
    except:
        print(traceback.format_exc())
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/meitu/tuijian", methods=["GET"])
def tuijian():
    db = pymysql.connect(host=host, user='root', password=pwd, port=3306,
                         db='meitu')  # 连接数据库
    cursor = db.cursor()
    return_dict = {'code': 200, 'msg': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.get_data() is None:
        return_dict['code'] = 400
        return_dict['msg'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    if 'row' in request.args:
        try:
            row = int(request.args['row'])
            row_list = []
            sqls = ''' select beg_id, sta_id, sum_num from meitulu_f '''
            cursor.execute(sqls)
            beg_ids = cursor.fetchall()
            # db.close()
            randints = []
            for id in beg_ids:
                rans = []
                rans.append(id[0])
                rans.append(id[1] + id[2])
                randints.append(rans)
            for i in range(row):
                tids = randints[randint(0, len(randints) - 1)]
                tid = randint(tids[0], tids[1])
                sqlss = ''' select * from meitulu WHERE id = {} '''.format(tid)
                cursor.execute(sqlss)
                t = cursor.fetchall()
                # db.close()
                r = t[0]
                a_rows = {}
                a_rows['id'] = r[0]
                a_rows['title'] = r[1]
                a_rows['num'] = r[2]
                a_rows['jigou'] = r[3]
                a_rows['mote'] = r[4]
                a_rows['tags'] = r[5]
                purls = r[6].split('0.jpg')
                a_rows['purl'] = '{}1.jpg'.format(purls[0])
                row_list.append(a_rows)
            return_dict['result'] = row_list
        except:
            print(traceback.format_exc())
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/meitu/get_pic", methods=["GET"])
def get_pic():
    return_dict = {'code': 200, 'msg': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.get_data() is None:
        return_dict['code'] = 400
        return_dict['msg'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    if 'id' in request.args:
        try:
            id = int(request.args['id'])# 传参，前面的是变量，括号里面是key
            rows = get_pics(id)
            row_list = []
            for r in rows:
                a_rows = {}
                a_rows['title'] = r[1]
                a_rows['purl'] = r[2]
                row_list.append(a_rows)
            return_dict['result'] = row_list
        except:
            print(traceback.format_exc())
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/meitu/get_classify", methods=["GET"])
def get_classify():
    return_dict = {'code': 200, 'msg': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.get_data() is None:
        return_dict['code'] = 400
        return_dict['msg'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    if 'index' in request.args:
        try:
            id = int(request.args['index'])# 传参，前面的是变量，括号里面是key
            if id == 1:
                rows = get_classifys()
                row_list = []
                for r in rows:
                    a_rows = {}
                    a_rows['cname'] = r[0]
                    a_rows['curl'] = r[1]
                    row_list.append(a_rows)
                return_dict['result'] = row_list
        except:
            print(traceback.format_exc())
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/meitu/get_classify_pic", methods=["GET"])
def get_classify_pic():
    db = pymysql.connect(host=host, user='root', password=pwd, port=3306,
                         db='meitu')  # 连接数据库
    cursor = db.cursor()
    return_dict = {'code': 200, 'msg': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.get_data() is None:
        return_dict['code'] = 400
        return_dict['msg'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    try:
        if 'page' in request.args and 'row' in request.args and 'classify' in request.args:
            page = int(request.args['page'])
            row = int(request.args['row'])
            classify = request.args['classify']
            row_list = []
            sqls = ''' select beg_id from meitulu_f WHERE cname = "{}" '''.format(classify)
            cursor.execute(sqls)
            beg_ids = cursor.fetchall()
            # db.close()
            s = (page - 1) * row + beg_ids[0][0]
            e = s + row - 1
            rows = get_zuixins(s, e)
            for r in rows:
                a_rows = {}
                a_rows['id'] = r[0]
                a_rows['title'] = r[1]
                a_rows['num'] = r[2]
                a_rows['jigou'] = r[3]
                a_rows['mote'] = r[4]
                a_rows['tags'] = r[5]
                purls = r[6].split('0.jpg')
                a_rows['purl'] = '{}1.jpg'.format(purls[0])
                row_list.append(a_rows)
            return_dict['result'] = row_list
    except:
        print(traceback.format_exc())

    return json.dumps(return_dict, ensure_ascii=False)

def get_zuixins(s, e):
    db = pymysql.connect(host=host, user='root', password=pwd, port=3306,
                         db='meitu')  # 连接数据库
    cursor = db.cursor()
    sql = 'select * from meitulu where id between {} and {};'.format(s, e)
    cursor.execute(sql)
    rows = cursor.fetchall()
    # db.close()
    return rows

def get_pics(id):
    db = pymysql.connect(host=host, user='root', password=pwd, port=3306,
                         db='meitu')  # 连接数据库
    cursor = db.cursor()
    sql = 'select * from meitulu_p where pid = {};'.format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    # db.close()
    return rows

def get_classifys():
    db = pymysql.connect(host=host, user='root', password=pwd, port=3306,
                         db='meitu')  # 连接数据库
    cursor = db.cursor()
    sql = 'select cname, curl from meitulu_f '
    cursor.execute(sql)
    rows = cursor.fetchall()
    # db.close()
    return rows

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=65535)

# get_pics(1)
# get_rows(1, 5)