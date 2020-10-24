'''''7.选中操作函数，使用函数实现。selection_set函数有两个参数第一个为开始的索引； 
第二个为结束的索引，如果不指定则只选中第一个参数指定的索引项'''
from tkinter import *

root = Tk()
lb = Listbox(root)
for i in range(10):
    lb.insert(END, str(i))
lb.selection_set(0, 10)
#  程序运行结果，选中了所有的项。 此代码并未指定Listbox为MULTIPLE或EXTENDED，查通过selection_set仍旧可以对Listbox进行操作。  
# 与之相对的便是取消选中的函数了，参数与selection_set在参数相同，如下代码取消索引从0－3在状态
lb.selection_clear(0, 3)

'''''8.得到当前Listbox中的item个数'''
print(lb.size())  # 输出10
lb.pack()
'''''9.返回指定索引的项'''
print(lb.get(3))  # 输出3
# get也为两个参数的函数，可以返回多个项(item)，如下返回索引值3－7的值
print(lb.get(3, 7))  # ('3', '4', '5', '6', '7')，是一个tuple类型

'''''10.返回当前返回的项的索引，不是item的值'''
print(lb.curselection())  # (4, 5, 6, 7, 8, 9)

'''''11.判断 一个项是否被选中，使用索引。'''
print(lb.selection_includes(8))  # True
print(lb.selection_includes(0))  # False
root.mainloop()  