from apscheduler.schedulers.blocking import BlockingScheduler
def t1(x):
    print(x)
    x += 1
def t2():
    x = 0
    scheduler = BlockingScheduler()
    # hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
    scheduler.add_job(lambda: t1(x), 'interval', seconds=3)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('定时任务出现异常')
t2()