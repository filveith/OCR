from collections import Counter
from RFUtils import *
from RFManipulation import *

ALL_CHIFFRES = "projetOCR/chiffres/"
TRAIN = "train/"
TEST = "test/"

def knn(training_set, training_labels, testing_set, testing_labels, k = 7):
    positive = 0
    negative = 0
    matrice_confusion = {}
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
        result = result_stats[0][0]
        search = testing_labels[idx]
        if search == result:
            positive += 1

            try:
                (matrice_confusion[search])[result] = (matrice_confusion[search])[result] + 1
            except :
                try:
                    matrice_confusion[str(search)][result] = 1
                except:
                    matrice_confusion[str(search)] = {result:1}
                
        else:
            negative += 1
            try:
                (matrice_confusion[search])[result] = (matrice_confusion[search])[result]+1
            except :
                try:
                    matrice_confusion[str(search)][result] = 1
                except:
                    matrice_confusion[str(search)] = {result:1}
                
    reussite = round((positive / (negative + positive)) * 100, 2)
    print(f"\nTaux de réussite : {reussite}% avec {positive} positifs et {negative} négatifs \n")
    
    print('         +       -       0       1       2       3       4       5       6       7       8       9       ')
    print('---------------------------------------------------------------------------------------------------------')

    for item in matrice_confusion:     
        print(f'{item}|       {matrice_confusion[item]["+"] if "+" in matrice_confusion[item] else 0}       {matrice_confusion[item]["-"] if "-" in matrice_confusion[item] else 0}       {matrice_confusion[item]["0"] if "0" in matrice_confusion[item] else 0}       {matrice_confusion[item]["1"] if "1" in matrice_confusion[item] else 0}       {matrice_confusion[item]["2"] if "2" in matrice_confusion[item] else 0}       {matrice_confusion[item]["3"] if "3" in matrice_confusion[item] else 0}       {matrice_confusion[item]["4"] if "4" in matrice_confusion[item] else 0}       {matrice_confusion[item]["5"] if "5" in matrice_confusion[item] else 0}       {matrice_confusion[item]["6"] if "6" in matrice_confusion[item] else 0}       {matrice_confusion[item]["7"] if "7" in matrice_confusion[item] else 0}       {matrice_confusion[item]["8"] if "8" in matrice_confusion[item] else 0}       {matrice_confusion[item]["9"] if "9" in matrice_confusion[item] else 0}       ')


trainImages = getImages(TRAIN)
trainLabels = getLabels(TRAIN)

testImages = getImages(TRAIN)
testLabels = getLabels(TRAIN)

knn(trainImages, trainLabels, testImages, testLabels)