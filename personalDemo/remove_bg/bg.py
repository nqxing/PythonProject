
# from removebg import RemoveBg
#
# rmbg = RemoveBg("g3zfQHgjWa82U5tmFWQoFRW7", "error.log") # 引号内是你获取的API
#
# rmbg.remove_background_from_img_file("1.jpg") #图片地址
from PIL import Image

im = Image.open('1212.png')
x,y = im.size
try:
  # 使用白色来填充背景 from：www.jb51.net
  # (alpha band as paste mask).
  p = Image.new('RGBA', im.size, (211, 211, 211))
  p.paste(im, (0, 0, x, y), im)
  p.save('12120.png')
except:
  pass