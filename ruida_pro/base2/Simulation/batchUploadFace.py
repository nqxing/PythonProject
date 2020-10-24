import os, shutil
import xlrd
from xlutils.copy import copy
import requests

path = r'D:\谷歌下载文件夹\老师人脸照片\头像'
new_path = r'D:\谷歌下载文件夹\老师人脸照片\生成的模板\老师'

def Template():
    tea_list = get_teaName()
    xls = xlrd.open_workbook(r'D:\谷歌下载文件夹\老师人脸照片\face.xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    x = 1
    for i in range(len(tea_list)):
        workNumber = tea_list[i]['workNumber']
        filenames = copy_files()
        if filenames[i].endswith('.jpg'):
            new_name = '{}.jpg'.format(workNumber)
            shutil.copyfile(os.path.join(path, filenames[i]), os.path.join(new_path, new_name))    #复制到新路径下，并重命名文件
        sheet.write(x, 0, workNumber)
        sheet.write(x, 1, workNumber + '.jpg')
        sheet.write(x, 2, '老师/{}.jpg'.format(workNumber))
        x += 1
    xlsc.save(r'D:\谷歌下载文件夹\老师人脸照片\生成的模板\face.xls')

def get_teaName():
    url = 'http://gateway2-test.591iq.com.cn/apps/base/school/teacher/list'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
        'AccessToken': 'A352CF0EE0698F2C7BC4A0C88C375C4A'
    }
    dict = {
        'rows': 100,
        'page': 1,
        'wordNumber': '',
        'schoolId': 6,
        'sort': False
    }
    r = requests.post(url, headers = headers, data=dict)
    return r.json()['data']['rows']
                                          #导入模块
def copy_files():                                           #定义函数名称
    filenames = os.listdir(path)
    return filenames

Template()
