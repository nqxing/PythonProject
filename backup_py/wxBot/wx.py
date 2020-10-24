from wxpy import *
import re

# 初始化机器人，扫码登陆
bot = Bot(cache_path=True)
bot.enable_puid('wxpy_puid.pkl')
# friends = bot.friends()
# print(len(friends))
# for f in friends:
#     print(f, f.wxid, "是否好友：{}".format(f.is_friend))
@bot.register() #Friend
def print_others(msg):
    msg_type, text, sender = msg.type, msg.text, msg.sender
    print(text)
    # puid = (msg.sender.puid,)
    # print(msg_type)
    # beizhu = re.findall(':(.*?)>', str(msg.sender))[0].strip()
    # beizhu = (beizhu,)
    # # logger.info('{} 发送了 > {}'.format(beizhu[0], text))
    # print('{} 发送了 > {}'.format(beizhu[0], text))
    # msg.reply('xx')
    # fid = bot.search('Bot')[0]
    # msg.forward(fid, prefix='老板发言')
    # print('{}'.format(raws))
    # msg.reply_raw_msg(raws)

    if msg_type == 'Sharing':
        print(msg.url)

bot.join()