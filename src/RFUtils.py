from PIL import Image, ImageOps
from os import walk
from RFManipulation import *
from RFExtraction import *

IMG_WIDTH = IMG_HEIGHT = 50

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

def showMatrix(results, search):
    positive = 0
    negative = 0
    matrice_confusion = {}
    if search == results:
        positive += 1

        try:
            (matrice_confusion[search])[results] = (matrice_confusion[search])[results] + 1
        except :
            try:
                matrice_confusion[str(search)][results] = 1
            except:
                matrice_confusion[str(search)] = {results:1}
            
    else:
        negative += 1
        try:
            (matrice_confusion[search])[results] = (matrice_confusion[search])[results]+1
        except :
            try:
                matrice_confusion[str(search)][results] = 1
            except:
                matrice_confusion[str(search)] = {results:1}
                
    reussite = round((positive / (negative + positive)) * 100, 2)
    print(f"\nTaux de réussite : {reussite}% avec {positive} positifs et {negative} négatifs \n")
    
    print('         +       -       0       1       2       3       4       5       6       7       8       9       ')
    print('---------------------------------------------------------------------------------------------------------')

    for item in matrice_confusion:     
        print(f'{item}|       {matrice_confusion[item]["+"] if "+" in matrice_confusion[item] else 0}       {matrice_confusion[item]["-"] if "-" in matrice_confusion[item] else 0}       {matrice_confusion[item]["0"] if "0" in matrice_confusion[item] else 0}       {matrice_confusion[item]["1"] if "1" in matrice_confusion[item] else 0}       {matrice_confusion[item]["2"] if "2" in matrice_confusion[item] else 0}       {matrice_confusion[item]["3"] if "3" in matrice_confusion[item] else 0}       {matrice_confusion[item]["4"] if "4" in matrice_confusion[item] else 0}       {matrice_confusion[item]["5"] if "5" in matrice_confusion[item] else 0}       {matrice_confusion[item]["6"] if "6" in matrice_confusion[item] else 0}       {matrice_confusion[item]["7"] if "7" in matrice_confusion[item] else 0}       {matrice_confusion[item]["8"] if "8" in matrice_confusion[item] else 0}       {matrice_confusion[item]["9"] if "9" in matrice_confusion[item] else 0}       ')