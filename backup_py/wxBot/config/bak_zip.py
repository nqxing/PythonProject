import os
import zipfile
import datetime
def zipDir(dirpath,outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w",zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()

# 生成mysql备份文件并执行备份mysql饿了么账号库
strlist = [r'cd C:\HuWs\PHPWEB\MySQL Server 5.6\bin', r'mysqldump -uroot -pMUGVHmugvtwja116ye38b1jhb public > C:\PythonProject\public.sql']
for s in strlist:
    with open(r"C:\PythonProject\1.bat", "a", encoding='utf-8') as f:
        f.write(s+'\n')
os.system(r'C:\PythonProject\1.bat')

# 生成压缩包
stime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
filename = 'wxBot_bak_{}.zip'.format(stime)
zipDir(r'C:\PythonProject\wxBot', r'C:\PythonProject\{}'.format(filename))

# 生成百度云上传bat文件并执行 bypy upload D:\PythonProject\ /wzry 上传到指定路径
strlist1 = [r'bypy upload C:\PythonProject\{}'.format(filename), r'del C:\PythonProject\{}'.format(filename)]
for s in strlist1:
    with open(r"C:\PythonProject\2.bat", "a", encoding='utf-8') as f:
        f.write(s+'\n')
os.system(r'C:\PythonProject\2.bat')

# 删除生成的bat文件和sql数据库
if(os.path.exists(r"C:\PythonProject\1.bat")):
    os.remove(r"C:\PythonProject\1.bat")
if(os.path.exists(r"C:\PythonProject\2.bat")):
    os.remove(r"C:\PythonProject\2.bat")
if(os.path.exists(r"C:\PythonProject\wxBot\eleme_id.sql")):
    os.remove(r"C:\PythonProject\wxBot\eleme_id.sql")