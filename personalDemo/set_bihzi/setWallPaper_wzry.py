import requests
from random import randint  # 随机函数
import win32api,win32con,win32gui
from PIL import Image
import os
def get_yingx():
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    json_url = 'https://pvp.qq.com/web201605/js/herolist.json'
    dicList = requests.get(json_url,headers=headers).json()
    bianhao = input_bianhao()
    if bianhao == 0:
        i = randint(0,len(dicList)-1)
        yinxNum = dicList[i]['ename']
        pifNameList = dicList[i]['skin_name'].split('|')
        pifNum =  randint(1,len(pifNameList))
        get_pifImg(yinxNum, pifNum)
    else:
        yinx_list(dicList)
def get_pifImg(Ybianhao,Pbianhao):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    pifImg_url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'
    imagePath = r'D:/wallpaper.jpg'
    imgUrl = pifImg_url.format(Ybianhao,Ybianhao,Pbianhao)
    img = requests.get(imgUrl, headers=headers)
    with open(imagePath, "wb") as f:
        f.write(img.content)
    setWallPaper(imagePath)
def yinx_list(dicList):
    count = 0
    for d in range(len(dicList)):
        yinxNum = dicList[d]['ename']
        yinxName = dicList[d]['cname']
        if len(yinxName) == 1:
            yinxNum = str(yinxNum)+' '*6
        if len(yinxName) == 2:
            yinxNum = str(yinxNum)+' '*4
        if len(yinxName) == 3:
            yinxNum = str(yinxNum)+' '*2
        yingx = '{}-{}'.format(yinxName,yinxNum)
        print(yingx,end='\t\t')
        count += 1
        if (count % 8 == 0) or d == len(dicList)-1:
            print(end='\n')  # 换行输出
    Ybianhao = input_Ybianhao()
    for i in range(len(dicList)):
        if dicList[i]['ename'] == Ybianhao:
            pifNameList = dicList[i]['skin_name'].split('|')
            for p in range(len(pifNameList)):
                pifName = '{}:{}'.format(p+1,pifNameList[p])
                print(pifName)
    Pbianhao = input_Pbianhao()
    get_pifImg(Ybianhao,Pbianhao)
def input_bianhao():
    print('0:随机设置')
    print('1:自行选择')
    bianhao = input("功能选择，请输入编号: ")
    print('---------------------------------')
    try:
        return int(bianhao)
    except Exception:
        print('你输入的编号有误，请重新输入~~')
        return input_bianhao()
def input_Ybianhao():
    print('---------------------------------')
    bianhao = input("请输入英雄编号: ")
    print('---------------------------------')
    try:
        return int(bianhao)
    except Exception:
        print('你输入的编号有误，请重新输入~~')
        return input_Ybianhao()
def input_Pbianhao():
    print('---------------------------------')
    bianhao = input("请输入皮肤序号: ")
    print('---------------------------------')
    try:
        return int(bianhao)
    except Exception:
        print('你输入的序号有误，请重新输入~~')
        return input_Pbianhao()
def setWallpaperFromBMP(newPath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, newPath, 1 + 2)
    # win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, win32con.SPIF_SENDWININICHANGE)
# convert jpg to bmp
def setWallPaper(imagePath):
    bmpImage = Image.open(imagePath)
    newPath = imagePath.replace('.jpg', '.bmp')
    bmpImage.save(newPath, "BMP")
    setWallpaperFromBMP(newPath)
    print('壁纸设置成功~')
    if (os.path.exists(imagePath)):
        os.remove(imagePath)
get_yingx()