from Container import Container
from Tree import learn
from random import shuffle
from c45 import *

from c45 import compute_gini_impurity


class CrossValidation:
    """ k-fold cross validation tool """

    def __init__(self, fileName, nbFeatures):
        self.k = 10
        self.pruneVal = 0.2
        self.nbFeatures = nbFeatures
        self.data = self.load_data(fileName)
        shuffle(self.data)  # shuffle data
        self.validation = 0

    def load_data(self, fileName):
        fle = open(fileName, "r")
        reader = fle.readlines()
        return [[item for item in row.strip("\n").split(",")] for row in reader]

    def validateID3(self):
        length = round(len(self.data) / self.k)
        validations = []  # percentage of correct predictions per testing data
        testing = []  # testing set
        training = []  # training set

        container = Container()

        # Give random column names:
        l = []
        for j in range(self.nbFeatures + 1):
            l.append(str(j))
        container._set_debug(l)
        container.set_n(self.nbFeatures + 1)

        for i in range(self.k):
            # PARTITION PHASE
            if i != self.k - 1:
                testing = self.data[i * length:(i + 1) * length]
                training = self.data[0:i * length] + self.data[(i + 1) * length::]
                container.set_nr(len(training))
            else:
                testing = self.data[i * length::]
                training = self.data[0:i * length]
                container.set_nr(len(training))

            # LEARN PHASE
            temp = [[] for _ in range(self.nbFeatures + 1)]
            for line in training:
                for i in range(self.nbFeatures + 1):
                    temp[i].append(line[i])

            container.set_data(temp)
            container.basic_statistics()
            tree = learn(container)

            # PREDICTION PHASE
            nbFalsePredictions = 0
            for test in testing:
                prediction = tree.decide(test[:-1])
                if prediction != test[-1]:
                    nbFalsePredictions += 1

            validations.append(1 - (nbFalsePredictions / len(testing)))

        # COMPUTE FINAL MEAN
        self.validation = sum(validations) / float(len(validations))
        return self.validation

    def validateC45(self):
        length = round(len(self.data) / self.k)
        validations = []  # percentage of correct predictions per testing data
        testing = []  # testing set
        training = []  # training set

        for i in range(self.k):
            print(i)
            # PARTITION PHASE
            if i != self.k - 1:
                testing = self.data[i * length:(i + 1) * length]
                training = self.data[0:i * length] + self.data[(i + 1) * length::]
            else:
                testing = self.data[i * length::]
                training = self.data[0:i * length]

            print("Len: " + str(len(testing)) + " and " + str(len(training)))
            # LEARN PHASE
            tree = build_decision_tree(training, grow_strategy=compute_gini_impurity)
            prune_tree(tree, self.pruneVal, debug=False)

            # PREDICTION PHASE
            nbFalsePredictions = 0
            for test in testing:
                prediction = classify(testing[0][:-1], tree)
                if prediction != test[-1]:
                    nbFalsePredictions += 1
                    print("False: ")
                    print(testing[0])

            validations.append(1 - (nbFalsePredictions / len(testing)))

        # COMPUTE FINAL MEAN
        self.validation = sum(validations) / float(len(validations))
        return self.validation

    def getData(self):
        return self.data

    def getValidation(self):
        return self.validation


if __name__ == '__main__':
    crossVal = CrossValidation("tennis.data", 4)
    print(crossVal.validateID3())
    print(crossVal.validateC45())
