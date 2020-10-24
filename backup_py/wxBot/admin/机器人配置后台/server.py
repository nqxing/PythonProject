from flask import Flask, jsonify, request
import json
import traceback
from flask_cors import *
import MySQLdb
import sqlite3
import hashlib
import random, string
import os

pwd = b'2020'

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'NOT FOUND'}), 404

@app.route('/wxBot1/upHtmlName', methods=['POST'])
def up_html_name():
    if request.method == 'POST':
        try:
            token = request.form.get('token')
            if token != len(token) and token == hashlib.md5(pwd).hexdigest():
                num = string.ascii_letters + string.digits
                new_name = "".join(random.sample(num, 10))
                f = open(r"name.txt", "r", )
                name = f.readlines()[0]  # 读取全部内容
                filepath = "{}.html".format(name)
                oldname = os.path.splitext(filepath)
                os.rename(oldname[0] + oldname[1], new_name + ".html")
                with open("name.txt", "w", encoding='utf-8') as f:
                    f.write(new_name)
                f = open(r"name.txt", "r", )
                name1 = f.readlines()[0]  # 读取全部内容
                if name1 == new_name:
                    return json.dumps({'msg': '操作成功'}, ensure_ascii=False)
                else:
                    return json.dumps({'msg': '操作失败'}, ensure_ascii=False)
            else:
                return json.dumps({'msg': '令牌错误'}, ensure_ascii=False)
        except:
            print(traceback.format_exc())
            return json.dumps({'code': -1, 'msg': '操作异常'}, ensure_ascii=False)

