# from PersonalDemo.dzbbs.dz import dz
from dz import dz
import time
from apscheduler.schedulers.blocking import BlockingScheduler

users = [
    # 541116212
    {
        'bbs_name': '村花',
        'user_name': '541116212',
        'cookie': 'n4XN_2132_saltkey=O6y04CZG; n4XN_2132_lastvisit=1582088626; _ga=GA1.2.658901050.1582092229; _gid=GA1.2.2147178131.1582092229; n4XN_2132_seccode=10277.f157fa75e7e26df2b7; n4XN_2132_ulastactivity=f8b4P4zOzeP39Di%2BGZUFBUiNbf9uKpnIUVvCXpbOz%2FWVwnKwpTGK; n4XN_2132_auth=d572k0doBek%2BraBwtZKOJ3JxNL%2BgzJpOZSWWZHfu2eEN8sXQjaa5jk5o7RR%2B2T0HmxwrhfngJLEZEgYfl1w69LXTQZc; n4XN_2132_lastcheckfeed=185393%7C1582092299; n4XN_2132_member_login_status=1; n4XN_2132_nofavfid=1; n4XN_2132_st_t=185393%7C1582092316%7Cba82340e083b9aaea6ceebe7aba57c51; n4XN_2132_atarget=1; n4XN_2132_forum_lastvisit=D_39_1582092316; n4XN_2132_visitedfid=39; n4XN_2132_smile=1D1; n4XN_2132_sid=T40050; n4XN_2132_lip=58.22.30.38%2C1582092299; n4XN_2132_st_p=185393%7C1582093128%7Cd9cf999e0d080b76b2f0e7339dcb4b69; n4XN_2132_viewid=tid_64956; _gat_gtag_UA_144688693_3=1; n4XN_2132_lastact=1582093163%09forum.php%09post; n4XN_2132_clearUserdata=forum; n4XN_2132_creditnotice=0D0D1D0D0D0D0D0D0D185393; n4XN_2132_creditbase=0D0D16D0D0D0D0D0D0; n4XN_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D',
        'formhash': 'e3df6bc4', #板块formhash 在帖子回复框页面可以查看
    },
    # 184417622
    {
        'bbs_name': '村花',
        'user_name': '184417622',
        # 账号cookie
        'cookie': 'n4XN_2132_saltkey=ANajsXx4; n4XN_2132_lastvisit=1582268927; n4XN_2132_sendmail=1; _ga=GA1.2.1671232547.1582272530; _gid=GA1.2.557064952.1582272530; n4XN_2132_sid=B6mqrO; n4XN_2132_seccode=14535.ee9222a1029a3ed05a; n4XN_2132_ulastactivity=5390Abx%2FdSpyfZMz2tUEUMgUueIixjQjjGS98ypMFj2YAARol%2Bm%2F; n4XN_2132_auth=5af3WN17hm1w832yb0xmbNzxkyMayJZW6rzQRT5bcfnTCQlii2h69YaUKWQ8nngwv7Gs7y5K7OnNE3GJeiaYDTogBow; n4XN_2132_lastcheckfeed=188243%7C1582272560; n4XN_2132_lip=58.22.30.38%2C1582272493; n4XN_2132_member_login_status=1; n4XN_2132_nofavfid=1; n4XN_2132_visitedfid=38; n4XN_2132_viewid=tid_51826; n4XN_2132_smile=1D1; n4XN_2132_st_p=188243%7C1582272645%7Cdec67718cf0203a71fc7127f31727755; n4XN_2132_lastact=1582272646%09home.php%09spacecp; n4XN_2132_checkpm=1; _gat_gtag_UA_144688693_3=1',
        'formhash': '29c0e33d',  # 板块formhash 在帖子回复框页面可以查看
    },
    # 541116212
    # {
    #     'bbs_name': '魔性',
    #     'user_name': '541116212',
    #     'cookie': '__cfduid=d5995b40c82bd3da039f850ecedfc9d961582178129; dyHK_2132_saltkey=MnD8wtDd; dyHK_2132_lastvisit=1582174530; _ga=GA1.2.1630525506.1582178133; _gid=GA1.2.385194512.1582178133; dyHK_2132_ulastactivity=9379JOd5btMJWHoUhKiaXmNflEa7vc%2FRbzsAd3vljufVmhaA2QAj; dyHK_2132_auth=3b84OnLUHO3ATdmFCNrRN3dRlJMjpbIerw2hwvwHR84SWskW9e9zhUULC%2F6O5Ub8mb7pVjHf6Ajz6sZ%2FMqBpCWlDA2E; dyHK_2132_lastcheckfeed=536622%7C1582178181; dyHK_2132_nofavfid=1; apt=1; dyHK_2132_atarget=1; dyHK_2132_visitedfid=46; dyHK_2132_st_t=536622%7C1582178336%7C989eb7f25ebcc72d27a0ec5719ace89d; dyHK_2132_forum_lastvisit=D_46_1582178336; dyHK_2132_sid=J58pPY; dyHK_2132_lip=58.22.30.38%2C1582178181; dyHK_2132_st_p=536622%7C1582178749%7C53bcf3e0a3518d052d4c794b4cb2254f; dyHK_2132_viewid=tid_228224; dyHK_2132_checkpm=1; dyHK_2132_sendmail=1; _gat_gtag_UA_153763458_4=1; dyHK_2132_smile=1D1; dyHK_2132_lastact=1582178771%09forum.php%09post; dyHK_2132_clearUserdata=forum; dyHK_2132_creditnotice=0D0D1D0D0D0D0D0D0D536622; dyHK_2132_creditbase=0D0D14D0D0D0D0D0D0; dyHK_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D',
    #     'formhash': '47539b05',  # 板块formhash 在帖子回复框页面可以查看
    # },
    # # 184417622
    # {
    #     'bbs_name': '魔性',
    #     'user_name': '184417622',
    #     # 账号cookie
    #     'cookie': '__cfduid=d92b792b07d447ee0603429aa93c36a731582251728; _ga=GA1.2.1629774824.1582251731; _gid=GA1.2.1051810722.1582251731; apt=1; dyHK_2132_saltkey=owsisUBf; dyHK_2132_lastvisit=1582248327; dyHK_2132_secqaa=1128.28e7b84bc767c9b949; dyHK_2132_seccode=1129.3d92b9e65cd3d144e6; dyHK_2132_sendmail=1; dyHK_2132_sid=c9KUDt; dyHK_2132_ulastactivity=d53eNoY%2FTDaR%2FBn8mesF5qIw%2BZx3hjlO7LC3DUwvhGQ0V7FpVohk; dyHK_2132_auth=e66411aafGMCkj2V5eOSJxcqb57sF%2B7sj4SO1PqwVUg3wVSRR6gUqEiXNnFBII4bbjBf3Mks7LVb2lS4tGMtvemRWms; dyHK_2132_lastcheckfeed=537213%7C1582252526; dyHK_2132_checkfollow=1; dyHK_2132_lip=122.51.67.37%2C1582252209; dyHK_2132_nofavfid=1; dyHK_2132_checkpm=1; dyHK_2132_creditnotice=0D0D2D0D0D0D0D0D0D537213; dyHK_2132_creditbase=0D0D10D0D0D0D0D0D0; dyHK_2132_lastact=1582252548%09plugin.php%09; _gat_gtag_UA_153763458_4=1',
    #     'formhash': '5e565624',  # 板块formhash 在帖子回复框页面可以查看
    # }
]

