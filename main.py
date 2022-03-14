from itertools import chain
from math import floor
import numpy as np
from re import A, sub
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

def createImgFromBin(img_2d_list, filename):
    flat = list(chain.from_iterable(img_2d_list))
    im2 = Image.new('1', (len(img_2d_list), len(img_2d_list[0])))
    im2.putdata(flat)
    im2.save('./out/'+filename+'.png')

def getsubgrid(origin, size, grid):
    offset = floor(size/2)
    grid = np.array(grid)
    return grid[origin[0] - offset:origin[0] + offset+1,
                origin[1] - offset:origin[1] + offset+1]

def erosion_is_ok(eroder, to_erode):
    flat_eroder = list(chain.from_iterable(eroder))
    flat_to_erode = list(chain.from_iterable(to_erode))
    
    for i in range(0, len(flat_eroder)):
        if flat_eroder[i] == 1 and flat_eroder[i] != flat_to_erode[i]:          
            return False 
    return True

def erosion(bin_img, eroder=[[1 for x in range(3)] for y in range(3)]):
    height, width = len(bin_img), len(bin_img[0])
    eroder_size = len(eroder)
    offset = floor(eroder_size/2)
    output=np.array([[0 for x in range(width)] for y in range(height)])
    for i in range(offset,height-offset):
        for j in range(offset, width-offset):
            subarray = getsubgrid((i,j),eroder_size,a)
            output[i,j] = int(erosion_is_ok(eroder, subarray))

    createImgFromBin(output, "retest")



a = [[0, 0, 0, 0, 0, 0, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0]]

erosion(a, eroder=[[1 for x in range(5)] for y in range(5)])

images = getImages()

for image in images:
    if image != '.DS_Store':
        with Image.open("./projetOCR/chiffres/"+image) as img:
            avgEachPixel(img, image)