@app.route('/wxBot1/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            login = request.form.get('login')
            if len(login) != 0:
                b = bytes(login, encoding='utf-8')
                if hashlib.md5(b).hexdigest() == '6351bf9dce654515bf1ddbd6426dfa97':
                    f = open(r"name.txt", "r", )
                    name = f.readlines()[0]  # 读取全部内容
                    return json.dumps({'code': 0, 'msg': '验证成功，正在跳转..', 'url': 'http://122.51.67.37/wxBot1-admin/{}.html?token={}'.format(name, hashlib.md5(pwd).hexdigest())}, ensure_ascii=False)
                else:
                    return json.dumps({'code': -1, 'msg': '密码错误'}, ensure_ascii=False)
            else:
                return json.dumps({'code': -1, 'msg': '密码不能为空'}, ensure_ascii=False)
        except:
            print(traceback.format_exc())
            return json.dumps({'code': -1, 'msg': '操作异常'}, ensure_ascii=False)

@app.route('/wxBot1/updateDakaState', methods=['POST'])
def up_dakaState():
    if request.method == 'POST':
        try:
            req_dict = request.form.to_dict()
            if 'UpDakaState' in req_dict and len(req_dict['UpDakaState']) != 0:
                if 'token' in req_dict and req_dict['token'] == hashlib.md5(pwd).hexdigest():
                    state = update_daka_state(req_dict)
                    if state['state'] == 0:
                        return json.dumps({'msg': state['result']}, ensure_ascii=False)
                    else:
                        return json.dumps({'msg': state['result']}, ensure_ascii=False)
                else:
                    return json.dumps({'msg': '令牌错误'}, ensure_ascii=False)
            else:
                return json.dumps({'msg': '所有项都不能为空'}, ensure_ascii=False)
        except:
            print(traceback.format_exc())
            return json.dumps({'msg': '操作异常'}, ensure_ascii=False)

@app.route('/wxBot1/updateSignState', methods=['POST'])
def up_signState():
    if request.method == 'POST':
        try:
            req_dict = request.form.to_dict()
            if 'UpSignState' in req_dict and len(req_dict['UpSignState']) != 0:
                if 'token' in req_dict and req_dict['token'] == hashlib.md5(pwd).hexdigest():
                    state = update_sign_state(req_dict)
                    if state['state'] == 0:
                        return json.dumps({'msg': state['result']}, ensure_ascii=False)
                    else:
                        return json.dumps({'msg': state['result']}, ensure_ascii=False)
                else:
                    return json.dumps({'msg': '令牌错误'}, ensure_ascii=False)
            else:
                return json.dumps({'msg': '所有项都不能为空'}, ensure_ascii=False)
        except:
            print(traceback.format_exc())
            return json.dumps({'msg': '操作异常'}, ensure_ascii=False)

@app.route('/wxBot1/daka', methods=['GET', 'POST'])
def get_daka():
    if request.method == 'GET':
        return_dict = {'code': 200, 'msg': '处理成功', 'result': False}
        try:
            lists = select_daka()
            results = []
            if lists:
                for list in lists:
                    for l in list:
                        results.append(l)
            if results:
                return_dict['result'] = results
        except:
            print(traceback.format_exc())
        return json.dumps(return_dict, ensure_ascii=False)
    if request.method == 'POST':
        try:
            req_dict = request.form.to_dict()
            if 'token' in req_dict and req_dict['token'] == hashlib.md5(pwd).hexdigest():
                req_dict.pop('token')
                for r in req_dict.keys():
                    if len(req_dict[r]) == 0:
                        return json.dumps({'msg': '所有项都不能为空'}, ensure_ascii=False)
                state = update_daka(req_dict)
                if state == 0:
                    return json.dumps({'msg': '操作成功'}, ensure_ascii=False)
                else:
                    return json.dumps({'msg': '操作失败'}, ensure_ascii=False)
            else:
                return json.dumps({'msg': '令牌错误'}, ensure_ascii=False)
        except:
            print(traceback.format_exc())
            return json.dumps({'msg': '操作异常'}, ensure_ascii=False)

@app.route('/wxBot1/eleme', methods=['GET', 'POST'])
def get_eleme():
    if request.method == 'GET':
        return_dict = {'code': 200, 'msg': '处理成功', 'result': False}
        try:
            lists = select_eleme()
            results = []
            if lists:
                for list in lists:
                    results.append({'text': list[0], 'text_info': list[1]})
            if results:
                return_dict['result'] = results
        except:
            print(traceback.format_exc())
        return json.dumps(return_dict, ensure_ascii=False)
    if request.method == 'POST':
        try:
            req_dict = request.form.to_dict()
            if 'token' in req_dict and req_dict['token'] == hashlib.md5(pwd).hexdigest():
                req_dict.pop('token')
                for r in req_dict.keys():
                    if len(req_dict[r]) == 0:
                        return json.dumps({'msg': '所有项都不能为空'}, ensure_ascii=False)
                state = update_eleme(req_dict)
                if state == 0:
                    return json.dumps({'msg': '操作成功'}, ensure_ascii=False)
                else:
                    return json.dumps({'msg': '操作失败'}, ensure_ascii=False)
            else:
                return json.dumps({'msg': '令牌错误'}, ensure_ascii=False)
        except:
            print(traceback.format_exc())
            return json.dumps({'msg': '操作异常'}, ensure_ascii=False)

def select_daka():
    obj = SqliteSearch()
    return obj.return_daka()
def update_daka(daka_dict):
    obj = SqliteSearch(db_dict=daka_dict)
    return obj.update_daka()

def select_eleme():
    obj = SqliteSearch()
    return obj.return_eleme()
def update_eleme(eleme_dict):
    obj = SqliteSearch(db_dict=eleme_dict)
    return obj.update_eleme()

def update_daka_state(state_dict):
    obj = SqliteSearch(db_dict=state_dict)
    return obj.up_daka_state()
def update_sign_state(state_dict):
    obj = SqliteSearch(db_dict=state_dict)
    return obj.up_sign_state()

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

    def return_daka(self):
        sqls = ''' select * from daka_text '''
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

class SqliteSearch(object):
    def __init__(self, db_dict=None):
        self.get_conn()
        if db_dict:
            self.db_dict = db_dict

    def get_conn(self):
        try:
            self.con = sqlite3.connect(r"C:\PythonProject\wxBot\config\eleme.db")
            # self.con = sqlite3.connect(r"D:\wxBot1\config\eleme.db")
            # self.con = sqlite3.connect(r"C:\PythonProject\wxBot1\config\eleme_test.db")
        except MySQLdb.Error as e:
            print('Error %d:%s' % (e.args[0], e.args[1]))

    def close_conn(self):
        try:
            if self.con:
                self.con.close()
        except MySQLdb.Error as e:
            print('Error: %s' % e)

    def return_daka(self):
        sqls = ''' select * from daka_text '''
        # 找到cursor
        cursor = self.con.cursor()
        # 执行SQL
        cursor.execute(sqls)
        lists = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return lists

    def update_daka(self):
        # 找到cursor
        cursor = self.con.cursor()
        if self.db_dict:
            for r in self.db_dict.keys():
                sqls = ''' UPDATE daka_text SET {} = "{}" '''.format(r, self.db_dict[r])
                # 执行SQL
                cursor.execute(sqls)
            self.con.commit()
            cursor.close()
            self.close_conn()
            return 0
        else:
            cursor.close()
            self.close_conn()
            return -1

    def return_eleme(self):
        sqls = ''' select text,text_info from eleme_text '''
        # 找到cursor
        cursor = self.con.cursor()
        # 执行SQL
        cursor.execute(sqls)
        lists = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return lists

    def update_eleme(self):
        # 找到cursor
        cursor = self.con.cursor()
        if self.db_dict:
            for r in self.db_dict.keys():
                sqls = ''' UPDATE eleme_text SET text = "{}" WHERE id  = {} '''.format(self.db_dict[r], int(r.split('-')[-1]))
                # 执行SQL
                cursor.execute(sqls)
            self.con.commit()
            cursor.close()
            self.close_conn()
            return 0
        else:
            cursor.close()
            self.close_conn()
            return -1

    def up_daka_state(self):
        # 找到cursor
        cursor = self.con.cursor()
        if self.db_dict:
            if 'UpDakaState' in self.db_dict:
                cursor.execute("select state from daka_vip WHERE wx_beizhu = '{}' ".format(self.db_dict['UpDakaState']))
                value = cursor.fetchall()
                if value:
                    if value[0][0] == 'yes':
                        state = 'no'
                    else:
                        state = 'yes'
                    sqls = ''' UPDATE daka_vip SET state = "{}" WHERE wx_beizhu  = "{}" '''.format(state, self.db_dict['UpDakaState'])
                    # 执行SQL
                    cursor.execute(sqls)
                    self.con.commit()
                else:
                    return {'state': -1, 'result': '{}不存在'.format(self.db_dict['UpDakaState'])}
            cursor.execute("select state from daka_vip WHERE wx_beizhu = '{}' ".format(self.db_dict['UpDakaState']))
            value = cursor.fetchall()[0][0]
            cursor.close()
            self.close_conn()
            return {'state':0, 'result':'{}的打卡状态已修改为{}'.format(self.db_dict['UpDakaState'], value)}
        else:
            cursor.close()
            self.close_conn()
            return {'state':-1, 'result':'更新失败'}

    def up_sign_state(self):
        # 找到cursor
        cursor = self.con.cursor()
        if self.db_dict:
            if 'UpSignState' in self.db_dict:
                cursor.execute("select state from eleme_sign WHERE wx_beizhu = '{}' ".format(self.db_dict['UpSignState']))
                value = cursor.fetchall()
                if value:
                    if value[0][0] == 'yes':
                        state = 'no'
                    else:
                        state = 'yes'
                    sqls = ''' UPDATE eleme_sign SET state = "{}" WHERE wx_beizhu  = "{}" '''.format(state, self.db_dict[
                        'UpSignState'])
                    # 执行SQL
                    cursor.execute(sqls)
                    self.con.commit()
                else:
                    return {'state': -1, 'result': '{}不存在'.format(self.db_dict['UpSignState'])}
            cursor.execute("select state from eleme_sign WHERE wx_beizhu = '{}' ".format(self.db_dict['UpSignState']))
            value = cursor.fetchall()[0][0]
            cursor.close()
            self.close_conn()
            return {'state': 0, 'result': '{}的饿了么签到状态已修改为{}'.format(self.db_dict['UpSignState'], value)}
        else:
            cursor.close()
            self.close_conn()
            return {'state': -1, 'result': '更新失败'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
