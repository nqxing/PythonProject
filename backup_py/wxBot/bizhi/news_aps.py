from apscheduler.schedulers.blocking import BlockingScheduler
from bizhi.wzry.get_wzry_news import get_news_wzry
from bizhi.yxlm.get_yxlm_news import get_news_yxlm

def main(groups):
    get_news_wzry(groups['wzry'])
    get_news_yxlm(groups['yxlm'])

def index_news(groups):
    main(groups)
    scheduler = BlockingScheduler()
    # hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
    scheduler.add_job(lambda: main(groups), 'interval', minutes=30)
    print('王者荣耀、英雄联盟新闻监控任务运行中，每隔30分钟执行一次')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('定时任务出现异常')