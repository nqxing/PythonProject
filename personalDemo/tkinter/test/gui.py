'a hello world GUI example.'

from tkinter import *
import tkinter.messagebox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='用户名: ')
        self.helloLabel.pack(side=LEFT)
        self.nameInput = Entry(self,width=15)
        self.nameInput.pack(side=LEFT)
        # self.helloLabel1 = Label(self, text='密码')
        # self.helloLabel1.pack()
        # self.nameInput1 = Entry(self,width=15)
        # self.nameInput1.pack()
        self.alertButton = Button(self, text='Hello', command=self.hello)
        self.alertButton.pack()
    def hello(self):
        name = self.nameInput.get() or 'world'
        tkinter.messagebox.showinfo('Message', 'Hello, %s' % name)

app = Application()
app.master.title('Hello World')
app.master.geometry('600x150')
# 主消息循环:
app.mainloop()


# from tkinter import *
#
# top = Tk()
# L1 = Label(top, text="网站名")
# L1.pack(side=LEFT)
# E1 = Entry(top, bd=5)
# E1.pack(side=RIGHT)
#
# top.mainloop()

