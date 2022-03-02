from PIL import Image
from os import walk

def avgEachPixel(img, name):
    # imgName = img.info["filename"]
    path = './clean/'+name+''
    imagePixels = list(img.getdata())
    newImage = []
    for p in imagePixels:
        avg = (p[0]+p[1]+p[2])/3
        if avg >= 255/2:
            newImage.append((255,255,255))
        else:
            newImage.append((0,0,0))       

    im2 = Image.new(img.mode, img.size)
    im2.putdata(newImage)
    im2.save(path)
    
def getImages():
    return next(walk("./projetOCR/chiffres/"), (None, None, []))[2]

images = getImages()

for image in images:
    if image != '.DS_Store':
        with Image.open("./projetOCR/chiffres/"+image) as img:
            avgEachPixel(img, image)


