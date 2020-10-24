import time

dic = {454545:'tttttttttttt',0:'ssss'}
# print(dic.keys())
# print(dic[454545])

import re
line = '从PG One的“猪精粉“变回路人，“他就是一个懦夫！”'
# line = line.decode("utf8")
# string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),line)
# print(string)
#
# import string
# # i = "Hello, how ? are, daddy's you ! "
# i = '从PG One的“猪精粉“变回路人，“他就是一个懦夫！”'
# a = i.translate(str.maketrans('', '', string.punctuation))
# print(a)

import re

# 只保留中文、大小写字母和阿拉伯数字
reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
# text = "<>\(*芸%芸^)，,\\（-我@   ）&love=+《你》！【~我//""[们]】2{0}1.6~————、结/婚'吧:：！这.!！_#？?（）个‘’“”￥$主|意()不。错……！"
print(re.sub(reg, '', line))
time.sleep(5)