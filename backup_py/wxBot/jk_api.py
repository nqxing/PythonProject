from flask import Flask, jsonify, request
import json
import traceback
from flask_cors import *
import MySQLdb

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'NOT FOUND'}), 404

@app.route("/hongbao/get_list", methods=["GET"])
def get_list():
    return_dict = {'code': 200, 'msg': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.get_data() is None:
        return_dict['code'] = 400
        return_dict['msg'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    try:
        if 'page' in request.args and 'pagesize' in request.args and 'is_jk' in request.args:
            page = int(request.args['page'])# 传参，前面的是变量，括号里面是key
            pagesize = int(request.args['pagesize'])
            is_jk = request.args['is_jk']
            # print(page, pagesize, is_jk)
            row_list = []
            if is_jk == 'no':
                lists = get_list_no()
                row = len(lists)
                p = row // pagesize
                # print(lists, row, p)
                if row < pagesize:
                    index = (page - 1) * pagesize
                    # print(index)
                    # db.close()
                    for i in range(index, page*row):
                        a_rows = {}
                        a_rows['yet'] = lists[i][0]
                        a_rows['yet_max'] = lists[i][1]
                        a_rows['alink'] = lists[i][2]
                        row_list.append(a_rows)
                    return_dict['result'] = row_list
                elif p >= page:
                    index = (page - 1) * pagesize
                    # print(index)
                    # db.close()
                    for i in range(index, page * pagesize):
                        a_rows = {}
                        a_rows['yet'] = lists[i][0]
                        a_rows['yet_max'] = lists[i][1]
                        a_rows['alink'] = lists[i][2]
                        row_list.append(a_rows)
                    return_dict['result'] = row_list
                else:
                    if row % pagesize != 0:
                        if p + 1 == page:
                            index = p * pagesize
                            y = row % pagesize
                            for i in range(index, index + y):
                                a_rows = {}
                                a_rows['yet'] = lists[i][0]
                                a_rows['yet_max'] = lists[i][1]
                                a_rows['alink'] = lists[i][2]
                                row_list.append(a_rows)
                            return_dict['result'] = row_list
                        else:
                            return_dict['result'] = []

            if is_jk == 'yes':
                lists = get_list_yes()
                row = len(lists)
                p = row // pagesize
                # print(lists, row, p)
                if row < pagesize:
                    index = (page - 1) * pagesize
                    # print(index)
                    # db.close()
                    for i in range(index, page*row):
                        a_rows = {}
                        a_rows['bianhao'] = lists[i][0]
                        a_rows['yet'] = lists[i][1]
                        a_rows['yet_max'] = lists[i][2]
                        row_list.append(a_rows)
                    return_dict['result'] = row_list
                elif p >= page:
                    index = (page - 1) * pagesize
                    # print(index)
                    # db.close()
                    for i in range(index, page * pagesize):
                        a_rows = {}
                        a_rows['bianhao'] = lists[i][0]
                        a_rows['yet'] = lists[i][1]
                        a_rows['yet_max'] = lists[i][2]
                        row_list.append(a_rows)
                    return_dict['result'] = row_list
                else:
                    if row % pagesize != 0:
                        if p + 1 == page:
                            index = p * pagesize
                            y = row % pagesize
                            for i in range(index, index + y):
                                a_rows = {}
                                a_rows['bianhao'] = lists[i][0]
                                a_rows['yet'] = lists[i][1]
                                a_rows['yet_max'] = lists[i][2]
                                row_list.append(a_rows)
                            return_dict['result'] = row_list
                        else:
                            return_dict['result'] = []

    except:
        print(traceback.format_exc())
    return json.dumps(return_dict, ensure_ascii=False)

def get_list_no():
    obj = MysqlSearch()
    return obj.return_jk_no()
def get_list_yes():
    obj = MysqlSearch()
    return obj.return_jk_yes()

class MysqlSearch(object):
    def __init__(self):
        self.get_conn()

    def get_conn(self):
        try:
            self.con = MySQLdb.connect(
                host='localhost',
                # host='122.51.67.37',
                port=3306,
                user='root',
                # passwd='mm123456',
                passwd='MUGVHmugvtwja116ye38b1jhb',
                db='eleme',
                charset='utf8'
            )
        except MySQLdb.Error as e:
            print('Error %d:%s' % (e.args[0], e.args[1]))

    def close_conn(self):
        try:
            if self.con:
                self.con.close()
        except MySQLdb.Error as e:
            print('Error: %s' % e)

    def return_jk_no(self):
        sqls = ''' select yet, yet_max, alink from eleme_group_sn WHERE state = 'yes' ORDER BY yet DESC '''
        # 找到cursor
        cursor = self.con.cursor()
        # 执行SQL
        cursor.execute(sqls)
        lists = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return lists

    def return_jk_yes(self):
        sqls = ''' select bianhao, yet, yet_max from eleme_group_sn WHERE state = 'no' ORDER BY yet DESC '''
        # 找到cursor
        cursor = self.con.cursor()
        # 执行SQL
        cursor.execute(sqls)
        lists = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return lists

    # def add_one(self):
    #     try:
    #         # 准备SQL
    #         sql = "INSERT INTO news (title,img_url,content,news_type) VALUE " \
    #               "(%s,%s,%s,%s);"
    #         # 获取链接和cursor
    #         cursor = self.con.cursor()
    #         # 提交数据到数据库
    #         cursor.execute(sql, ('标题1', '/static/img/news/01.png', '新闻内容1', '推荐',))
    #         # 提交事务
    #         self.con.commit()
    #     except:
    #         self.con.rollback()
    #     # 关闭cursor和连接
    #     cursor.close()
    #     self.close_conn()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
