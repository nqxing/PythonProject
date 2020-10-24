from config.fun_api import *
from config.config import *
from plugins.ele_hbao.hongbao_cx import cx_hongbao


class my_thread(threading.Thread):
    def __init__(self, bianhao, group_sn, alink, wxmsg):
        threading.Thread.__init__(self)
        self.th_id = bianhao
        # self.th_name = th_name
        self.group_sn = group_sn
        self.alink = alink
        self.wxmsg = wxmsg
    def run(self):
        jk_hongbao(self.group_sn, self.th_id, self.alink, self.wxmsg)

def wx_index(group_sn, bianhao, alink, wxmsg):
    th = my_thread(bianhao, group_sn, alink, wxmsg)  # id, name
    th.start()

# 红包监控 获取指定账号进行查询 出现最佳或最佳已被领取后退出程序

def jk_hongbao(group_sn, bianhao, alink, wxmsg):
    try:
        hb_time = DEFAULT_HB_TIME
        hongbaoMax = int(re.findall('第(.*?)个', wxmsg.text)[0])
        k = True
        if hongbaoMax != None:
            write_log(1, '{} - 【红包{}】的最佳手气红包为第{}个'.format(wxmsg.sender, bianhao, hongbaoMax))
            x = -1  # 控制红包监控语句打印，确保只在有人点了红包后才进行打印输出
            num = 1
            z = True
            values = get_eleid()
            if values == '暂无可用账号':
                fid = wxmsg.search('vip_大号')[0]
                fid.send('当前已无饿了么可用账号，请赶紧添加')
                write_log(1, '当前已无饿了么可用账号，请赶紧添加')
            else:
                phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], values[5]
                # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
                begin_time = int(time.time())  # 获取运行该脚本时的时间戳
                wx_beizhu = re.findall(':(.*?)>', str(wxmsg.sender))[0].strip()
                SQL().add_ele_hb(bianhao, group_sn, hongbaoMax, alink, False, wx_beizhu)
                strs = SQL().select_var_info("ELE_KL")
                if strs:
                    wxmsg.reply('【红包{}】福利天天领，复制这条信息{}，到[手机淘宝]立刻领红包'.format(bianhao, strs))
                while True:
                    result = cx_hongbao(phone, link, sign, sid, group_sn)
                    if result['status'] == 0:
                        if result['value']['promotion_records'] != None:
                            hongbao = len(result['value']['promotion_records'])
                            if hongbao < hongbaoMax - 1:
                                if x == -1:
                                    wxmsg.reply('【红包{}】监控中，该红包最佳手气为第{}个，当前已有{}人领取，请留意微信消息（注：红包监控周期为3小时，请记得将红包分享至人多的群聊中哦）'.format(bianhao, hongbaoMax, hongbao))
                                if hongbao > x:
                                    write_log(1, '{} - 【红包{}】使用了[{}]账号进行监控'.format(wxmsg.sender, bianhao, phone))
                                    write_log(1, '{} - 【红包{}】监控中，当前已有{}人领取'.format(wxmsg.sender, bianhao, hongbao))
                                    SQL().up_ele_hb_time(hongbao, group_sn, phone)
                                    x = hongbao  # 查到最新红包已领取数量后赋值
                                num += 1
                                t_run_time = int(time.time()) - begin_time
                                if t_run_time // 60 >= 180:
                                    SQL().up_ele_over_hb(group_sn)
                                    write_log(1, '{} - 【红包{}】监控已达3小时，系统将自动关闭监控'.format(wxmsg.sender, bianhao))
                                    k = False
                                    break
                                if hongbao <= hongbaoMax - 3:
                                    time.sleep(17)
                                    # write_log(1, '{} - 【红包{}】等待{}秒'.format(wxmsg.sender, bianhao, default_cxtime + 10))
                            elif hongbao == hongbaoMax - 1:
                                if z:
                                    write_log(1, '{} - 【红包{}】监控中，当前已有{}人领取'.format(wxmsg.sender, bianhao, hongbao))
                                    # msg = '【红包{}】下一个就是最佳手气红包，快去点开领取吧'.format(bianhao)
                                    msg = '【红包{}】下一个就是最佳手气红包，请翻阅消息点击源红包领取'.format(bianhao)
                                    wxmsg.reply(msg)
                                    # wxmsg.reply(alink)
                                    write_log(1, '{} - 【红包{}】下一个就是最佳手气红包，快去点开领取吧，{}'.format(wxmsg.sender, bianhao, alink))
                                    z = False
                                t_run_time = int(time.time()) - begin_time
                                if t_run_time // 60 >= 180:
                                    SQL().up_ele_over_hb(group_sn)
                                    write_log(1, '{} - 【红包{}】监控已达3小时还未被领取，当前已领取{}个，系统将自动关闭监控'.format(wxmsg.sender, hongbao, bianhao))
                                    # wxmsg.reply('【红包{}】监控已达3小时，系统将自动关闭监控'.format(bianhao))
                                    k = False
                                    break
                                # break
                            elif hongbao > hongbaoMax - 1:
                                is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
                                if num == 1 and is_lucky and z:
                                    write_log(1, '{} - 【红包{}】的最佳手气已经被领走了，请换个红包吧'.format(wxmsg.sender, bianhao))
                                    wxmsg.reply('【红包{}】的最佳手气已经被领走了，请换个红包吧'.format(bianhao))
                                    break
                                if num == 1 and is_lucky == False and z:
                                    write_log(1, '{} - 【红包{}】已领取{}个，但最佳手气还未产生，快去领取试试吧'.format(wxmsg.sender, bianhao, hongbao))
                                    wxmsg.reply('【红包{}】已领取{}个，但最佳手气还未产生，快去领取试试吧'.format(bianhao, hongbao))
                                    wxmsg.reply(alink)
                                    break
                                if num > 1 and z == False:
                                    if is_lucky:
                                        lucky_name = result['value']['promotion_records'][hongbaoMax - 1]['sns_username']
                                        lucky_amount = result['value']['promotion_records'][hongbaoMax - 1]['amount']
                                        lucky_msg = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, lucky_name, lucky_amount)
                                        wxmsg.reply(lucky_msg)
                                        SQL().add_ele_hb_record(bianhao, lucky_name, lucky_amount, "wx")
                                        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                                        lucky_msg_info = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, re.sub(reg, '', lucky_name), lucky_amount)
                                        write_log(1, lucky_msg_info)
                                        break
                                    else:
                                        promotion_records = result['value']['promotion_records']
                                        for p in promotion_records:
                                            is_lucky = p['is_lucky']  # 减一是数组从0开始读
                                            if is_lucky:
                                                lucky_name = p['sns_username']
                                                lucky_amount = p['amount']
                                                lucky_msg = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, lucky_name, lucky_amount)
                                                wxmsg.reply(lucky_msg)
                                                SQL().add_ele_hb_record(bianhao, lucky_name, lucky_amount, "wx")
                                                reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                                                lucky_msg_info = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao,
                                                                                                re.sub(reg, '', lucky_name),
                                                                                                lucky_amount)
                                                write_log(1, lucky_msg_info)
                                                break
                                t_run_time = int(time.time()) - begin_time
                                if t_run_time // 60 >= 180:
                                    SQL().up_ele_over_hb(group_sn)
                                    write_log(1, '{} - 【红包{}】监控已达3小时还未被领取，当前已领取{}个，系统将自动关闭监控'.format(wxmsg.sender, bianhao, hongbao))
                                    # wxmsg.reply('【红包{}】监控已达3小时，系统将自动关闭监控'.format(bianhao))
                                    k = False
                                    break
                            time.sleep(hb_time)
                        else:
                            write_log(1, '{} - 【红包{}】[{}]查询该红包数量为空了，{}'.format(wxmsg.sender, bianhao, phone, alink))
                            break
                    elif result['status'] == 1:
                        # if num == 1:
                        #     wxmsg.reply('系统正在调度账号中，请稍等')
                        write_log(1, '{} - 【红包{}】{}身份信息过期，需重新验证'.format(wxmsg.sender, bianhao, phone))
                        SQL().up_ele_id_info("未登录", phone)
                        values = get_eleid()
                        if values:
                            phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], \
                                                              values[5]
                            write_log(1, '{} - 【红包{}】身份信息失效，现在更换手机号为{}监控'.format(wxmsg.sender, bianhao, phone))
                        else:
                            fid = wxmsg.search('vip_大号')[0]
                            fid.send('当前已无饿了么可用账号，请赶紧添加')
                            write_log(1, '{} - 【红包{}】当前已无饿了么可用账号，请赶紧添加'.format(wxmsg.sender, bianhao))
                            break
                    elif result['status'] == 2:
                        write_log(3, '{} - 未知错误，{}'.format(wxmsg.sender, result['value']))
                        if result['value']['message'] == '领取失败，请刷新再试。':
                            values = get_eleid()
                            if values:
                                phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], \
                                                                  values[5]
                                write_log(1, '{} - 【红包{}】领取失败，请刷新再试。现在更换手机号为{}监控'.format(wxmsg.sender, bianhao, phone))
                            else:
                                write_log(1, '{} - 【红包{}】当前已无饿了么可用账号，请赶紧添加'.format(wxmsg.sender, bianhao))
                                break
                        hb_time += 1
                        time.sleep(hb_time)
                        if hb_time > 15:
                            wxmsg.reply('【红包{}】抱歉，系统出现异常，请重新分享试试'.format(bianhao))
                            break
                    elif result['status'] == -1:
                        write_log(3, '{} - {}'.format(wxmsg.sender, result['value']))
                        hb_time += 1
                        time.sleep(hb_time)
                        if hb_time > 15:
                            wxmsg.reply('【红包{}】抱歉，系统出现异常，请重新分享试试'.format(bianhao))
                            break
                run_time = int(time.time()) - begin_time
                write_log(1, '{} - 【红包{}】监控完毕~用时{}分{}秒，共查询了{}次'.format(wxmsg.sender, bianhao, run_time//60, run_time%60, num))
                if k:
                    SQL().del_ele_group_sn(group_sn)
                    # wxmsg.reply('【红包{}】退出监控，用时{}分{}秒'.format(bianhao, run_time//60, run_time%60))
        else:
            write_log(1, '【红包{}】识别出错，已退出监控'.format(bianhao))
            wxmsg.reply('【红包{}】识别出错，已退出监控'.format(bianhao))
    except:
        write_log(1, '【红包{}】Error : {}'.format(bianhao, traceback.format_exc()))

def get_eleid():
    ele_ids = SQL().select_ele_id_info()
    if ele_ids:
        tup_id = ele_ids[0]
        t = time.time()
        SQL().up_ele_id_time_stamp(int(round(t * 1000)), tup_id[0])
        return tup_id
    else:
        return '暂无可用账号'