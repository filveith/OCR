from PIL import Image, ImageOps
from os import walk
from RFManipulation import standardize
from RFExtraction import *

IMG_WIDTH = IMG_HEIGHT = 50

def getBinaryImg(img):
    """Return the binary version of an image (Only black and white pixels)

    Args:
        img (Image)

    Returns:
        array: The binary image as a nested array [[0,1,1,...][1,1,1,...]] 
    """
    imagePixels = list(img.getdata())
    binaryImage = []
    width = img.size[0]
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
                img = standardize(img)
                results.append((img, getStatsOfImage(img)))
    return results

def getLabels(set):
    imagesNames = next(walk(set), (None, None, []))[2]
    results = []
    
    for name in imagesNames:
        results.append(name[0])
    return results


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