#-*-coding:utf-8-*-
from PIL import Image

def test(path):
    img=Image.open(path)
    w,h=img.size
    for x in range(w):
        for y in range(h):
            r,g,b=img.getpixel((x,y))
            if 190<=r<=255 and 170<=g<=255 and 0<=b<=140:
                img.putpixel((x,y),(0,0,0))
            if 0<=r<=90 and 210<=g<=255 and 0<=b<=90:
                img.putpixel((x,y),(0,0,0))
    img=img.convert('L').point([0]*150+[1]*(256-150),'1')
    return img

for i in range(1,2):
    path = str(i) + '.jpg'
    im = test(path)
    path = path.replace('jpg','png')
    im.save(path)