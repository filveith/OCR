from itertools import chain
from math import ceil, floor, sqrt
from tokenize import String
from tracemalloc import stop
from turtle import width
import numpy as np
from re import A
import copy
from PIL import Image, ImageOps
from os import walk

ALL_CHIFFRES = "projetOCR/chiffres/"
TRAIN = "train/"
TEST = "test/"
IMG_WIDTH = IMG_HEIGHT = 50

def standardize(img, name):
    path = './clean/'+name+''
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    imagePixels = list(img.getdata())
    newImage = []
    
    for p in imagePixels:
        if p >= 255/2:
            newImage.append(255)
        else:
            newImage.append(0)       

    im2 = Image.new(img.mode, img.size)
    im2.putdata(newImage)
    im2.save(path)
    return im2
    

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

def getImages(set):
    imagesNames = next(walk(set), (None, None, []))[2]
    results = []

    for image in imagesNames:
        if image != '.DS_Store':
            with ImageOps.grayscale(Image.open(set+image)) as img:
                print(image)
                img = standardize(img, image)
                results.append((img, getStatsOfImage(img)))
    return results

def getLabels(set):
    imagesNames = next(walk(set), (None, None, []))[2]
    results = []
    
    for name in imagesNames:
        results.append(name[0])
    return results

def createImgFromBin(img_2d_list, filename, width = IMG_WIDTH, height = IMG_HEIGHT):
    flat = list(img_2d_list)
    # Check if list is nested or not (if yes we flaten it)
    if any(isinstance(i, list) for i in img_2d_list): 
        flat = list(chain.from_iterable(img_2d_list))
        width = len(img_2d_list[0])
        height = len(img_2d_list)

    img = Image.new('1', (width, height))
    img.putdata(flat)
    img.save('./clean/'+filename)

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
            #Fix this getSubGrid(bin_img)
            subarray = getsubgrid((i,j),eroder_size, bin_img)
            output[i,j] = int(erosion_is_ok(eroder, subarray))
                  
    createImgFromBin(output, "retest")

def dilatation(img, dilater_size=3):
    imagePixels = getBinaryImg(img)
    newImage = copy.deepcopy(imagePixels)

    for row, val in enumerate(imagePixels):
        for i, p in enumerate(imagePixels[row]):
            if p == 0:
                for x in range(-1,2,1):
                    for y in range(-1,2,1):
                        try:
                            if imagePixels[row+x][i+y] == 1:
                                newImage[row+x][i+y] = 0
                        except:
                            pass
    
    createImgFromBin(newImage, 'res_dilatation', img.size[0], img.size[1])
    return newImage

# def knn(training_set, training_labels, testing_set, k = 5):
#     predictions = []
#     for idx, sample in enumerate(testing_set):
#         distances = 
            

def getStatsOfImage(img):
    stats = []
    stats.append(zoning(img))
    # ajouter autres stats
    
    return stats

def isPrime(num):
    if num > 1:
        for i in range(2, num//2):
            if (num % i) == 0:
                return False
            else:
                return True
    else:
        return False

def zoning(ukwImg, grid_size = 3):
    
    binImg = getBinaryImg(ukwImg)
    
    zones = ()

    newZone = []
    nbImg = 1

    for x in range(grid_size):
        for y in range(grid_size):
            
            startX = x*ceil(IMG_WIDTH/grid_size)
            stopX = ceil(IMG_WIDTH/grid_size) + startX

            startY = y*ceil(IMG_WIDTH/grid_size)
            stopY = ceil(IMG_WIDTH/grid_size) + startY

            if stopX > IMG_WIDTH : stopX = IMG_WIDTH
            if stopY > IMG_HEIGHT : stopY = IMG_HEIGHT

            width = stopX-startX
            height = stopY-startY

            newZone = [binImg[X][Y] for X in range(startX, stopX) for Y in range(startY, stopY)]

            # print(startX, stopX, startY, stopY, "   ",  round(avgZone(newZone)),"%    img size : ", height, width)

            createImgFromBin(newZone, 'zone'+str(nbImg)+'.png', height, width)

            nbImg = nbImg + 1

            zones += (round(avgZone(newZone)),)

    # print(zones)
    
    return zones

def avgZone(zone):
    size = len(zone)
    sum = 0
    for p in zone:
        sum += int(not bool(p))

    avg = sum / size * 100
    # print(avg)
    
    return avg

def distanceEuclidienne(vecteur1, vecteur2):
    """Calcule la distance euclidienne entre deux vecteurs

    Args:
        vecteur1 (tuple)
        vecteur2 (tuple)

    Returns:
        int: la distance
    """
    maxLen = max(len(vecteur1), len(vecteur2))
    
    dist = 0
    
    for i in range(maxLen - len(vecteur1)):
        vecteur1 = vecteur1 + (0,)
        
    for j in range(maxLen - len(vecteur2)):
        vecteur2 = vecteur2 + (0,)
    
    for k in range(maxLen):
        dist += (vecteur2[k] - vecteur1[k])**2
        
    return dist
    

a = [[0, 0, 1, 1, 1, 0, 0],
     [0, 0, 1, 1, 1, 0, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0]]

test = [i for i in range(10) for j in range(2)]

# allImages = getImages(ALL_CHIFFRES)

# trainImages = getImages(TRAIN)
# trainLabels = getLabels(TRAIN)

# testImages = getImages(TEST)
# testLabels = getLabels(TEST)

zoning(Image.open('clean/1_1.png'))