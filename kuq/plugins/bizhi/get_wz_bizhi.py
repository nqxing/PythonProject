from nonebot import on_command, CommandSession
import requests
from config import GET_WZ_WALL_HOST

@on_command('wz_bizhi')
async def wz_bihzi(session: CommandSession):
    # print(session.state)
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    hero_name = session.state.get('hero_name')
    try:
        result = requests.get(GET_WZ_WALL_HOST.format(hero_name))
        await session.send(result.text)
    except:
        await session.send("系统异常，请联系群主处理")



