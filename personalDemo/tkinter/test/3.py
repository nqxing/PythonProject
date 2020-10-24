from tkinter import *

'''
开启Entry对输入文本验证功能。
1、实现该功能，需要通过设置validate、validatecommand和invalidcommand三个选项。 
2、启用验证的开关是validate选项，该选项可以设置以下的值：
    focus：当entry组件获得或者失去焦点的时候验证 
    focusin：当entry组件获得焦点的时候验证 
    focusout:当entry组件失去焦点的时候验证 
    key:当输入框被编辑的时候验证 
    all:当出现上面任何一种情况时候验证 
    none:关闭验证功能。默认设置为该选项
3、validatecommand选项指定一个验证函数，该函数只能返回True或者False表示验证结果，一般情况下验证函数只需要知道输入框中的内容即可，
可以通过Entry组件的get()方法来获得该字符串。
4、invalidcommand选项指定的函数只有在validatecommand的返回值为False的时候才被调用。
'''
'''
validatecommand选项指定一个验证函数，该函数只能返回True或者False表示验证结果
invalidcommand选项指定的函数只有在validatecommand的返回值为False的时候才被调用。
'''
root = Tk()


def text():
    if e1.get() == '芝麻开门':
        print('正确')
        return True
    else:
        print('错误')
        return False


def text2():
    print('validatecommand的返回值为False的时候调用了我')
    return False


v = StringVar()
e1 = Entry(root, textvariable=v, validate='focusout', validatecommand=text,)
e2 = Entry(root)
e1.pack(padx=10, pady=10)
e2.pack(padx=10, pady=10)
mainloop()