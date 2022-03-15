from collections import Counter
from turtle import position
from RFUtils import *
from RFManipulation import *

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
        
        # Print knn infos
        # print(f"Le candidat {idx} était un {testing_labels[idx]} et on a trouvé {result_stats}")

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

    showMatrix(matrice_confusion, positive, negative)


trainImages = getImages(TRAIN)
trainLabels = getLabels(TRAIN)

testImages = getImages(TEST)
testLabels = getLabels(TEST)

knn(trainImages, trainLabels, testImages, testLabels)