from config.fun_api import *

class my_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        bak_sql()
def bak_sql_index():
    th = my_thread()
    th.start()

def bak_sql():
    try:
        # os.system(r'cd C:\HuWs\PHPWEB\MySQL Server 5.6\bin') windows路径
        os.system(r'cd /usr/local/mysql/bin')
        # file_name = 'C:\PythonProject\public_{}.sql'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) windows路径
        file_name = '/root/python/sql_bak/public_{}.sql'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        os.system(r'mysqldump -u{} -p{} {} > {}'.format(USER, PWD, DB_NAME, file_name))
        if (os.path.exists(file_name)):
            bp = ByPy()
            bp.upload(localpath="{}".format(file_name), remotepath='sql', ondup='overwrite')
            os.remove(file_name)
    except:
        write_log(3, traceback.format_exc())
