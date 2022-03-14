from email.mime import image
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
from collections import Counter

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

    return binaryImage

def getImages(set):
    imagesNames = next(walk(set), (None, None, []))[2]
    results = []

    for image in imagesNames:
        if image != '.DS_Store':
            with ImageOps.grayscale(Image.open(set+image)) as img:
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

def getSubgrid(origin, size, grid):
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
            subarray = getSubgrid((i,j),eroder_size, bin_img)
            output[i,j] = int(erosion_is_ok(eroder, subarray))
                  
    #createImgFromBin(output, "retest")
    return output

def dilatation(img, dilater_size=3):
    #imagePixels = getBinaryImg(img)
    newImage = copy.deepcopy(img)

    for row, val in enumerate(img):
        for i, p in enumerate(img[row]):
            if p == 0:
                for x in range(-1,2,1):
                    for y in range(-1,2,1):
                        try:
                            if img[row+x][i+y] == 1:
                                newImage[row+x][i+y] = 0
                        except:
                            pass
    
    #createImgFromBin(newImage, 'res_dilatation', img.size[0], img.size[1])
    return newImage

def knn(training_set, training_labels, testing_set, testing_labels, k = 7):
    for idx, sample in enumerate(testing_set):
        distances = [distanceEuclidienne(sample[1], train_sample[1]) for train_sample in training_set]

        sorted_distances = [pair[0] for pair in sorted(enumerate(distances), key=lambda x:x[1])]

        candidates = [training_labels[idx] for idx in sorted_distances[:k]]
        counts = Counter(candidates)
        result_stats = ()
        for key in counts.keys():
            result_stats += ((key, str(round((counts[key] / k) * 100, 2)) + "%"),)
            

        result_stats = sorted(result_stats, key=lambda x:x[1], reverse=True)
        print(f"Le candidat {idx} était un {testing_labels[idx]} et on a trouvé {result_stats}")
            

def getStatsOfImage(img):
    """Récupère les informations (zoning, profils horizontal et vertical) d'une image qu'on utilisera pour la catégoriser

    Args:
        img (Image)

    Returns:
        tuple: Les informations de l'image
    """
    stats = tuple()
    stats += (zoning(img),)
    stats += (getProfilOfImage("V", img),)
    stats += (getProfilOfImage("H", img),)
    
    return stats

def getProfilOfImage(direction, img):
    """Détermine le profil de l'image

    Args:
        direction (str) : la direction du profil
        img (Image)

    Returns:
        tuple: le profil
    """
    resultat = ()
    imagePixels = np.array(list(img.getdata()))
    imagePixels = imagePixels.reshape(img.size[0], img.size[1])

    if direction == "H":
        for row in imagePixels:
            nbPerRow = 0
            for pixel in row:
                if pixel == 0:
                    nbPerRow += 1
            resultat += (nbPerRow,)
    elif direction == "V":
        for col in range(img.size[1]):
            nbPerCol = 0
            for line in range(img.size[0]):
                if imagePixels[line][col] == 0:
                    nbPerCol += 1
            resultat += (nbPerCol,)
    else:
        return ()

    return resultat

def zoning(ukwImg, grid_size = 4):
    
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
        if type(vecteur1[k]) == tuple and type(vecteur2[k]) == tuple:
            dist += distanceEuclidienne(vecteur1[k], vecteur2[k])
        else:
            dist += (vecteur2[k] - vecteur1[k])**2
        
    return dist
    
trainImages = getImages(TRAIN)
trainLabels = getLabels(TRAIN)

testImages = getImages(TEST)
testLabels = getLabels(TEST)

knn(trainImages, trainLabels, testImages, testLabels)

