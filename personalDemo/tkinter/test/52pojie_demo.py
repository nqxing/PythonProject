# coding:utf-8
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk
import os
import requests
import re
import time
import random
import threading


class UI:
    root = Tk()
    window_captcha = Toplevel(root)
    window_login = Toplevel(root)
    window_passengers = Toplevel(root)
    window_passengers.resizable(False, False)
    window_captcha.resizable(False, False)
    window_login.resizable(False, False)
    root.resizable(False, False)
    radio_state = IntVar()
    radio_state.set("1")
    width_screen = root.winfo_screenwidth()
    height_screen = root.winfo_screenheight()
    url_captcha = "captcha.png"
    if os.path.exists(url_captcha):
        os.remove(url_captcha)
    try:
        image_captcha = ImageTk.PhotoImage(file=url_captcha)
    except FileNotFoundError:
        label_captcha = Label(window_captcha, text="验证码不存在")
    else:
        label_captcha = Label(window_captcha, image=image_captcha)
    label_captcha_tip = Label(window_captcha, text="请输入正确的验证码序号，以“，”分隔")
    entry_captcha_index = Entry(window_captcha, width=25)
    button_captcha_confirm = Button(window_captcha, text="确定", width=10, height=2)
    root.withdraw()
    window_login.withdraw()
    # window_captcha.withdraw()
    window_passengers.withdraw()
    label_user_name_tip = Label(window_login, text="账户名:")
    label_user_pwd_tip = Label(window_login, text="密码:")
    entry_user_name = Entry(window_login, width=20)
    entry_user_pwd = Entry(window_login, width=20, show="●")
    button_login_confirm = Button(window_login, text="登录", width=10, height=2)
    label_to_station = Label(root, text="到达站:")
    label_from_station = Label(root, text="出发站:")
    label_leave_date = Label(root, text="离开日期:")
    entry_to_station = Entry(root, width=8)
    entry_from_station = Entry(root, width=8)
    entry_leave_date = Entry(root, width=20)
    radio_adult = Radiobutton(text="成人", value="1", variable=radio_state)
    radio_student = Radiobutton(text="学生", value="2", variable=radio_state)
    button_ticket_confirm = Button(root, text="开始查票")
    label_ticket_title = Label(root, text="当前车次信息:")
    button_passengers_show = Button(root, text="选择乘车人")
    window_captcha.protocol("WM_DELETE_WINDOW", root.destroy)
    window_login.protocol("WM_DELETE_WINDOW", root.destroy)
    tree_header_index = []
    checkBox_var = []
    tree_header_name = ["序号", "班次", "发车时间", "到达时间", "历时", "乘车时间", "软卧", "无座", ",硬卧", "硬座", "二等座", "一等座", "特等座"]
    for index in range(1, 14):
        tree_header_index.append(str(index))
    tree_all_trains = ttk.Treeview(root, columns=tree_header_index, show='headings', height=10)
    for iterator in range(1, len(tree_header_index) + 1):
        tree_all_trains.column(tree_header_index[iterator - 1], width=len(tree_header_name[iterator - 1]) * 25,
                               anchor='center')
        tree_all_trains.heading(tree_header_index[iterator - 1], text=tree_header_name[iterator - 1])
    scroll_tree_y = ttk.Scrollbar(root, orient="vertical", command=tree_all_trains.yview)
    tree_all_trains.configure(yscroll=scroll_tree_y.set)

    def update_captcha(self):
        try:
            self.image_captcha = ImageTk.PhotoImage(file=self.url_captcha)
        except Exception as e:
            self.label_captcha["text"] = "验证码不存在"
        else:
            self.label_captcha["image"] = self.image_captcha

    def update_tickets(self, trains):
        trains_show = self.tree_all_trains.get_children()
        for train in trains_show:
            self.tree_all_trains.delete(train)
        trains_show = []
        for train in trains:
            train = train[4:17]
            trains_show.append(train)
        for index in range(0, len(trains_show)):
            trains_show[index][0] = index + 1
            self.tree_all_trains.insert('', 'end', values=trains_show[index])

    def select_ticket(self):
        return self.tree_all_trains.selection()

    def show_ticket_information(self, ticket_data):
        # A1硬座 A3硬卧 A4软卧 A6高级软卧 OT其他 A9商务特等座 M一等座 WZ无座 O二等座
        try:
            information = ticket_data["price_information"]["A1"]
            print(information)
        except Exception as e:
            print(type(e))
        print(ticket_data)
        return

    def confirm_passengers(self):
        self.window_passengers.destroy()
        return

    def show_passengers(self, passengers_data):
        self.window_passengers = Toplevel(self.root)
        self.window_passengers.resizable(False, False)
        self.window_passengers.geometry(
            "350x200+{}+{}".format(str(self.width_screen // 2 - 175), str(self.height_screen // 2 - 100)))
        self.window_passengers.title("选择乘车人")
        init_x = 80
        init_y = 30
        index = 0
        for passenger in passengers_data:
            try:
                var = self.checkBox_var[index]
            except IndexError:
                var = IntVar()
                var.set(0)
                self.checkBox_var.append(var)
            checkBox_passenger_choose = Checkbutton(self.window_passengers,
                                                    variable=var,
                                                    text="{}:{}".format(passenger["passenger_name"],
                                                                        passenger["passenger_id_no"]))
            index += 1
            checkBox_passenger_choose.place(x=init_x, y=init_y)
            init_y += 30
            if init_y + 50 > self.window_passengers.winfo_height():
                self.window_passengers.geometry(
                    "{}x{}+{}+{}".format(str(self.window_passengers.winfo_width()), str(init_y + 100),
                                         str(self.width_screen - self.window_passengers.winfo_width() // 2),
                                         str(self.height_screen - self.window_passengers.winfo_height() // 2)))
        button_passengers_confirm = Button(self.window_passengers, text="确定", command=self.confirm_passengers, width=10)
        button_passengers_confirm.place(x=init_x + 60, y=init_y)
        self.window_passengers.update()

    def init_component(self):
        self.window_captcha.geometry(
            "600x250+{}+{}".format(str(self.width_screen // 2 - 300), str(self.height_screen // 2 - 125)))
        self.root.geometry(
            "950x500+{}+{}".format(str(self.width_screen // 2 - 475), str(self.height_screen // 2 - 250)))
        self.window_login.geometry(
            "350x200+{}+{}".format(str(self.width_screen // 2 - 175), str(self.height_screen // 2 - 100)))
        self.window_passengers.geometry(
            "350x200+{}+{}".format(str(self.width_screen // 2 - 175), str(self.height_screen // 2 - 100)))
        self.window_captcha.title("验证码检测")
        self.window_login.title("12306登录窗口")
        self.window_passengers.title("请选择乘车人")
        self.root.title("12306抢票软件 made by 不愿透露姓名的热心市民程先生")
        self.label_captcha.place(x=30, y=20)
        self.label_captcha_tip.place(x=360, y=50)
        self.entry_captcha_index.place(x=360, y=80)
        self.button_captcha_confirm.place(x=400, y=110)
        self.label_user_name_tip.place(x=70, y=40)
        self.label_user_pwd_tip.place(x=70, y=80)
        self.entry_user_name.place(x=120, y=40)
        self.entry_user_pwd.place(x=120, y=80)
        self.button_login_confirm.place(x=130, y=120)
        self.label_from_station.place(x=20, y=20)
        self.entry_from_station.place(x=70, y=20)
        self.label_to_station.place(x=160, y=20)
        self.entry_to_station.place(x=210, y=20)
        self.label_leave_date.place(x=300, y=20)
        self.entry_leave_date.place(x=360, y=20)
        self.radio_adult.place(x=540, y=15)
        self.radio_student.place(x=600, y=15)
        self.button_ticket_confirm.place(x=660, y=15)
        self.tree_all_trains.place(x=20, y=60)
        self.label_ticket_title.place(x=20, y=300)
        self.button_passengers_show.place(x=120, y=295)
        self.scroll_tree_y.pack(side=RIGHT, fill=Y)
        self.window_login.mainloop()
        self.window_captcha.mainloop()
        self.window_passengers.mainloop()


class Tickets:
    stations = []
    trains = []
    starting = ""
    destination = ""
    user_name = ""
    passengers = []
    localtime = time.localtime(time.time())
    year, month, day = time.strftime("%Y", localtime), time.strftime("%m", localtime), time.strftime("%d", localtime)
    book_time = 29 * 24 * 60 * 60

    def query_station(self, place):
        place_abbr = ''
        try:
            place_abbr = self.stations[place]
        except KeyError:
            place_abbr = -1
        return place_abbr

    def format_date(self, ticket_date):
        reg = '\d{4}-\d{1,2}-\d{1,2}'
        if re.match(reg, ticket_date):
            dates = ticket_date.split('-')
            # ticket_year = int(dates[0], 10)
            # ticket_month = int(dates[1], 10)
            ticket_day = int(dates[2], 10)
            try:
                ticket_time = time.mktime(time.strptime(ticket_date, "%Y-%m-%d"))
            except ValueError:
                return {
                    "result_msg": "日期范围不合法",
                    "result_code": "1"
                }
            if ticket_time < time.time() and ticket_day != self.day or ticket_time - time.time() > self.book_time:
                return {
                    "result_msg": "日期不在预定范围之内",
                    "result_code": "2"
                }
            else:
                ticket_date = time.localtime(ticket_time)
                ticket_date = time.strftime("%Y-%m-%d", ticket_date)
                return {
                    "ticket_date": ticket_date,
                    "result_msg": "日期正确",
                    "result_code": "0"
                }
        else:
            return {
                "result_msg": "日期格式错误",
                "result_code": "3"
            }


class Spider:
    session = requests.session()
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    once_header = {}
    apptk_list = []
    repeat_submit_token = ""

    def get_header(self):
        agent = self.user_agent_list[random.randint(0, len(self.user_agent_list) - 1)]
        self.session = requests.session()
        header = {
            "User-Agent": agent,
            "Accept": "*/*",
            "Accept - Encoding": "gzip,deflate,br",
            "Accept - Language": "zh-CN,zh;",
            "q": "0.9",
            "Cache - Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "kyfw.12306.cn",
            "Origin": "https://kyfw.12306.cn"
        }
        return header

    def get_station(self):
        station_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"
        response = self.session.get(station_url, headers=self.once_header)
        stations_all = re.findall(u'([\u4e00-\u95fa5]+)\|([A-Z]+)', response.text)
        stations = dict(stations_all)
        return stations

    def update_captcha(self):
        captcha_url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}".format(
            random.uniform(0, 1))
        response = self.session.get(captcha_url, headers=self.once_header)
        captcha_image = response.content
        fn = open('captcha.png', 'wb')
        fn.write(captcha_image)
        fn.close()

    def check_captcha(self, captcha_index):
        check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        image_coordination = []
        if captcha_index == "":
            return
        all_index = []
        reg = "[\d,]*\d"
        while True:
            if re.match(reg, captcha_index):
                if "，" in captcha_index:
                    all_index = captcha_index.split('，')
                else:
                    all_index = captcha_index.split(',')
                for index in all_index:
                    index = int(index, 10)
                    if index > 4:
                        index -= 4
                        coordination_x = (index % 5 - 1) * 73 + 36.5 + 5
                        coordination_y = 145
                    else:
                        coordination_x = (index % 5 - 1) * 73 + 36.5 + 5
                        coordination_y = 75
                    coordination = str(coordination_x) + "," + str(coordination_y)
                    image_coordination.append(coordination)
                break
        key_code = {
            "answer": ",".join(image_coordination),
            "login_site": "E",
            "rand": "sjrand"
        }
        response = self.session.post(check_url, params=key_code, headers=self.once_header)
        check_result = response.json()
        return check_result

    def login_step_1(self, user_name, user_pwd):
        login_url = "https://kyfw.12306.cn/passport/web/login"
        login_header = self.once_header
        login_header["Referer"] = "https://kyfw.12306.cn/otn/login/init"
        key_code = {
            "username": user_name,
            "password": user_pwd,
            "appid": "otn"
        }
        response = self.session.post(login_url, params=key_code, headers=login_header, verify=False)
        time.sleep(random.uniform(0, 1))
        login_result = response.json()
        # login_msg = login_result["result_message"]
        # login_code = login_result["result_code"]
        # uamtk = login_result["uamtk"]
        return login_result

    def login_step_2(self, uamtk):
        login_url = 'https://kyfw.12306.cn/otn/login/userLogin'
        login_check_url_1 = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        login_check_url_2 = "https://kyfw.12306.cn/otn/uamauthclient"
        params_check_1 = {
            "appid": "otn"
        }
        response_check_1 = self.session.post(login_check_url_1, headers=self.once_header, params=params_check_1)
        response_check_1 = response_check_1.json()
        # check_code_1 = response_check_1["result_code"]
        # check_message_1 = response_check_1["result_message"]
        check_new_app_tk = response_check_1["newapptk"]
        params_check_2 = {
            "tk": check_new_app_tk
        }
        time.sleep(random.uniform(0, 1))
        response_check_2 = self.session.post(login_check_url_2, headers=self.once_header, params=params_check_2)
        response_check_2 = response_check_2.json()
        # check_code_2 = response_check_2["result_code"]
        # check_message_2 = response_check_2["result_message"]
        check_app_tk = response_check_2["apptk"]
        apptk = check_app_tk
        self.apptk_list.append(apptk)
        time.sleep(random.uniform(0, 1))
        key_code = {
            "_json_att": " "
        }
        self.session.post(login_url, params=key_code, headers=self.once_header)
        time.sleep(random.uniform(0, 1))
        self.session.get(login_url, headers=self.once_header)
        return response_check_2

    def query_tickets(self, from_station, to_station, leave_date, ticket_type):
        query_url = 'https://kyfw.12306.cn/otn/leftTicket/queryA'
        key_word = {
            "leftTicketDTO.train_date": leave_date,
            "leftTicketDTO.from_station": from_station,
            "leftTicketDTO.to_station": to_station,
            "purpose_codes": ticket_type
        }
        header = self.once_header
        response = self.session.get(query_url, params=key_word, headers=header)
        tickets = response.json()
        tickets = tickets['data']['result']
        trains = []
        for ticket in tickets:
            data = ticket.split("|")
            train_key = data[0]  # 车密匙
            train_no_key = data[2]  # 车次号
            train_no = data[3]  # 车次
            depart_date = data[8]  # 出发时间
            arrive_date = data[9]  # 到达时间
            all_time = data[10]  # 历时
            take_date = re.findall(u'(\d{4})(\d{2})(\d{2})', data[13])
            to_station_no = data[17]
            from_station_no = data[16]
            take_date = "-".join(list(take_date[0]))  # 乘车时间
            soft_berth = data[25]  # 软卧
            no_seat = data[26]  # 无座
            hard_soft_berth = data[28]  # 硬卧
            hard_seat = data[29]  # 硬座
            second_seat = data[30]  # 二等座
            first_seat = data[31]  # 一等座
            best_seat = data[32]  # 商务特等座
            seat_types = data[35]  # 座位类型
            train_information = [train_key, train_no_key, seat_types, to_station_no, from_station_no, train_no,
                                 depart_date,
                                 arrive_date, all_time, take_date,
                                 soft_berth,
                                 no_seat,
                                 hard_soft_berth, hard_seat,
                                 second_seat,
                                 first_seat, best_seat]
            trains.append(train_information)
        return trains
        # time.sleep(random.uniform(0, 1))
        # check_user()
        # time.sleep(random.uniform(0, 1))
        # select_train(leave_date, ticket_type)

    def get_ticket_price(self, train_information):
        price_url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice'
        price_params = {
            "train_no": train_information["train_no_key"],
            "from_station_no": train_information["from_station_no"],
            "to_station_no": train_information["to_station_no"],
            "seat_types": train_information["seat_types"],
            "train_date": train_information["take_date"]
        }
        price_header = self.once_header
        price_header["If-Modified-Since"] = "0"
        price_header["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        time.sleep(1)
        price_response = self.session.get(url=price_url, params=price_params, headers=price_header)
        price_response = price_response.json()
        price_ticket = price_response["data"]
        return price_ticket

    def check_user(self):
        check_user_url = "https://kyfw.12306.cn/otn/login/checkUser"
        check_user_headers = self.once_header
        check_user_headers["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        user_check_params = {
            "_json_att": " "
        }
        response_user_check = self.session.post(check_user_url, params=user_check_params, headers=check_user_headers)
        response_user_check = response_user_check.json()
        passengers = self.get_dc()
        return passengers

    def get_dc(self):
        global repeat_submit_token
        check_dc_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        dc_header = self.once_header
        dc_header["Upgrade-Insecure-Requests"] = "1"
        dc_header["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        dc_params = {
            "_json_att": ""
        }
        time.sleep(random.uniform(0, 1))
        response_dc = self.session.post(check_dc_url, params=dc_params, headers=dc_header)
        repeat_submit_token = re.findall(r"globalRepeatSubmitToken = '(.*?)';", response_dc.text)[0]
        passengers = self.get_passengers()
        return passengers

    def get_passengers(self):
        get_passengers_url = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
        get_passengers_header = self.once_header
        get_passengers_header["X-Requested-With"] = "XMLHttpRequest"
        get_passengers_header['Referer'] = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        get_passengers_params = {
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": repeat_submit_token
        }
        time.sleep(0.5)
        response_passengers = self.session.post(get_passengers_url, params=get_passengers_params,
                                                headers=get_passengers_header)
        response_passengers = response_passengers.json()
        passengers_list = response_passengers["data"]["normal_passengers"]
        return passengers_list

    def __init__(self):
        self.once_header = self.get_header()


def update_captcha(event, UI, Spider):
    # if event != "":
    #     messagebox.showinfo("坐标", str(event.x) + str(event.y))
    # return
    # 上面可以用来判断坐标以后可以扩展
    Spider.update_captcha()
    UI.update_captcha()
    return


def confirm_captcha_index(event, UI, Spider):
    result = Spider.check_captcha(UI.entry_captcha_index.get())
    if result["result_code"] == "4":
        # UI.root.deiconify()
        UI.window_captcha.destroy()
        UI.window_login.deiconify()
    else:
        update_captcha(event, UI=UI, Spider=Spider)
        print("验证码信息：", result)
    messagebox.showinfo("验证码信息", result["result_message"])


def confirm_login(event, UI, Spider, Tickets):
    result_1 = Spider.login_step_1(UI.entry_user_name.get(), UI.entry_user_pwd.get())
    if result_1["result_code"] == 0:
        messagebox.showinfo("登录成功", "账号密码正确，现在开始验证账号信息是否异常")
        result_2 = Spider.login_step_2(result_1["uamtk"])
        print("验证信息", result_2)
        if result_2["result_code"] == 0:
            Tickets.user_name = result_2["username"]
            messagebox.showinfo("验证成功", "账号状态正常，现在转到查票主页面")
            messagebox.showinfo("{},您好".format(Tickets.user_name), "欢迎使用12306查/抢票软件")
        UI.window_login.destroy()
        UI.root.deiconify()
    else:
        print("账号密码信息", result_1)


def query_tickets(event, UI, Spider, Tickets):
    from_station = Tickets.query_station(UI.entry_from_station.get())
    to_station = Tickets.query_station(UI.entry_to_station.get())
    leave_date = Tickets.format_date(UI.entry_leave_date.get())
    if from_station == -1:
        messagebox.showwarning("查无此站点", "出发站信息有误，请核对后输入")
        return
    if to_station == -1:
        messagebox.showwarning("查无此站点", "到达站信息有误，请核对后输入")
        return
    if leave_date["result_code"] != "0":
        messagebox.showwarning("查询时间错误", leave_date["result_msg"])
    else:
        leave_date = leave_date["ticket_date"]
    ticket_type = UI.radio_state.get()
    if ticket_type == 1:
        ticket_type = "ADULT"
    else:
        ticket_type = "0X00"
    Tickets.trains = Spider.query_tickets(to_station=to_station, from_station=from_station, leave_date=leave_date,
                                          ticket_type=ticket_type)
    UI.update_tickets(Tickets.trains)


def show_ticket_information(event, UI, Spider, Tickets):
    if len(UI.tree_all_trains.selection()) == 0:
        return
    select_ticket = UI.select_ticket()[0]
    select_ticket_information = UI.tree_all_trains.item(select_ticket, "values")
    select_train_no_key = Tickets.trains[int(select_ticket_information[0], 10)][1]
    select_seat_types = Tickets.trains[int(select_ticket_information[0], 10)][2]
    select_to_station_no = Tickets.trains[int(select_ticket_information[0], 10)][3]
    select_from_station_no = Tickets.trains[int(select_ticket_information[0], 10)][4]
    select_ticket_information = {
        "train_index": select_ticket_information[0],
        "train_no": select_ticket_information[1],
        "depart_time": select_ticket_information[2],
        "arrive_time": select_ticket_information[3],
        "all_time": select_ticket_information[4],
        "take_date": select_ticket_information[5],
        "soft_berth": select_ticket_information[6],
        "no_seat": select_ticket_information[7],
        "hard_soft_berth": select_ticket_information[8],
        "hard_seat": select_ticket_information[9],
        "second_seat": select_ticket_information[10],
        "first_seat": select_ticket_information[11],
        "best_seat": select_ticket_information[12],
        "to_station_no": select_to_station_no,
        "from_station_no": select_from_station_no,
        "seat_types": select_seat_types,
        "train_no_key": select_train_no_key
    }
    ticket_price = Spider.get_ticket_price(select_ticket_information)
    ticket_data = {
        "ticket_information": select_ticket_information,
        "price_information": ticket_price
    }
    UI.show_ticket_information(ticket_data)


def check_user(event, Spider, UI, Tickets):
    Tickets.passengers = Spider.check_user()
    passengers_data = []
    for passenger in Tickets.passengers:
        data = {
            "passenger_name": passenger["passenger_name"],
            "passenger_id_no": passenger["passenger_id_no"]
        }
        passengers_data.append(data)
    UI.show_passengers(passengers_data)


def threading_task(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()
    threads.append(t)


threads = []

if __name__ == '__main__':
    UI = UI()
    Spider = Spider()
    Tickets = Tickets()
    Tickets.stations = Spider.get_station()
    threading_task(update_captcha, "", UI, Spider)
    UI.label_captcha.bind("<Button-1>", lambda x: threading_task(update_captcha, x, UI, Spider))
    UI.button_captcha_confirm.bind("<Button-1>", lambda x: threading_task(confirm_captcha_index, x, UI, Spider))
    UI.button_login_confirm.bind("<Button-1>", lambda x: threading_task(confirm_login, x, UI, Spider, Tickets))
    UI.button_ticket_confirm.bind("<Button-1>", lambda x: threading_task(query_tickets, x, UI, Spider, Tickets))
    UI.tree_all_trains.bind("<Button-1>", lambda x: threading_task(show_ticket_information, x, UI, Spider, Tickets))
    UI.button_passengers_show.bind("<Button-1>", lambda x: threading_task(check_user, x, Spider, UI, Tickets))
    UI.init_component()