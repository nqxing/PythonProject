# 把31一个省信息合并成一个文件
import os
dirPath = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\全国信息\\'
dirsList = ['上海', '云南省', '内蒙古自治区', '北京', '吉林省', '四川省', '天津', '宁夏回族自治区', '安徽省', '山东省', '山西省', '广东省', '广西壮族自治区', '新疆维吾尔自治区',
            '江苏省', '江西省', '河北省', '河南省', '浙江省', '海南省', '湖北省', '湖南省', '甘肃省', '福建省', '西藏自治区', '贵州省', '辽宁省', '重庆', '陕西省', '青海省', '黑龙江省']
dirsList1 = ['上海市', '云南省', '内蒙古自治区', '北京市', '吉林省', '四川省', '天津市', '宁夏回族自治区', '安徽省', '山东省', '山西省', '广东省', '广西壮族自治区', '新疆维吾尔自治区',
            '江苏省', '江西省', '河北省', '河南省', '浙江省', '海南省', '湖北省', '湖南省', '甘肃省', '福建省', '西藏自治区', '贵州省', '辽宁省', '重庆市', '陕西省', '青海省', '黑龙江省']
countryDic = {}
# for dName in os.listdir(dirPath):
#     name = dName.split('.')[0]
#     dirsList.append(name)

for i in range(len(dirsList1)):
    f = open("{}{}.txt".format(dirPath,dirsList1[i]), "r",encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    shengDic = eval(lines[0])[dirsList[i]]
    countryDic[dirsList[i]] = shengDic
print(countryDic.keys())
print(countryDic['北京'])
with open("全国地区信息.txt", "w", encoding='utf-8') as f:
    f.write(str(countryDic))
print('成功~~')

# f = open("全国地区信息.txt", "r",encoding='utf-8')
# lines = f.readlines()  # 读取全部内容
# shengDic = eval(lines[0])
# listL = list(shengDic.keys())
# print(shengDic['广西壮族自治区']['梧州市']['藤县'])