cunh_bbs_dict = {
    'host': 'https://www.cunhua.co', #论坛地址
    'fid': '39', #版块ID值
    'page_max': 150, #该版块下帖子最大页数
    'fid_url': '/forum-{}-{}.html', #版块的url格式 第一个花括号对应版块ID 第二个花括号对应页数
    'jinb_name': '金币', #该论坛金币名称
    'reply_second': 50, #该论坛回帖间隔时间 单位秒
    'hour_reply_num': 30, #该论坛每小时可回帖数
    'tid_split': True #论坛帖子链接是否需要切割
}

mox_bbs_dict = {
    'host': 'https://www.moxing.one', #论坛地址
    #账号cookie
    'fid': '46', #版块ID值
    'page_max': 366, #该版块下帖子最大页数
    'fid_url': '/forum.php?mod=forumdisplay&fid={}&page={}', #版块的url格式 第一个花括号对应版块ID 第二个花括号对应页数
    'jinb_name': '软妹币', #该论坛金币名称
    'reply_second': 40, #该论坛回帖间隔时间 单位秒
    'hour_reply_num': 5, #该论坛每小时可回帖数
    'tid_split': False
}

def sign():
    for u in users:
        if u['bbs_name'] == '村花':
            new_bbs_dict = dict(cunh_bbs_dict, **u)
        else:
            new_bbs_dict = dict(mox_bbs_dict, **u)
        dz.sign(new_bbs_dict)
        time.sleep(3)

def reply():
    for u in users:
        if u['bbs_name'] == '村花':
            new_bbs_dict = dict(cunh_bbs_dict, **u)
        else:
            new_bbs_dict = dict(mox_bbs_dict, **u)
        dz.main(new_bbs_dict)
        time.sleep(3)

def main():
    sign()
    reply()

main()
scheduler = BlockingScheduler()
# hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
scheduler.add_job(main,  'cron', hour=14, minute=00)

dz.sava_txt('定时回帖任务已启动')
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    dz.sava_txt('定时任务出现异常')