import psutil
import os
import time
cmd_pids = []
py_pids = []
def get_pids(name):
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        process_name = p.name()
        # print(process_name, pid)
        if process_name == name:
            # print(p.cwd())
            # 获取当前路径的上级路径
            # print(os.path.abspath(os.path.dirname(os.getcwd())))
            # time.sleep(50)
            if p.cwd() == os.getcwd():
                # print(pid)
                cmd_pids.append(pid)
def kill(name, cmd_pids):
    for pid in cmd_pids:
        try:
            os.popen('taskkill.exe /pid:' + str(pid))
            print('{}[{}] 程序进程关闭成功~~'.format(name, pid))
        except Exception as e:
            print('{}[{}] 程序进程关闭失败~~'.format(name, pid))
print("正在关闭目标程序~~")
get_pids('cmd.exe')
if cmd_pids:
    kill('cmd.exe', cmd_pids)
get_pids('python.exe')
if py_pids:
    kill('python.exe', py_pids)
print('3秒后自动退出...')
time.sleep(3)
