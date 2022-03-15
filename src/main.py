from collections import Counter
from RFUtils import *
from RFManipulation import *

TRAIN = "train/"
TEST = "test/"

def knn(training_set, training_labels, testing_set, testing_labels, k = 7):
    for idx, sample in enumerate(testing_set):
        distances = [distanceEuclidienne(sample[1], train_sample[1]) for train_sample in training_set]

        sorted_distances = [pair[0] for pair in sorted(enumerate(distances), key=lambda x:x[1])]

        candidates = [training_labels[idx] for idx in sorted_distances[:k]]
        counts = Counter(candidates)
        result_stats = ()
        for key in counts.keys():
            result_stats += ((key, str((counts[key] / k) * 100) + "%"),)

        result_stats = sorted(result_stats, key=lambda x:x[1], reverse=True)
        result = result_stats[0][0]
        search = testing_labels[idx]
        
        showMatrix(result, search)


trainImages = getImages(TRAIN)
trainLabels = getLabels(TRAIN)

testImages = getImages(TRAIN)
testLabels = getLabels(TRAIN)

knn(trainImages, trainLabels, testImages, testLabels)