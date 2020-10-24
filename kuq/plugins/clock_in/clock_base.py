from plugins.pub_fun.fun_api import *
from config import *

def daka_open(qq):
    values = SQL().select_clock(qq)
    if values and values[0][0] != None and values[0][1] != None:
        values = SQL().select_clock_open1(qq)
        tx_time_str = values[0][1]
        state_str = values[0][0]
        if state_str == True and tx_time_str == None:
            card_dict[qq] = 'up_time'
            return '您已开启打卡提醒，但还未设置提醒时间，现在回复时间设置吧'
        elif state_str == False and tx_time_str == None:
            card_dict[qq] = 'up_time'
            SQL().up_clock_open1(qq)
            return '您的打卡提醒开启成功，但还未设置提醒时间，现在回复时间设置吧'
        elif state_str == False and tx_time_str != None:
            card_dict[qq] = 'up_time'
            SQL().up_clock_open1(qq)
            return '您的打卡提醒开启成功，当前设置的提醒时间为（{}），如需更改请重新发送时间哦'.format(tx_time_str)
        else:
            return '您已开启打卡提醒，无需再次开启，若您要关闭提醒请发送“关闭打卡提醒”'
    else:
        # msg.sender.send_image('public.jpg')
        return '您未开启打卡提醒或未与公众号绑定，无法直接开启\n请打开微信搜一搜，关注公众号(最趣分享)后发送关键字“打卡提醒”进行开启或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU'

def daka_close(qq):
    values = SQL().select_clock(qq)
    if values and values[0][0] != None and values[0][1] != None:
        state_str = SQL().select_clock_open1(qq)[0][0]
        if state_str == True:
            SQL().up_clock_open2(qq)
            return '您的打卡提醒已关闭，发送“开启打卡提醒”可再次开启哦'
        elif state_str == False:
            return '您的打卡提醒已是关闭状态，无需重复关闭'
    else:
        # msg.sender.send_image('public.jpg')
        return '您未开启打卡提醒或未与公众号绑定，无法直接关闭\n请打开微信搜一搜，关注公众号(最趣分享)后发送关键字“打卡提醒”进行开启或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU'

def daka_update_time(qq, text):
    text = text.replace(' ', '')
    text = text.replace('：', ':')
    values = SQL().select_clock_open1(qq)
    state_str = values[0][0]
    time_list = values[0][1]
    if state_str == True or time_list == None:
        if '，' in text and '：' in text:
            text = text.replace('，', ',')
            text = text.replace('：', ':')
        if '，' in text:
            text = text.replace('，', ',')
        if '：' in text:
            text = text.replace('：', ':')
        if ',' in text:
            tx_time_list = []
            tx_times = text.split(',')
            if len(tx_times) < 5:
                for tx in tx_times:
                    if ':' in tx:
                        tx_list = tx.split(':')
                        if len(tx_list) == 2 and len(tx_list[0]) < 3 and len(tx_list[1]) < 3:
                            txs = is_time(tx)
                            if len(txs) == 5:
                                tx_time_list.append(txs)
                            else:
                                return txs
                        else:
                            return '时间格式不正确，请修改后重新发送'
                    else:
                        return '时间格式不正确，请修改后重新发送'
                if len(tx_times) == len(tx_time_list):
                    tx_time_list = ','.join(tx_time_list)
                    SQL().up_clock_times(qq, tx_time_list, len(tx_times))
                    value = card_dict.pop(qq)
                    return '恭喜你，时间设置成功，到点您会收到打卡提醒哦（注：如需修改请重新发送时间即可）'
            else:
                return '最多只能设置4个时间哦'
        else:
            if ':' in text:
                text_list = text.split(':')
                if len(text_list) == 2 and len(text_list[0]) < 3 and len(text_list[1]) < 3:
                    txs = is_time(text)
                    if len(txs) == 5:
                        SQL().up_clock_times(qq, txs, 1)
                        value = card_dict.pop(qq)
                        return '恭喜你，时间设置成功，到点您会收到打卡提醒哦（注：如需修改请重新发送时间即可）'
                    else:
                        return txs
                else:
                    return '时间格式不正确，请修改后重新发送'
            else:
                return '时间格式不正确，请修改后重新发送'
    elif state_str == False and time_list != None:
        return '您已关闭打卡提醒，不可以修改提醒时间哦'

def is_time(tx_time):
    hours = None
    min = None
    nums = tx_time.split(':')
    if nums[0].isdigit():
        if len(nums[0]) == 1:
            hours = '0{}'.format(nums[0])
        elif len(nums[0]) == 2 and int(nums[0]) < 24:
            hours = nums[0]
        else:
            return '小时格式不正确，请修改后重新发送'
    else:
        return '小时格式不正确，请修改后重新发送'
    if nums[1].isdigit():
        if len(nums[1]) == 1:
            min = '0{}'.format(nums[1])
        elif len(nums[1]) == 2 and int(nums[1]) < 60:
            min = nums[1]
        else:
            return '分钟格式不正确，请修改后重新发送'
    else:
        return '分钟格式不正确，请修改后重新发送'
    if hours != None and min != None:
        return '{}:{}'.format(hours, min)