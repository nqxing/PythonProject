# from PIL import Image
from ctypes import *
import requests

# obj= CDLL(r"D:\PythonProject\PersonalDemo\code_identify\demo.dll")

# #print(obj)
# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
#
#
#
#
# if __name__=="__main__":
#
#     img = get_file_content(r'D:\PythonProject\PersonalDemo\code_identify\1.jpg')
#     print(type(img))
#     dz=obj.ocr(img, len(img))
#     print("\n\n\n\n" +str(dz) + "\n\n\n\n")

def cx_code(img):
    obj = CDLL(r"D:\PythonProject\PersonalDemo\code_identify\demo.dll")
    dz = obj.ocr(img, len(img))
    return str(dz)
url = 'https://passport2.chaoxing.com/num/code'
mysession = requests.Session()
r = mysession.get(url, timeout=60 * 4)
if r.status_code == 200:
    yzm = cx_code(r.content)
    print(yzm)
