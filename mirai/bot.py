from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend
from graia.application.group import Group
from plugins.wzry.reply import group_reply
from plugins.pub_fun.fun_api import *

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="541116212", # 填入 authKey
        # account=184417622, # 你的机器人的 qq 号
        account=173391006, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

# @bcc.receiver("FriendMessage")
# async def friend_message_listener(msg: MessageChain, app: GraiaMiraiApplication, friend: Friend):
#     print(msg.has(Plain))
#     p = msg.get(Plain)
#     print(p[0].text)
#     print(friend.id)
#     await app.sendFriendMessage(friend, MessageChain.create([
#         Plain("Hello, World!")
#     ]))

@bcc.receiver("GroupMessage")
async def friend_message_listener(msg: MessageChain, app: GraiaMiraiApplication, group: Group):
    try:
        if msg.has(Plain):
            p = msg.get(Plain)
            rep_str = group_reply(p[0].text)
            # print(group.id)
            if rep_str:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain(rep_str)
                ]))
    except:
        write_log(3, traceback.format_exc())

# @bcc.receiver("FriendRecallEvent")
# async def friend_ch():
#     pass
app.launch_blocking()