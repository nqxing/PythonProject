import requests

# station_name_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
# r = requests.get(station_name_url)
# result1 = ''
# result2 = ''
# try:
#     for i in r.split('@'):
#         # i 的格式为  bjb|北京北|VAP|beijingbei|bjb|0
#         if len(i.split('|')) >= 3:  # 是否大于3个成员，排除返回起始无效字段ar station_names ='
#             stationText = i.split('|')[1]
#             stationCode = i.split('|')[2]
#             if stationText == '龙岩':
#                 result1 = stationCode
#             elif stationText == '福州':
#                 result2 = stationCode
#             if result1 != '' and result2 != '':  # 找到起止code 后直接退出,避免无效等待
#                 reg = result1 + result2
#                 print(reg)
# except Exception:
#     print('查询失败,请检查如上信息是否正确~~')
# try:
#     requests.get('http://github.com', timeout=0.001)
# except Exception:
#     print('超时了')
#
# from tkinter import *
# root = Tk()
# lb = Listbox(root)
# for item in ['python','tkinter','widget']:
#     lb.insert(END,item)
# #只添加一项将[]作为一个item
# #lb.insert(0,['linux','windows','unix'])
# #添加三项，每个string为一个item
# lb.insert(0,'linux','windows','unix')
# lb.pack()
# root.mainloop()

from tkinter import *

'''
1、设置两个frame类型按钮，当点击Button按钮触发command命令。
2、command命令指向一个事件，改变页面显示的内容。
'''

root = Tk()
# 1、设置两个Frame窗口。一个容器窗口部件。帧可以有边框和背景，当创建一个应用程序或dialog(对话）版面时，帧被用来组织其它的窗口部件。
frame1 = Frame(root)
frame2 = Frame(root)
var = StringVar()
var.set('您不是会员不能下载VIP资源\n前先注册会员再来下载资源')
# 2、设置第一个Label显示文本内容。
textLabel = Label(frame1,
                  textvariable=var,  # 与按钮相关的Tk变量（通常是一个字符串变量）。如果这个变量的值改变，那么按钮上的文本相应更新。
                  justify=LEFT,  # 定义多行文本如何对齐。可取值有：LEFT, RIGHT, 或 CENTER。
                  )
textLabel.pack(side=RIGHT)  # 按扭停靠在窗口的哪个位置left: 左,top: 上,right: 右,botton: 下
# 3、设置第二个Label显示图片信息。
photo = PhotoImage(file="002.gif")  # PhotoImage()方法只支持gif格式的图片。
imgLabel = Label(root, image=photo)
imgLabel.pack(side=LEFT)


def callback():
    var.set('你的身份验证失败，你不是会员')

    # 4、设置一个Button按钮触发callback方法。


theButton = Button(frame2, text='我已注册会员', command=callback)
theButton.pack()
# 5、设置两个frame窗口的大小
frame1.pack(padx=10, pady=10)
frame2.pack(padx=10, pady=10)
mainloop()