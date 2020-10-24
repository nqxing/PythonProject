a = ['工艺3', '绘画3', '书法3', '设计3',]
import requests
# b = ['设计3','工艺3', '书法3','绘画3' ,]
# print (len(list(set(b).difference(set(a)))))
# print (list(set(a).difference(set(b))))
# import re
# f = open("1.txt", "r")
# strs = f.readlines()
# print(strs[0])
#
# # video_urls = re.findall('"z-ico-video"></span>(.*?)</span>', strs[0], re.S)
# video_urls = re.findall(".*?/video/(.*?)'", strs[0], re.S)
# print(video_urls)
# print(len(video_urls))



# headers = {
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
# }
# r = requests.get('https://www.zhihu.com/api/v4/questions/1235454/answers', headers=headers)
# print(r.status_code)
# print(r.text)

# a = 1
# b = 3
# print(a/b)

# print ('%.2f' %(a/b))
import decimal

ac = 1
b = 23
# intt = '%.2f' % (ac/b)
intt = round(ac/b, 2)
# intt = '0.086'
print(intt*100)
# at = decimal.Decimal(intt)
# decimal.getcontext().rounding = decimal.ROUND_05UP
# print(round(at, 2))

#方法一：
# print(round(a/b,2))


#
# video = requests.get('https://vdn1.vzuu.com/SD/56d0a97a-a263-11e9-ac15-0a580a453318.mp4?disable_local_cache=1&bu=com&expiration=1562730374&auth_key=1562730374-0-0-12a44a7bc01c570c9ac715a6f17fdf62&f=mp4&v=hw', headers=headers)
# img_path = "D:/知乎答案图片"
# try:
#     if video.status_code == 200:
#         with open(img_path + '/' + 'shishi' + '.mp4', "wb") as f:
#             f.write(video.content)
#     else:
#         print('视频下载失败!', video.status_code)
# except:
#     # print(traceback.format_exc())
#     pass