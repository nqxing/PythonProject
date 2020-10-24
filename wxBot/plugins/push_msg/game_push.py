from config.fun_api import *

class my_thread(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.bot = bot
    def run(self):
        push_game(self.bot)
def push_game_index(bot):
    th = my_thread(bot)  # id, name
    th.start()

def push_game(bot):
    v1 = SQL().select_var_info("WZ_NEW_WALL")
    v2 = SQL().select_var_info("WZ_NEW_NEWS")
    v3 = SQL().select_var_info("LOL_NEW_WALL")
    v4 = SQL().select_var_info("LOL_NEW_NEWS")
    if v1 != "None":
        send_fwx_group(bot, "王者荣耀壁纸群", v1, True)
        SQL().up_var_info("WZ_NEW_WALL", "None")
    if v2 != "None":
        if "$" in v2:
            values = v2.split("$")
            for v in values:
                send_fwx_group(bot, "王者荣耀壁纸群", v, True)
                time.sleep(1)
        else:
            send_fwx_group(bot, "王者荣耀壁纸群", v2, True)
        SQL().up_var_info("WZ_NEW_NEWS", "None")
    if v3 != "None":
        send_fwx_group(bot, "英雄联盟壁纸群", v3, True)
        SQL().up_var_info("LOL_NEW_WALL", "None")
    if v4 != "None":
        if "$" in v4:
            values = v4.split("$")
            for v in values:
                send_fwx_group(bot, "英雄联盟壁纸群", v, True)
                time.sleep(1)
        else:
            send_fwx_group(bot, "英雄联盟壁纸群", v4, True)
        SQL().up_var_info("LOL_NEW_NEWS", "None")

def send_fwx_group(bot, names, message, type):
    try:
        message = message.replace('|', '\n')
        if type:
            wxpy_groups = bot.groups().search(names)
            if wxpy_groups:
                wxpy_groups[0].send(message)
                write_log(1, '发送了微信消息[{}]给[{}]'.format(message, names))
            else:
                fid = bot.search('vip_大号')[0]
                fid.send('未找到接收者名字{}'.format(names))
                write_log(1, '未找到接收者名字{}'.format(wxpy_groups))
        else:
            my_friend = bot.friends().search(names)
            if my_friend:
                if len(my_friend) == 1:
                    my_friend[0].send(message)
                else:
                    for f in my_friend:
                        f_str = re.findall(':(.*?)>', str(f))[0].strip()
                        if names == f_str:
                            f.send(message)
                write_log(1, '发送了微信消息[{}]给[{}]'.format(message, names))
            else:
                fid = bot.search('vip_大号')[0]
                fid.send('未找到接收者名字{}'.format(names))
                write_log(1, '未找到接收者名字{}'.format(my_friend))
    except:
        write_log(3, '微信消息发送异常 - {}'.format(traceback.format_exc()))
