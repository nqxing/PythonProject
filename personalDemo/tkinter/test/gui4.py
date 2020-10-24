import tkinter
from tkinter import *
from tkinter import messagebox
import requests
import json
import threadpool
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import inspect
import ctypes
import datetime

class tl12306(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()

        # 给主窗口设置标题内容
        self.root.title("12306余票监控系统")
        width = 615
        height = 440

        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        self.var = StringVar()
        # self.var.set('票数监控中,关闭程序即退出监控')
        self.label_tips = tkinter.Label(self.root, textvariable=self.var, justify=CENTER ,font=("微软雅黑", 12, "bold"),fg='red')
        self.label_time = tkinter.Label(self.root, text='请输入日期:（如: 2018-10-01）')
        self.label_beginEnd = tkinter.Label(self.root, text='请输入起始站点：')
        self.label_from = tkinter.Label(self.root, text='从')
        self.label_to = tkinter.Label(self.root, text='到')
        self.label_TrainTimes = tkinter.Label(self.root, text='请选择监控车次：（可多选）')
        self.var1 = StringVar()
        # self.var1.set('')
        self.label_sum = tkinter.Label(self.root, textvariable=self.var1,)
        self.label_mail = tkinter.Label(self.root, text='邮件通知：（留空不通知）')
        self.label_Refresh = tkinter.Label(self.root, text='查询间隔：(秒)')

        self.input_time = tkinter.Entry(self.root, width=30)
        self.input_begin = tkinter.Entry(self.root, width=10)
        self.input_end = tkinter.Entry(self.root, width=10)
        self.input_mail = tkinter.Entry(self.root, width=24)
        self.input_Refresh = tkinter.Entry(self.root, width=10)
        self.query_button = tkinter.Button(self.root, text="开始查询", width=8,command=self.Thread_setlist)
        self.clear_button = tkinter.Button(self.root, text='清空车次', width=8,command=self.setlist_clear)
        self.Monitor_button = tkinter.Button(self.root, text="开始监控", width=8,height=1,command=self.Thread_Monitor,font=("微软雅黑", 12, "bold"))
        self.StopMonitor_button = tkinter.Button(self.root, text="停止监控", width=8,height=1,command=self.stopMonitor,font=("微软雅黑", 12, "bold"))
        self.LB = tkinter.Listbox(self.root, selectmode=MULTIPLE, relief=GROOVE)
        self.yscrollbar = tkinter.Scrollbar(self.LB, command=self.LB.yview)
        # 复选框
        self.vHobby_FirstClass = tkinter.IntVar()  # 创建IntVar对象，指明爱好为音乐
        self.vHobby_SecondClass = tkinter.IntVar()
        self.vHobby_NoSeat = tkinter.IntVar()

        self.checkbox_FirstClass = tkinter.Checkbutton(self.root, text="一等座", variable=self.vHobby_FirstClass)  # 音乐复选框
        self.checkbox_SecondClass = tkinter.Checkbutton(self.root, text="二等座", variable=self.vHobby_SecondClass)
        self.checkbox_NoSeat = tkinter.Checkbutton(self.root, text="无座", variable=self.vHobby_NoSeat)

        self.result1 = ''


    def gui_arrang(self):

        self.root.iconbitmap('.\\ico\\my.ico')

        self.label_tips.place(x=150, y=25)

        self.label_time.place(x=57, y=62)
        self.input_time.place(x=57, y=90)
        self.label_beginEnd.place(x=57, y=115)
        self.label_from.place(x=57, y=138)
        self.input_begin.place(x=77, y=140)
        self.label_to.place(x=155, y=138)
        self.input_end.place(x=178, y=140)
        self.query_button.place(x=262, y=135)
        self.clear_button.place(x=340, y=135)

        self.label_TrainTimes.place(x=57, y=165)
        self.label_sum.place(x=469, y=165)
        self.LB.place(x=57, y=190, relwidth=0.81, relheight=0.238)
        self.LB.insert(0, '暂无车次信息,请先查询车次~~')
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.LB.config(yscrollcommand=self.yscrollbar.set)
        self.label_mail.place(x=57, y=298)
        self.input_mail.place(x=57,y=322)
        self.checkbox_FirstClass.place(x=150, y=368)
        self.checkbox_SecondClass.place(x=220, y=368)
        self.checkbox_NoSeat.place(x=290, y=368)

        self.label_Refresh.place(x=57, y=348)
        self.input_Refresh.place(x=57,y=372)
        self.Monitor_button.place(x=355, y=349)
        self.StopMonitor_button.place(x=460,y=349)

    def get_station_code(self):
        '''根据起止站站点名去获取对应的站点编码'''
        self.station_name_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'  # 起始站点信息表，根据起止站点获取站点编码code
        result = {}
        result['from_code'] = ''
        result['to_code'] = ''
        try:
            r = requests.get(url=self.station_name_url).text
            for i in r.split('@'):
                # i 的格式为  bjb|北京北|VAP|beijingbei|bjb|0
                if len(i.split('|')) >= 3:  # 是否大于3个成员，排除返回起始无效字段ar station_names ='
                    stationText = i.split('|')[1]
                    stationCode = i.split('|')[2]
                    if stationText == self.from_station:
                        result['from_code'] = stationCode
                    elif stationText == self.to_statian:
                        result['to_code'] = stationCode
                    if result['from_code'] != '' and result['to_code'] != '':  # 找到起止code 后直接退出,避免无效等待
                        return result
            if result['from_code'] == '' or result['to_code'] == '':
                return result
        except Exception:
            tkinter.messagebox.showerror('错误提示', '站点表编码获取出错了~~')
    def getlist(self):
        '''根据传入的日期，起点站，终点站去查询余票信息'''
        # 灵活修改为模拟输入【日期，起止站点由用户输入】
        self.url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
        self.headers = {
            "Host": "kyfw.12306.cn",
            "If-Modified-Since": "0",
            "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
        }
        self.result = self.get_station_code()
        self.lastresult = []  # 所有车次所有余票信息列表
        if self.result['from_code'] == '' or self.result['to_code'] == '':
            tkinter.messagebox.showerror('地址查询失败', '请检查起始站点是否正确~~')
            return self.lastresult
        else:
            try:
                r = requests.get(self.url.format(self.data, self.result['from_code'], self.result['to_code']), headers=self.headers)
                if  r.status_code == 200:
                    j = json.loads(r.text)
                    k = j['data']
                    map = k['map']
                    for r in k['result']:
                        strarray = r.split('|')
                        train_num = str(strarray[3])# 车次
                        state = str(strarray[1])
                        SetOut = map[str(strarray[6])]
                        destination = map[str(strarray[7])]
                        seat1 = str(strarray[-6])  # 一等座
                        seat2 = str(strarray[-7])  # 二等座
                        seat3 = str(strarray[-11])  # 站票
                        timebeg = str(strarray[8])
                        timeend = str(strarray[9])
                        BusSchedules = '{},{}-{},时间:{}-{},一等座({}),二等座({}),无座({}),{}'.format(train_num,SetOut,destination,timebeg,timeend,seat1,seat2,seat3,state)
                        self.lastresult.append(BusSchedules)
                    return self.lastresult
                else:
                    tkinter.messagebox.showerror('错误提示', '服务器状态码:%s\n可能是访问太频繁,被封IP了~~'%r.status_code)
            except Exception as e:
                print(e)
                tkinter.messagebox.showerror('错误提示', '地址访问出错了~~')
    def Thread_setlist(self):
        t = threading.Thread(target=self.setlist)
        t.setDaemon(True)
        t.start()
    def setlist(self):
        self.data = self.input_time.get()
        self.from_station = self.input_begin.get()
        self.to_statian = self.input_end.get()
        now = datetime.datetime.now()
        begintime = now.strftime('%Y-%m-%d')
        delta = datetime.timedelta(days=29)
        dates = [begintime]
        for i in range(delta.days):
            dt = now + datetime.timedelta(i+1)
            dt = dt.strftime('%Y-%m-%d')
            dates.append(dt)
        if self.data == '':
            tkinter.messagebox.showinfo('请输入日期', '请输入日期~~')
        elif not self.data in dates:
            tkinter.messagebox.showinfo('日期错误', '日期格式错误或查询日期不在范围内~~')
        elif self.from_station == '':
            tkinter.messagebox.showinfo('请输入起点站', '请输入起点站~~')
        elif self.to_statian == '':
            tkinter.messagebox.showinfo('请输入终点站', '请输入终点站~~')
        else:
            self.query_button.config(state=DISABLED)
            self.clear_button.config(state=DISABLED)
            self.LB.delete(0,END)
            self.last_result = self.getlist()
                # 为回显列表赋值
            if self.lastresult:
                for item in self.last_result:
                    self.LB.insert(END, item)
            self.query_button.config(state=NORMAL)
            self.clear_button.config(state=NORMAL)
            if self.last_result:
                self.var1.set('共计%s个车次'%len(self.last_result))
    def setlist_clear(self):
        if self.LB.size() == 1:
            self.LB.delete(1,END)
        else:
            self.LB.delete(0, END)
            self.var1.set('')
            self.LB.insert(0, '暂无车次信息,请先查询车次~~')
    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    def stopMonitor(self):
        # self.finded_tiket = True
        try:
            self._async_raise(self.t.ident,SystemExit)
            self.Monitor_button.config(state=NORMAL)
            self.var.set('')
        except Exception as e:
            tkinter.messagebox.showerror('错误提示', '请先开始监控~~')
    def Thread_Monitor(self):
        self.t = threading.Thread(target=self.Monitor)
        self.t.setDaemon(True)
        self.t.start()
    def Monitor(self):
        self.FirstClass = self.vHobby_FirstClass.get()
        self.SecondClass = self.vHobby_SecondClass.get()
        self.NoSeat = self.vHobby_NoSeat.get()
        tuplelist = self.LB.curselection()
        self.finded_tiket = False
        if not tuplelist:
            tkinter.messagebox.showinfo('请选择车次', '请至少选择一个车次~~')
        elif self.LB.size() ==1:
            tkinter.messagebox.showinfo('请选择车次', '请至少选择一个车次~~')
        elif self.input_mail.get() != '' and\
            re.match("^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$",
                     self.input_mail.get()) == None:
            tkinter.messagebox.showinfo('邮箱地址错误', '请输入正确的邮箱地址~~')
        elif self.input_Refresh.get() == '':
            tkinter.messagebox.showinfo('请输入查询间隔', '请输入查询间隔~~')
        elif self.input_Refresh.get() != '' and self.input_Refresh.get().isdigit() == False:
                tkinter.messagebox.showinfo('请输入查询间隔', '请输入正整数~~')
        elif self.FirstClass + self.SecondClass + self.NoSeat == 0:
            tkinter.messagebox.showinfo('请选择座次', '您还未选择几等座哦~~')
        else:
            self.Monitor_button.config(state=DISABLED)
            self.num = 1
            self.var.set('票数监控中,关闭程序即退出监控...')
            last_result = []  # 所有车次所有余票信息列表
            for t in tuplelist:
                ti = self.last_result[t].split(',')[0]
                last_result.append(ti)
            while self.finded_tiket == False:
                self.run_Monitor(last_result)
                self.var.set('票数监控中,关闭程序即退出监控...已查询%s次' % self.num)
                self.num+=1
                if self.finded_tiket == False:
                    time.sleep(int(self.input_Refresh.get()))
            self.var.set('')
    def run_Monitor(self,last_result):
        try:
            r = requests.get(self.url.format(self.data, self.result['from_code'], self.result['to_code']),headers=self.headers)
            if r.status_code == 200:
                j = json.loads(r.text)
                k = j['data']
                self.Rlist = k['result']
                pool = threadpool.ThreadPool(len(last_result))
                Monitors = threadpool.makeRequests(self.begin_Monitor, last_result)
                [pool.putRequest(Mon) for Mon in Monitors]
                pool.wait()
                if self.result1:
                    if self.input_mail.get() != '':
                        mail = self.input_mail.get()
                        self.send_mail(self.result1,mail)
                    tkinter.messagebox.showinfo('有票啦', '%s' % self.result1)
                    self.Monitor_button.config(state=NORMAL)
                    self.result1 = ''
            else:
                tkinter.messagebox.showinfo('监控失败', '服务器状态码:%s\n可能是访问太频繁,被封IP了~~' % r.status_code)
        except Exception:
            tkinter.messagebox.showerror('错误提示', '地址访问出错了~~')
    def begin_Monitor(self,lastresult):
        for r in self.Rlist:
            if '|{}|'.format(lastresult) in r:
                strarray = r.split('|')
                seat1 = str(strarray[-6])  # 一等座
                seat2 = str(strarray[-7])  # 二等座
                seat3 = str(strarray[-11])  # 站票
                result = ''
                if self.FirstClass == 1:
                    if seat1 != '无' and seat1 != '':
                        result += '一等座({}),'.format(seat1)  # pyrhon的三目运算，如果返回实际剩余票数，则显示余票数
                if self.SecondClass == 1:
                    if seat2 != '无' and seat2 != '':
                        result += '二等座({}),'.format(seat2)
                if self.NoSeat == 1:
                    if seat3 != '无' and seat3 != '':
                        result += '无座({}),'.format(seat3)
                if result != '':
                    self.finded_tiket = True  # 查到票就标记已有票，不再刷新页面，如果不是自己想要的车次，可以注释此行代码，或者修改判断逻辑
                    result = '{},{}有票啦~~'.format(lastresult, result)
                    self.result1 +=  result+'\n'
    def send_mail(self,str,mail):
        # 第三方 SMTP 服务
        mail_host = "smtp.qq.com"  # 设置服务器
        mail_user = "184417622@qq.com"  # 用户名
        mail_pass = "tmkyeaxztrvybiij"  # 口令
        sender = '184417622@qq.com'
        receivers = [mail]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        message = MIMEText('Hello~\n你关注的车次信息有余票啦~快去买票吧~\n%s'%str, 'plain', 'utf-8')
        message['From'] = Header("朝夕忆浅", 'utf-8')
        message['To'] = Header("", 'utf-8')
        message['Subject'] = Header("您所关注的车次有余票啦~", 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
            tkinter.messagebox.showinfo('发送成功', '邮件发送成功,请查收~~')
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
            tkinter.messagebox.showerror('发送失败', '邮件发送失败,请查看邮件地址是否正确~~')
def main():
    # 初始化对象
    L = tl12306()
    # 进行布局
    L.gui_arrang()
    # 主程序执行
    tkinter.mainloop()
if __name__ == '__main__':
    main()