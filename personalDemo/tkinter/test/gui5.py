import tkinter as tk  # 导入tkinter模块
import tkinter.messagebox

class Application(tk.Frame):  # 定义GUI应用程序类，派生于Frame类
    def __init__(self, master=None):  # 构造函数
        tk.Frame.__init__(self, master)  # 父类构造函数
        self.grid()
        self.createWidgets()  # 创建子组件

    def createWidgets(self):
        self.lblTitle = tk.Label(self, text="个人信息调查")  # 个人信息调查标签
        self.lblName = tk.Label(self, text="姓名")
        self.lblSex = tk.Label(self, text="性别")
        self.lblHobby = tk.Label(self, text="爱好")
        self.lblTitle.grid(row=0, column=0, columnspan=4)  # 个人信息标签置于0行0列，跨4列
        self.lblName.grid(row=1, column=0)
        self.lblSex.grid(row=2, column=0)
        self.lblHobby.grid(row=3, column=0)
        # 文本框
        self.entryName = tk.Entry(self)  # 创建Entry组件，接收姓名
        self.entryName.grid(row=1, column=1, columnspan=3)  # 姓名文本框位于1行1列，跨3列
        # 单选按钮
        self.vSex = tk.StringVar()  # 创建StringVar对象，接收性别
        self.vSex.set("M")  # 设置初始值为“男”
        self.radioSexM = tk.Radiobutton(self, text="男", value="M", variable=self.vSex)
        self.radioSexF = tk.Radiobutton(self, text="女", value="F", variable=self.vSex)
        self.radioSexM.grid(row=2, column=1)
        self.radioSexF.grid(row=2, column=2)
        # 复选框
        self.vHobbyMusic = tk.IntVar()  # 创建IntVar对象，指明爱好为音乐
        self.vHobbySports = tk.IntVar()
        self.vHobbyTravel = tk.IntVar()
        self.vHobbyMovie = tk.IntVar()
        self.checkboxMusic = tk.Checkbutton(self, text="音乐", variable=self.vHobbyMusic)  # 音乐复选框
        self.checkboxSports = tk.Checkbutton(self, text="运动", variable=self.vHobbySports)
        self.checkboxTravel = tk.Checkbutton(self, text="旅游", variable=self.vHobbyTravel)
        self.checkboxMovie = tk.Checkbutton(self, text="电影", variable=self.vHobbyMovie)
        self.checkboxMusic.grid(row=3, column=1)  # 音乐复选框位于3行1列
        self.checkboxSports.grid(row=3, column=2)
        self.checkboxTravel.grid(row=3, column=3)
        self.checkboxMovie.grid(row=3, column=4)
        # 按钮
        self.btnOK = tk.Button(self, text="提交", command=self.funcOK)  # 创建提交按钮组件
        self.btnOK.grid(row=4, column=1, sticky=tk.E)  # 提交按钮置于4行1列
        self.btnCancel = tk.Button(self, text="取消", command=root.destroy)  # 创建取消按钮
        self.btnCancel.grid(row=4, column=3, sticky=tk.W)

    def funcOK(self):
        strSex = "男" if (self.vSex.get() == "M") else "女"
        strMusic = self.checkboxMusic['text'] if (self.vHobbyMusic.get() == 1) else ''
        strSports = self.checkboxSports['text'] if (self.vHobbySports.get() == 1) else ''
        strTravel = self.checkboxTravel['text'] if (self.vHobbyTravel.get() == 1) else ''
        strMovie = self.checkboxMovie['text'] if (self.vHobbyMovie.get() == 1) else ''
        str1 = self.entryName.get() + "您好:\n"
        str1 += "您的性别是：" + strSex + "\n"
        str1 += "您的爱好是：" + strMusic + '、' + strSports + '、' + strTravel + '、' + strMovie
        tk.messagebox.showinfo("个人信息", str1)  # 弹出消息对话框


root = tk.Tk()  # 创建一个Tk根窗口组件root
root.title("个人信息调查")  # 设置窗口标题
app = Application(master=root)  # 创建Application对象实例
app.mainloop() 