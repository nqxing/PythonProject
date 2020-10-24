import json
import requests
def test1():
    dirPath = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\全国信息\\'
    f = open("{}天津市.txt".format(dirPath), "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    shengDic = eval(lines[0])
    beijing = {}
    beijing['天津'] = shengDic
    with open("天津市.txt", "w", encoding='utf-8') as f:
        f.write(str(beijing))


def test2():
    dirPath = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\txt\\'
    f = open("{}天津市.txt".format(dirPath), "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    shengDic = eval(lines[0])
    beijing = {}
    beijing['天津'] = shengDic
    with open("测试.txt", "w") as f:
        f.write(str(beijing))

def test3():
    f = open("测试.txt", "r")
    lines = f.readlines()  # 读取全部内容
    shengDic = eval(lines[0])
    # print(shengDic)
    # print(type(shengDic))
    json_str = json.dumps(shengDic,ensure_ascii=False)
    print(json_str)
    print(type(json_str))
    # beijing = {}
    # beijing['天津'] = shengDic
    # with open("天津市.txt", "w", encoding='utf-8') as f:
    #     f.write(str(beijing))

def fangtang():
    api = "https://pushbear.ftqq.com/sub"
    title = u"这是个通知标题"
    content = "这个许天态，不要自以为是，多和朋友交流。"
    data = {
        "sendkey": "7639-5d73449e8a2a1db47195cfc57210c07a",
        "text": title,
        "desp": content
    }
    res = requests.post(api, data=data)
    try:
        if res.json()["code"] == 0:
            print("发送成功")
        else:
            print(res.json())
            print("发送失败，重新发送")
    except:
        print('发送出错')

def suiList():
    import random
    foo = ['a', 'b', 'c', 'd', 'e']
    from random import choice
    print(choice(foo))

    # 2.使用python random模块的sample函数从列表中随机选择一组元素
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # 设置种子使得每次抽样结果相同
    # random.seed(10)
    slice = random.sample(list, 5)  # 从list中随机获取5个元素，作为一个片断返回
    print(slice)
    print(list)

def jiabandan():
    DayList = ['01','11','13','17','18','20','27']
    month = '12'
    jiabanLsit = []
    for j in DayList:
        jiabanLsit.append('%s月%s日加班审批单' % (month,j))
        jiabanLsit.append('2018-%s-%s 18:00' % (month,j))
        jiabanLsit.append('2018-%s-%s 20:00' % (month,j))
        jiabanLsit.append('因赶项目进度，所以加班')
    for jb in jiabanLsit:
        print(jb)
fangtang()