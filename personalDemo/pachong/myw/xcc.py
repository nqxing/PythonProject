# from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
#
# import os,time,random
# def task(n,m):
#     print('%s is runing' %os.getpid())
#     print(m)
#     s = random.randint(1,3)
#     time.sleep(s)
#     print('%s等待了%s秒'%(os.getpid(),s))
#     return n**2
#
# if __name__ == '__main__':
#
#     executor=ProcessPoolExecutor(max_workers=5)
#
#     futures=[]
#     for i in range(11):
#         future=executor.submit(task,i,i+1)
#         futures.append(future)
#     executor.shutdown(True)
#     print('+++>')
#     for future in futures:
#         print(future.result())
import os

save_path = r'D:\KDW'
folder = os.path.exists(save_path)
if not folder:
    os.makedirs(save_path)
