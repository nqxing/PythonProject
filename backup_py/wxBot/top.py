import sqlite3
import re

# conn = sqlite3.connect(r'C:\PythonProject\eleme\config\eleme.db')
conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\eleme.db')
#创建一个游标 curson
cursor = conn.cursor()


def sort_key(s):
    if s:
        try:
            c = re.findall(r'\d+$', s)[0]
        except:
            c = -1
        return int(c)

def strsort(alist):
    alist.sort(key=sort_key, reverse=True)
    return alist

sum_dic = {}

cursor.execute("select DISTINCT ename from eleme_amount")
vaus = cursor.fetchall()

def top_all():
    for v in range(len(vaus)):
        sum_list = []
        sum_list.append(vaus[v][0])
        cursor.execute("select amount, esource  from eleme_amount WHERE ename = '{}' ".format(vaus[v][0]))
        vauss = cursor.fetchall()
        sum_list.append(len(vauss))
        qq_num = 0
        wx_num = 0
        int_sum = 0
        float_sum = 0
        for va in vauss:
            if va[1] == 'wx':
                wx_num += 1
                if '.' in va[0]:
                    float_sum += float(va[0])
                else:
                    int_sum += int(va[0])
            if va[1] == 'qq':
                qq_num += 1
                if '.' in va[0]:
                    float_sum += float(va[0])
                else:
                    int_sum += int(va[0])
        if int_sum == 0:
            sum_amount = float_sum
            sum_amount = '%.1f' % sum_amount
        elif float_sum == 0:
            sum_amount = int_sum
        else:
            sum_amount = float_sum + int_sum
            sum_amount = '%.1f' % sum_amount
        sum_list.append(sum_amount)
        sum_list.append(qq_num)
        sum_list.append(wx_num)
        # print(v[0], float_sum, int_sum)
        # sum_list.append('【{}】共抢了{}个红包，累计{}元（其中大包群{}个，监控系统{}个）'.format(vaus[v][0], len(vauss), sum_amount, qq_num, wx_num))
        sum_dic['{}_{}'.format(v+1, len(vauss))] = sum_list
    sum_lists = strsort(list(sum_dic.keys()))
    return sum_lists

def top_qq():
    for v in range(len(vaus)):
        sum_list = []
        sum_list.append(vaus[v][0])
        cursor.execute("select amount, esource, bianhao  from eleme_amount WHERE ename = '{}' ".format(vaus[v][0]))
        vauss = cursor.fetchall()
        sum_list.append(len(vauss))
        qq_num = 0
        wx_num = 0
        int_sum = 0
        float_sum = 0
        for va in vauss:
            if len(va[2]) == 4:
                if va[1] == 'wx':
                    wx_num += 1
                    if '.' in va[0]:
                        float_sum += float(va[0])
                    else:
                        int_sum += int(va[0])
                if va[1] == 'qq':
                    qq_num += 1
                    if '.' in va[0]:
                        float_sum += float(va[0])
                    else:
                        int_sum += int(va[0])
            else:
                print(va[2])
        if int_sum == 0:
            sum_amount = float_sum
            sum_amount = '%.1f' % sum_amount
        elif float_sum == 0:
            sum_amount = int_sum
        else:
            sum_amount = float_sum + int_sum
            sum_amount = '%.1f' % sum_amount
        sum_list.append(sum_amount)
        sum_list.append(qq_num)
        sum_list.append(wx_num)
        # print(v[0], float_sum, int_sum)
        # sum_list.append('【{}】共抢了{}个红包，累计{}元（其中大包群{}个，监控系统{}个）'.format(vaus[v][0], len(vauss), sum_amount, qq_num, wx_num))
        sum_dic['{}_{}'.format(v+1, len(vauss))] = sum_list
    sum_lists = strsort(list(sum_dic.keys()))
    for s in sum_lists:
        print(sum_dic[s])

all_vas = top_all()
id = 1
all_str = ''
for a in all_vas:
    a_str = 'No.{} [{}] 累计领取{}个 合计{}元（大包群{}个，控包系统{}个）\n\n'.format(id, sum_dic[a][0], sum_dic[a][1], sum_dic[a][2], sum_dic[a][3], sum_dic[a][4])
    all_str += a_str
    id += 1
print(all_str)