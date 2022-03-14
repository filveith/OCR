from traceback import print_tb
from PIL import Image, ImageOps
from os import walk
from itertools import chain
from math import floor
import numpy as np
from re import A, sub

def unBlur(img, name):
    path = './clean/'+name+''
    imagePixels = list(img.getdata())
    newImage = []
    for p in imagePixels:
        if p >= 255/2:
            newImage.append(255)
        else:
            newImage.append(0)       

    print(newImage)

    im2 = Image.new(img.mode, img.size)
    im2.putdata(newImage)
    im2.save(path)
    return im2
    
def createImgFromBin(img_2d_list, filename, width=10, height=10):
    flat = list(img_2d_list)
    # Check if list is nested or not (if yes we flaten it)
    if any(isinstance(i, list) for i in img_2d_list): 
        flat = list(chain.from_iterable(img_2d_list))
        width = len(img_2d_list[0])
        height = len(img_2d_list)

    im2 = Image.new('1', (height, width))
    im2.putdata(flat)
    im2.save('./clean/'+filename)

def getBinaryImg(img):
    imagePixels = list(img.getdata())
    binaryImage = []
    width, height = img.size
    nb = 0
    row = []
    for p in imagePixels:
        nb += 1
        if p == 255:
            row.append(1)
        else:
            row.append(0)   

        if width == nb:
            binaryImage.append(row)
            nb = 0
            row = []

    # print(binaryImage)
    return binaryImage

def zoning(img, nb_zones = 4):
    refImg = './projetOCR/Reference/1.png'
    ukwImg = './ProjetOCR/clean/1_1.png'
    
    return 0

def dilatation(img, dilater_size=3):
    imagePixels = list(img.getdata())
    newImage = imagePixels

    width, height = img.size
    print(imagePixels)

    for i, p in enumerate(imagePixels):
        print(p)
        if p == 255:
            for x in range(width*-1,width*2,width):
                for y in range(dilater_size):
                    try:
                        print("x: ",x," y: ",y," i: ",i,"  co:",(i+x+y)," value: ",imagePixels[(i+x)+y])
                        if imagePixels[(i+x)+y] == 0:
                            print("255")
                            newImage[(i+x)+y] = 255
                    except:
                        pass

    print(newImage)
    createImgFromBin(newImage, 'res_dilatation', img.size[0], img.size[1])
    return newImage

def getsubgrid(origin, size, grid):
    offset = floor(size/2)
    grid = np.array(grid)
    return grid[origin[0] - offset:origin[0] + offset+1,
                origin[1] - offset:origin[1] + offset+1]

def erosion_is_ok(eroder, to_erode):
    flat_eroder = list(chain.from_iterable(eroder))
    flat_to_erode = list(chain.from_iterable(to_erode))
    print(flat_eroder, flat_to_erode)
    print()
    for i in range(0, len(flat_eroder)):
        if flat_eroder[i] == 1 and flat_eroder[i] != flat_to_erode[i]:          
            return False 
    return True
        

def erosion(bin_img, imageName, eroder=[[1 for x in range(3)] for y in range(3)]):
    print(imageName, bin_img)
    height, width = len(bin_img), len(bin_img[0])
    print(width, height)
    eroder_size = len(eroder)
    offset = floor(eroder_size/2)
    output=np.array([[0 for x in range(width)] for y in range(height)])
    for i in range(offset,height-offset):
        for j in range(offset, width-offset):
            subarray = getsubgrid((i,j),eroder_size,a)
            output[i,j] = int(erosion_is_ok(eroder, subarray))

    createImgFromBin(output, imageName)


# with ImageOps.grayscale(Image.open("./out/dilatation.png")) as img:
#     dilatation(img) 



a = [[0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 1, 1, 0, 0],
     [0, 0, 1, 1, 1, 0, 0],
     [0, 0, 1, 0, 1, 0, 0],
     [0, 0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 0]]    



# createImgFromBin(a, 'dilatation')

def getImages():
    return next(walk("./projetOCR/chiffres/"), (None, None, []))[2]

def getCleanImages():
    return next(walk("./clean/"), (None, None, []))[2]

images = getImages()

for image in images:
    if image != '.DS_Store':
        with ImageOps.grayscale(Image.open("./projetOCR/chiffres/"+image)) as img:
            unBlur(img, image)

cleanImages = getCleanImages()

for image in cleanImages:
    if image != '.DS_Store':
        with Image.open("./clean/"+image) as img:
            binImg = getBinaryImg(img)
            erosion(binImg, image)