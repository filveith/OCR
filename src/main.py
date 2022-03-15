

from collections import Counter
from RFUtils import *
from RFManipulation import *

ALL_CHIFFRES = "projetOCR/chiffres/"
TRAIN = "train/"
TEST = "test/"

def knn(training_set, training_labels, testing_set, testing_labels, k = 7):
    positive = 0
    negative = 0
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
        else:
            negative += 1

    reussite = round((positive / (negative + positive)) * 100, 2)
    print(f"Taux de réussite : {reussite}% avec {positive} positifs et {negative} négatifs")


trainImages = getImages(TRAIN)
trainLabels = getLabels(TRAIN)

testImages = getImages(TRAIN)
testLabels = getLabels(TRAIN)

knn(trainImages, trainLabels, testImages, testLabels)