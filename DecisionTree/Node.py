from sklearn import tree

tls = tree.DecisionTreeClassifier()

import math

l = ['x', 'x', 'y', 'y']


def m_log(i):
    return math.log(i, 2)


def csv_header(fle):
    labels, data, outcome = [], [], []
    with open(fle, 'r')as f:
        for idx, line in enumerate(f.readlines()):
            if idx == 0:
                labels = line.strip("\n").split(",")
            else:
                line = line.strip("\n").split(",")
                outcome.append(line[-1])
                data.append(line[:len(line) - 2])
    return labels, data, outcome


def rd_cvs(fle):
    ll = []
    with open(fle, 'r') as f:
        for i in f.readlines():
            ll.append(i.strip("\n").split(","))
    return ll


# labels, data, outcome = rd_cvs("./tennis.txt")
# print(labels)
# print(outcome)
dta = rd_cvs("./tennis.txt")


class Matrix:
    def __init__(self, data):
        self.header = data[0]  # labels
        self.data = data[1:]  # remove header
        self.class_labels = [i[-1] for i in self.data]
        # for i in self.data:
        #     print(i)
        # print("---")

    def get_header(self): return self.header

    def get_labels(self): return self.class_labels

    def get_row(self, idx): return self.data[:][idx]

    def get_col(self, idx): return self.data[idx]

    def __getitem__(self, item):
        return self.data[item[0]][item[1]]


# mat = Matrix(dta)
# print(mat.get_labels())
# print(mat.get_header())
# print(mat[(0, 2)])


def entropy_column(data):  # for feature
    """
    Calculate entropy of row (eg entropy for the parent node
    entropy = sum(p_i * log2(1/p_i))
    :param data: 
    :return:entropy for row 
    """
    ftrs = set(l)
    ldata = len(data)  # number of events
    entropy = 0
    for i in ftrs:
        entropy += (data.count(i) / ldata) * m_log(1.0 / (data.count(i) / ldata))
    print(ftrs)
    print(entropy)
    return -1


def entropy(s):
    res = 0
    val, counts = np.unique(s, return_counts=True)
    freqs = counts.astype('float') / len(s)
    for p in freqs:
        if p != 0.0:
            res -= p * np.log2(p)
    return res


def information_gain(data):
    return -1


class Node:
    def __init__(self, parent, subset, nodeid=None, label=None):
        self.node_id = nodeid
        self.children = []
        self.parent = parent
        self.subset = subset
        self.label = label


class Leaf(Node):
    def __int__(self, parent, subset, nodeid=None, label=None):
        Node.__init__(self, parent=parent, nodeid=nodeid)


class RootNode(Node):
    def __int__(self, parent, subset, label=None):
        Node.__init__(self, parent=parent, nodeid=nodeid)


class Dtree:
    def __init__(self, data):
        self.data = Matrix(data)
        self.root = None

    def train(self):
        if not self.data:
            return None
        else:
            self.root = RootNode(None, 1, self.data)

    def rc(self, node, data, labels, outcome):
        pass

    def test(self):
        pass


y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
x = [1, 1, 2, 3, 1, 2, 1, 3, 3]
import numpy as np


def pure(s):
    """
    Stopping condition all class variables are identical ie entropy = 0
    ie. 1 class 
    :param s: 
    :return: 
    """
    return len(set(s)) == 1


def gain(y, target_subset):
    res = entropy(y)

    # We partition x, according to attribute values x_i
    val, counts = np.unique(x, return_counts=True)
    freqs = counts.astype('float') / len(x)

    # We calculate a weighted average of the entropy
    for p, v in zip(freqs, val):
        res -= p * entropy(y[x == v])

    return res


import pprint


def recursive_split(x, y):
    # If there could be no split, just return the original set
    if pure(y) or len(y) == 0:
        return y

    # We get attribute that gives the highest mutual information
    inf_gain = np.array([gain(y, x_attr) for x_attr in x.T])
    selected_attr = np.argmax(info_gain)

    # If there's no gain at all, nothing has to be done, just return the original set
    if np.all(info_gain < 1e-6):
        return y

    # We split using the selected attribute
    sets = partition(x[:, selected_attr])

    res = {}
    for k, v in sets.items():
        y_subset = y.take(v, axis=0)
        x_subset = x.take(v, axis=0)

        res["x_%d = %d" % (selected_attr, k)] = recursive_split(x_subset, y_subset)

    return res


x1 = [0, 1, 1, 2, 2, 2]
x2 = [0, 0, 1, 1, 1, 0]
y = np.array([0, 0, 0, 1, 1, 0])
X = np.array([x1, x2]).T
pprint(recursive_split(X, y))
