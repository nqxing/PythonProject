# 禁用安全请求警告 关闭SSL验证时用
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49'
                  ' Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
}
# mysql链接信息
HOST = 'localhost'
# HOST = '122.51.67.37'
USER = 'root'
PWD = 'MUGVHmugvtwja116ye38b1jhb'
# PWD = 'mm123456'


IS_DAILI = False  # 红包是否要加上代理访问
IS_HTTPS = True  # 是否关闭SSL证书验证 报443时打开此开关解决验证问题
XH_MAX = 35
ID_MAX = 35

PROXY = '59.44.247.194:9797'
PROXIES = {
    'http': 'http://' + PROXY,
    'https': 'https://' + PROXY
}

GARBAGE_PATH = r'garbage\garbage.db'
WZRY_PATH = r'bizhi\wzry\wzry.db'
YXLM_PATH = r'bizhi\yxlm\yxlm.db'
RILI_PATH = r'rili\rili.db'

KUQ_DATA_PATH = r'C:\CQA-xiaoi\data\173391006\eventv2.db' #服务器的kuq数据库地址
# KUQ_DATA_PATH = r'D:\CQA-xiaoi\data\173391006\eventv2.db' #本地的kuq数据库地址
ELEME_DATA_PATH = r'config\eleme.db'  # 账号数据库地址
# ELEME_DATA_PATH = r'D:\eleme\config\eleme.db'  # 账号数据库地址

DEFAULT_HB_TIME = 7  # 红包每隔多少秒查询一次，若报操作太快了请增加秒数
KQ_TIME = 60  # 每隔多少秒查询一次聊天记录
CX_MIN = 0  # 捕获多少分钟前的红包