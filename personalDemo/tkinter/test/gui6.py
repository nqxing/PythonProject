from tkinter import *

root = Tk()
width = 600
height = 150
#获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root.geometry(alignstr)

# 单选
# LB1 = Listbox(root)

# Label(root, text='单选：选择你的课程').pack()
# for item in ['Chinese', 'English', 'Math']:
#     LB1.insert(END, item)
# LB1.pack()

#
# scrolly=Scrollbar(root)
# scrolly.pack(side=RIGHT,fill=Y)
# # 多选
# LB2 = Listbox(root, selectmode=MULTIPLE,width=20,height=3,yscrollcommand=scrolly.set)
# Label(root, text='多选：你会几种编程语言').pack()
# for item in ['python', 'C++', 'C', 'Java', 'Php']:
#     LB2.insert(END, item)
# LB2.pack()
#
# scrolly.config(command=LB2.yview)

# 多选
LB2 = Listbox(root, selectmode=MULTIPLE,relief=GROOVE)
Label(root, text='多选：你会几种编程语言').pack()
for item in ['python', 'C++', 'C', 'Java', 'Php']:
    LB2.insert(END, item)
LB2.place(x=5,y=25,relwidth=0.3,relheight=0.5)
yscrollbar = Scrollbar(LB2,command=LB2.yview)
yscrollbar.pack(side=RIGHT, fill=Y)
LB2.config(yscrollcommand=yscrollbar.set)

root.mainloop()