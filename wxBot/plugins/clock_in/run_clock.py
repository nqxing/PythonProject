from plugins.clock_in.send_daka import send_daka_index
from plugins.ele_sign.send_sign import send_sign_index
from plugins.push_msg.game_push import push_game_index
from config.pub_sql_bak import bak_sql_index
from config.fun_api import *

def clock(bot):
    # 打卡提醒服务
    # week_int = datetime.datetime.now().weekday()
    sign_time = datetime.datetime.now().strftime('%H:%M')

    # if week_int != 5 and week_int != 6: # 周末不提醒，5代表星期六
    #     # 该方法是异步执行
    #     send_daka_index(bot)

    # if sign_time == '09:00':
    #     # logger.info('开始执行饿了么签到')
    #     # 该方法是异步执行
    #     send_sign_index(bot)

    if sign_time == '10:00':
        # 更新王者信息库
        result = requests.get("http://127.0.0.1:90/robot/UPwzInfo/")

    # 更新饿了么状态
    # if sign_time == '00:00':
    #     SQL().up_state()

    if sign_time == '01:00':
        # 该方法是异步执行 备份sql
        bak_sql_index()
    # 该方法是异步执行 发送王者、英雄联盟新闻和更新的新壁纸信息
    push_game_index(bot)


def mon_clock(bot):
    while True:
        if datetime.datetime.now().strftime('%S') == "01":
            break
        time.sleep(0.5)
    write_log(1, "监控系统准备运行，现在退出循环")
    clock(bot)
    write_log(1, '指令执行成功，监控系统运行中...')
    scheduler = BlockingScheduler()
    # hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
    scheduler.add_job(lambda: clock(bot), 'interval', minutes=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('定时任务出现异常')