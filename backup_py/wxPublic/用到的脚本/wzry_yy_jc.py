import shutil,os
import re,json
import requests
from xpinyin import Pinyin
def reture_dir(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return dirs
def return_files(file_dir, fname):
    files = []
    dirs = reture_dir(file_dir)
    for d in dirs:
        fnames = str(d)
        m = bool(re.search(fname, fnames, re.IGNORECASE))
        if m:
            files.append(fnames)
    return files
num = 1
f = open(r"hero.txt", "r", encoding='utf-8')
lines = f.readlines()  # 读取全部内容
hero = '%s' % lines[0].replace("'", '"')
hero_dic = json.loads('{}'.format(hero))

# hero_dic = {'花木兰': 'huamulan'}
# print(hero_dic)
#
hero_ids = list(hero_dic.keys())
for i in hero_ids:
    path1 = r'D:\王者荣耀语音包\移动后\{}'.format(i)
    path2 = r'{}\模拟战语音包'.format(path1)
    folder = os.path.exists(path1)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path1)  # makedirs 创建文件时如果路径不存在会创建这个路径
    folder1 = os.path.exists(path2)
    if not folder1:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path2)  # makedirs 创建文件时如果路径不存在会创建这个路径
    files = return_files(r"D:\王者荣耀语音包\被移动", hero_dic[i])
    for f in files:
        if 'MN_' in f:
            shutil.move(r"D:\王者荣耀语音包\被移动\{}".format(f), path2)
        else:
            # 移动文件夹
            shutil.move(r"D:\王者荣耀语音包\被移动\{}".format(f), path1)
    print('已移动{}个英雄'.format(num))
    num+=1

# p = Pinyin()
# new_dic = {}
# r = requests.get('http://game.gtimg.cn/images/yxzj/web201706/js/heroid.js')
# r.encoding = 'gbk'
# heros = re.findall('module_exports = {(.*?)};', r.text, re.S)
# hero = '{%s}' % heros[0].replace("'", '"')
# hero_dic = json.loads('{}'.format(hero))
# # hero_dic = {'154': '花木兰', '141': '貂蝉',}
# hero_ids = list(hero_dic.keys())
#
# for i in hero_ids:
#     if i != '155':
#         new_dic[hero_dic[i]] = p.get_pinyin(u"{}".format(hero_dic[i]), '')
# print(new_dic)
# with open("hero.txt", "w", encoding='utf-8') as f:
#     f.write(str(new_dic))

# print(return_files(r"D:\王者荣耀语音包\被移动", "huamulan"))
# print(bool(re.search("huamulan", "Hero_HuaMuLan_Skin_C_SFX", re.IGNORECASE)))
