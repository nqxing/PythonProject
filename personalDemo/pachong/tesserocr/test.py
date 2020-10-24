import tesserocr
from PIL import Image
image=Image.open('captcha.jpgs')

image = image. convert('L')
threshold = 200
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table,'1')
image. show()

t = tesserocr.image_to_text(image)
print(t)
print(type(t))
print(len(t))