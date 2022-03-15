import numpy as np
from math import ceil
from RFUtils import getBinaryImg

IMG_WIDTH = IMG_HEIGHT = 50

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