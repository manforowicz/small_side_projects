from PIL import Image, ImageEnhance, ImageDraw
import random

background = Image.new('RGB',(3840,2160),(0,0,0))

depthmap = Image.open('depthmap.png')
depthmap = depthmap.convert("L")

'''im = Image.open('nature.jpg')

w,h=im.size
im = im.crop((w/2,0,h/4+w/2,h))
im = im.resize((100,400))


w,h = im.size
for x in range(w):
    for y in range(h):
        r,g,b = im.getpixel((x,y))
        r = r+random.randrange(-100,100)
        g = g+random.randrange(-100,100)
        b = b+random.randrange(-100,100)
        im.putpixel((x,y),(r,g,b))

enhancer = ImageEnhance.Sharpness(im)
im = enhancer.enhance(4.0)'''

im = Image.new('RGB',(480,2160),(0,0,0))
w,h = im.size
for i in range(4000):
    r = random.randrange(0,255)
    g = random.randrange(0,255)
    b = random.randrange(0,255)
    x = random.randrange(-50,w)
    y = random.randrange(-50,h)
    draw = ImageDraw.Draw(im)
    draw.ellipse([(x,y),(x+50,y+50)],fill=(r,g,b))


background.paste(im,(0,0))
w,h = background.size
for x in range(480,w):
    for y in range(h):
        depth = depthmap.getpixel((x,y))
        depth = depth//4
        pixel = background.getpixel((x-480+depth,y))
        background.putpixel((x,y),pixel)

background.save('background.png',"PNG")
