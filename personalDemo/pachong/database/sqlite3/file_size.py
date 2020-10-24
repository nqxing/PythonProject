import os
import time
import asyncio
# print(os.path.getsize(r'D:\360安全浏览器下载\CQA-xiaoi\酷Q Air\data\184417622\eventv2.db'))
# print(int(time.time()))

# os.system(r'D:\PythonProject\PersonalDemo\pachong\eleme\1.bat')
# print('执行这句了')
# time.sleep(50)


async def test():
    asyncio.sleep(3)
    print('ces')
    time.sleep(10)

def run():
    i = 0
    while True:
        print('循环')
        i+=1
        if i >6:
            print('进来了')
            loop.run_until_complete(test())
            print('到这了')

loop = asyncio.get_event_loop()
if __name__ =='__main__':
    run()