from auto_reply.package import *

def card_open(fromUser):
    values = pubCardUsers.objects.filter(wx_open_id=fromUser)
    if values.exists():
        value = values[0]
        if value.state == True and value.time_list == None:
            return '请在5分钟内回复你要提醒的时间，如：09:00,18:00（注：多个时间之间用逗号隔开哦，最多可设置4个时间）'
        elif value.state == False and value.time_list == None:
            value.state = True
            value.save()
            return '请在5分钟内回复你要提醒的时间，如：09:00,18:00（注：多个时间之间用逗号隔开哦，最多可设置4个时间）'
        elif value.time_list != None:
            value.state = True
            value.save()
            if value.bind_name == None:
                pwd = get_bind_name(fromUser, 0)
                return '您当前已设置提醒时间为（{}），但还未绑定微信/QQ，绑定后即可收到打卡提醒哦\n\n{}'.format(value.time_list, pwd)
            else:
                pwd = get_bind_name(fromUser, 0)
                return '您当前设置的提醒时间为（{}），如需更改请在5分钟内回复你要提醒的新时间哦\n\n{}'.format(value.time_list, pwd)
        else:
            return '您当前设置的提醒时间为（{}），如需更改请在5分钟内回复你要提醒的新时间哦，如：09:00,18:00（注：多个时间之间用逗号隔开哦，最多可设置4个时间）'.format(value.time_list)
    else:
        pub = pubCardUsers()
        pub.wx_open_id = fromUser
        pub.save()
        return '请在5分钟内回复你要提醒的时间，如：09:00,18:00（注：多个时间之间用逗号隔开哦，最多可设置4个时间）'

def card_set_time(text, fromUser):
    text = text.replace(' ', '')
    text = text.replace('：', ':')
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
                values = pubCardUsers.objects.filter(wx_open_id=fromUser)
                value = values[0]
                value.time_list = tx_time_list
                value.time_num = len(tx_times)
                value.state = True
                value.save()
                pwd = get_bind_name(fromUser, 1)
                if '你已绑定' in pwd:
                    return '恭喜你，时间设置成功，到点您会收到打卡信息哦\n\n{}'.format(pwd)
                return '恭喜你，时间设置成功，但还未绑定微信/QQ，绑定后即可收到打卡提醒哦\n\n{}'.format(pwd)
        else:
            return '最多只能设置4个时间哦'
    else:
        if ':' in text:
            text_list = text.split(':')
            if len(text_list) == 2 and len(text_list[0]) < 3 and len(text_list[1]) < 3:
                txs = is_time(text)
                if len(txs) == 5:
                    values = pubCardUsers.objects.filter(wx_open_id=fromUser)
                    value = values[0]
                    value.time_list = txs
                    value.time_num = 1
                    value.state = True
                    value.save()
                    pwd = get_bind_name(fromUser, 1)
                    if '你已绑定' in pwd:
                        return '恭喜你，时间设置成功，到点您会收到打卡信息哦\n\n{}'.format(pwd)
                    return '恭喜你，时间设置成功，但还未绑定微信/QQ，绑定后即可收到打卡提醒哦\n\n{}'.format(pwd)
                else:
                    return txs
            else:
                return '时间格式不正确，请修改后重新发送'
        else:
            return '时间格式不正确，请修改后重新发送'

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