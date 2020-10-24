import tkinter


class FindLocation(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("全球定位ip位置(离线版)")
        self.root.geometry('600x150')
        # 创建一个输入框,并设置尺寸

        self.helloLabel = tkinter.Label(self.root, text='用户名')
        self.nameInput = tkinter.Entry(self.root, width=30)

        self.helloLabel1 = tkinter.Label(self.root, text='密码')
        self.nameInput1 = tkinter.Entry(self.root, width=30)

        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command=self.hello, text="查询")

    # 完成布局
    def gui_arrang(self):
        self.helloLabel.pack()
        self.nameInput.pack()
        self.helloLabel1.pack()
        self.nameInput1.pack()
        self.result_button.pack()

    # 根据ip查找地理位置
    def hello(self):
        name = self.nameInput.get() or 'world'
        tkinter.messagebox.showinfo('Message', 'Hello, %s' % name)

def main():
    # 初始化对象
    FL = FindLocation()
    # 进行布局
    FL.gui_arrang()
    # 主程序执行
    tkinter.mainloop()
    pass


if __name__ == "__main__":
    main()