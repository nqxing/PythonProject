import requests
from random import randint  # 随机函数
from bs4 import BeautifulSoup
import os
import datetime
import win32api,win32con,win32gui
from PIL import Image
def getImg():
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    url = 'https://bing.ioliu.cn/?p={}'.format(randint(1,93))
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.content, 'lxml')
    itemList = soup.find_all(class_='item')
    aLink = 'https://bing.ioliu.cn{}'.format(itemList[randint(0,len(itemList)-1)].find(name='a')['href'])
    aHtml = requests.get(aLink,headers=headers)
    aSoup = BeautifulSoup(aHtml.content, 'lxml')
    # print(aSoup)
    imgUrl = aSoup.find(class_='progressive').find(name='img')['data-progressive']
    img_path = "D:/bingPhoto/"
    folder = os.path.exists(img_path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(img_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    # img_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    img = requests.get(imgUrl, headers=headers)
    with open(img_path  + "wallpaper.jpg", "wb") as f:
        f.write(img.content)
    imagePath = r'{}wallpaper.jpg'.format(img_path)
    setWallPaper(imagePath)
def setWallpaperFromBMP(newPath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, newPath, 1 + 2)
    # win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, win32con.SPIF_SENDWININICHANGE)
# convert jpg to bmp
def setWallPaper(imagePath):
    bmpImage = Image.open(imagePath)
    bmpImage = Image.open(imagePath)
    newPath = imagePath.replace('.jpg', '.bmp')
    bmpImage.save(newPath, "BMP")
    setWallpaperFromBMP(newPath)
    print('壁纸设置成功~')
    if (os.path.exists(imagePath)):
        os.remove(imagePath)
getImg()