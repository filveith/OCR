from itertools import chain
from math import floor, sqrt
import numpy as np
from re import A
from PIL import Image
from os import walk

ALL_CHIFFRES = "projetOCR/chiffres/"
TRAIN = "train/"
TEST = "test/"


def standardize(img, name):
    path = './clean/'+name+''
    img = img.resize((50, 50))
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
            with Image.open(set+image) as img:
                results.append((img, getStatsOfImage(img)))
    return results

def getLabels(set):
    imagesNames = next(walk(set), (None, None, []))[2]
    results = []
    
    for name in imagesNames:
        results.append(name[0])
    return results

def createImgFromBin(img_2d_list, filename):
    flat = list(img_2d_list)
    width, height = img_2d_list.size
    # Check if list is nested or not (if yes we flaten it)
    if any(isinstance(i, list) for i in img_2d_list): 
        flat = list(chain.from_iterable(img_2d_list))
        width = len(img_2d_list[0])
        height = len(img_2d_list)

    im2 = Image.new('1', (height, width))
    im2.putdata(flat)
    im2.save('./clean/'+filename)

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

# def knn(training_set, training_labels, testing_set, k = 5):
#     predictions = []
#     for idx, sample in enumerate(testing_set):
#         distances = 
            

def getStatsOfImage(img):
    stats = []
    stats.append(zoning(img))
    # ajouter autres stats
    
    return stats

def zoning(ukwImg, nb_zones = 4):
    
    binImg = getBinaryImg(ukwImg)
    
    # for i in range(nb_zones):
        
    zone1 = [binImg[x][y] for x in range(0,25) for y in range(0,25)]
    zone2 = [binImg[y][x] for x in range(25,50) for y in range(0,25)]
    zone3 = [binImg[y][x] for x in range(0,25) for y in range(25,50)]
    zone4 = [binImg[y][x] for x in range(25,50) for y in range(25,50)]

    avgZone(zone1)
    avgZone(zone2)
    avgZone(zone3)
    avgZone(zone4)

    return 0

def avgZone(zone):
    size = len(zone)
    sum = 0
    for p in zone:
        sum += int(not bool(p))

    avg = sum / size * 100
    print(avg)
    
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

allImages = getImages(ALL_CHIFFRES)

trainImages = getImages(TRAIN)
trainLabels = getLabels(TRAIN)

testImages = getImages(TEST)
testLabels = getLabels(TEST)
