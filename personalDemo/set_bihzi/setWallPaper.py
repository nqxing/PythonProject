import requests
import json
import win32api,win32con,win32gui
from PIL import Image
def main():
    r = requests.get('http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1')
    res = r.content.decode('utf-8')
    response = json.loads(res)
    url = response['images'][0]['url']
    a = requests.get('http://cn.bing.com' + url)
    imagepath = r'D:\img.jpg'
    with open(imagepath, 'wb') as f:
        f.write(a.content)
    setWallPaper(imagepath)
def setWallpaperFromBMP(imagepath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, 1 + 2)
# convert jpg to bmp
def setWallPaper(imagePath):
    bmpImage = Image.open(imagePath)
    newPath = imagePath.replace('.jpg', '.bmp')
    bmpImage.save(newPath, "BMP")
    setWallpaperFromBMP(newPath)
    print('壁纸设置成功~')
main()