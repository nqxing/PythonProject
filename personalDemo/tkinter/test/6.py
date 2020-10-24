from tkinter import Tk, Scrollbar, Frame
import tkinter
from tkinter.ttk import Treeview



#创建tkinter应用程序窗口

root = Tk()

#设置窗口大小和位置

root.geometry('500x300+400+300')

#不允许改变窗口大小

root.resizable(False, False)

#设置窗口标题

root.title('通信录管理系统')



#使用Treeview组件实现表格功能

frame = Frame(root)

frame.place(x=0, y=10, width=480, height=280)

#滚动条

scrollBar = tkinter.Scrollbar(frame)

scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

#Treeview组件，6列，显示表头，带垂直滚动条

tree = Treeview(frame,columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6'),show="headings",yscrollcommand=scrollBar.set)

#设置每列宽度和对齐方式

tree.column('c1', width=70, anchor='center')

tree.column('c2', width=40, anchor='center')

tree.column('c3', width=40, anchor='center')

tree.column('c4', width=120, anchor='center')

tree.column('c5', width=100, anchor='center')

tree.column('c6', width=90, anchor='center')

#设置每列表头标题文本

tree.heading('c1', text='姓名')

tree.heading('c2', text='性别')

tree.heading('c3', text='年龄')

tree.heading('c4', text='部门')

tree.heading('c5', text='电话')

tree.heading('c6', text='QQ')

tree.pack(side=tkinter.LEFT, fill=tkinter.Y)

#Treeview组件与垂直滚动条结合

scrollBar.config(command=tree.yview)

#定义并绑定Treeview组件的鼠标单击事件

def treeviewClick(event):

    pass

# tree.bind('', treeviewClick)



#插入演示数据

for i in range(10):

    tree.insert('', i, values=[str(i)]*6)

#运行程序，启动事件循环

root.mainloop()