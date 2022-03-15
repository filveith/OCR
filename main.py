from email.mime import image
from itertools import chain
from math import ceil, floor, sqrt
from tokenize import String
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

def standardize(image, name):
    path = './clean/'+name+''
    image = image.resize((IMG_WIDTH, IMG_HEIGHT))
    imagePixels = list(image.getdata())
    newImage = []

    for p in imagePixels:
    
        if p >= 255/2:
            newImage.append(255)
        else:
            newImage.append(0)       

    img = Image.new(image.mode, image.size)
    img.putdata(newImage) #Unblurred verion of the image
    
    dilatedImg = dilatation(img)
    img = Image.new('1', dilatedImg.size) # Create a new image object because we save it in binary 
    img.putdata(list(dilatedImg.getdata())) #Unblurred + dilated image

    erodedImg = erosion(img)
    img.putdata(list(erodedImg.getdata())) #Unblurred + dilated + eroded image

    img.save(path)
    
    return img
    

def getBinaryImg(img):
    """Return the binary version of an image (Only black and white pixels)

    Args:
        img (Image)

    Returns:
        array: The binary image as a nested array [[0,1,1,...][1,1,1,...]] 
    """
    imagePixels = list(img.getdata())
    binaryImage = []
    width, height = img.size
    nb = 0
    row = []
    for p in imagePixels:
        nb += 1
        if p == 255 or p == 1:
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
    
    dilatedImg = Image.new('1', img.size)
    newImage_flat = [item for sublist in newImage for item in sublist]
    dilatedImg.putdata(newImage_flat)
    return dilatedImg

def erosion(img, eroder_size=3):
    """Erode an image

    Args:
        img (Image)
        eroder_size (int, optional): The size of the eroder. Defaults to 3.

    Returns:
        Image: an eroded version of the given image
    """
    imagePixels = getBinaryImg(img)
    newImage = copy.deepcopy(imagePixels)

    # print(newImage)

    for row, val in enumerate(imagePixels):
        for i, p in enumerate(imagePixels[row]):
            if p == 1:
                for x in range(-1,2,1):
                    for y in range(-1,2,1):
                        try:
                            if imagePixels[row+x][i+y] == 0:
                                newImage[row+x][i+y] = 1
                        except:
                            pass
    
    erodedImg = Image.new('1', img.size)
    newImage_flat = [item for sublist in newImage for item in sublist]
    erodedImg.putdata(newImage_flat)
    return erodedImg


def knn(training_set, training_labels, testing_set, testing_labels, k = 7):
    positive = 0
    negative = 0
    matrice_confusion_pos = {}
    matrice_confusion_neg = {}
    for idx, sample in enumerate(testing_set):
        distances = [distanceEuclidienne(sample[1], train_sample[1]) for train_sample in training_set]

        sorted_distances = [pair[0] for pair in sorted(enumerate(distances), key=lambda x:x[1])]

        candidates = [training_labels[idx] for idx in sorted_distances[:k]]
        counts = Counter(candidates)
        result_stats = ()
        for key in counts.keys():
            result_stats += ((key, str((counts[key] / k) * 100) + "%"),)

        result_stats = sorted(result_stats, key=lambda x:x[1], reverse=True)
        print(f"Le candidat {idx} était un {testing_labels[idx]} et on a trouvé {result_stats}")
        if testing_labels[idx] == result_stats[0][0]:
            positive += 1
            try:
                matrice_confusion_pos[str(testing_labels[idx])] = int(matrice_confusion_pos[str(testing_labels[idx])]) + 1
            except :
                matrice_confusion_pos[str(testing_labels[idx])] = 1
        else:
            negative += 1
            try:
                matrice_confusion_neg[str(testing_labels[idx])] = int(matrice_confusion_neg[str(testing_labels[idx])]) + 1
            except :
                matrice_confusion_neg[str(testing_labels[idx])] = 1

    print(matrice_confusion_pos, matrice_confusion_neg)
    reussite = round((positive / (negative + positive)) * 100, 2)
    print(f"Taux de réussite : {reussite}% avec {positive} positifs et {negative} négatifs")
    
    print('         +       -       0       1       2       3       4       5       6       7       8       9       ')
    print('---------------------------------------------------------------------------------------------------------')
    print('+|       {}      {}      {}      {}      {}      {}      {}      {}      {}      {}      {}      {}      ')
    print('-|')
    print('0|')
    print('1|')
    print('2|')
    print('3|')
    print('4|')
    print('5|')
    print('6|')
    print('7|')
    print('8|')
    print('9|')

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

            newZone = [binImg[X][Y] for X in range(startX, stopX) for Y in range(startY, stopY)]

            nbImg = nbImg + 1

            zones += (round(avgZone(newZone)),)

    return zones

def avgZone(zone):
    size = len(zone)
    sum = 0
    for p in zone:
        sum += int(not bool(p))

    avg = sum / size * 100
    
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

testImages = getImages(TRAIN)
testLabels = getLabels(TRAIN)

knn(trainImages, trainLabels, testImages, testLabels)