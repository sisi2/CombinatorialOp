from math import log


class C45:
    """
    Class implementing a C4.5 decision tree
    """

    def __init__(self, col=-1, value=None, left_child=None, right_child=None, label=None):
        self._class_feature_index = col
        self._value = value  # Feature value stored in the node
        self._left_child = left_child
        self._right_child = right_child
        self._node_label = label  # If leaf store class label, else None

    @property
    def class_feature_index(self):
        return self._class_feature_index

    @class_feature_index.setter
    def class_feature_index(self, val):
        self._class_feature_index = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def left_child(self):
        return self._left_child

    @left_child.setter
    def left_child(self, val):
        self._left_child = val

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, val):
        self._right_child = val

    @property
    def node_label(self):
        return self._node_label

    @node_label.setter
    def node_label(self, val):
        self._node_label = val


def build_subset(data: [[]], target_column: [], target_value: str):
    """
    Build subset from daset, removing target_column with target_value ie class label
    :param data: input dataset
    :param target_column: 
    :param target_value: 
    :return: 
    """
    splittingFunction = None
    subset1, subset2 = [], []
    for row in data:
        if row[target_column] == target_value:
            subset1.append(row)
        else:
            subset2.append(row)
    return subset1, subset2


def occurences(rows: [[]]):
    """
    Compute occurences for class feature
    :param rows: row for wich to compute occurences
    :return: dictionary {feature:number_of_occurences}
    """
    results = {}
    lst = [row[-1] for row in rows]
    vars = set(lst)
    for i in vars:
        results[i] = lst.count(i)
    return results


def entropy(data: [[]]):
    """
    Compute the entropy of the dataset
    :param data: dataset
    :return: entropy for the dataset
    """
    occurence = occurences(data)
    entropy = 0.0
    for r in occurence:
        p = float(occurence[r]) / len(data)
        entropy -= p * log(p, 2)
    return entropy


def compute_gini_impurity(data: [[]]):
    """
    Compute gini impurity
    :param data: input dataset 
    :return: gini impurity
    """
    total = len(data)
    counts = occurences(data)
    imp = 0.0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        for k2 in counts:
            if k1 == k2: continue
            p2 = float(counts[k2]) / total
            imp += p1 * p2
    return imp


def compute_variance(rows: [[]]):
    """
    Compute the variance of the dataset
    :param rows: input dataset  
    :return: 
    """
    if len(rows) == 0:
        return 0
    data = [float(row[len(row) - 1]) for row in rows]
    mean = sum(data) / len(data)
    variance = sum([(d - mean) ** 2 for d in data]) / len(data)
    return variance


def build_decision_tree(rows: [[]], grow_strategy=entropy):
    """
    Build decision tree from data and gain function
    :param rows: dataset
    :param grow_strategy: information gain property
    :return: decision tree
    """

    if len(rows) == 0: return C45()  # empty tree
    currentScore = grow_strategy(rows)
    bestGain = 0.0
    bestAttribute, bestSets = None, None
    columnCount = len(rows[0]) - 1  # only data without class features
    for col in range(0, columnCount):
        columnValues = [row[col] for row in rows]
        for value in columnValues:
            (set1, set2) = build_subset(rows, col, value)
            p = float(len(set1)) / len(rows)
            gain = currentScore - p * grow_strategy(set1) - (1 - p) * grow_strategy(set2)
            if gain > bestGain and len(set1) > 0 and len(set2) > 0:
                bestGain = gain
                bestAttribute = (col, value)
                bestSets = (set1, set2)

    if bestGain > 0:
        trueBranch = build_decision_tree(bestSets[0])
        falseBranch = build_decision_tree(bestSets[1])
        return C45(col=bestAttribute[0], value=bestAttribute[1], left_child=trueBranch,
                   right_child=falseBranch)
    else:
        return C45(label=occurences(rows))


def classify(observations, tree: C45):
    """
    Classify data
    :param observations: 
    :param tree: 
    :return: 
    """
    # TODO missing data
    if tree.node_label is not None:  # leaf
        return set(tree.node_label.keys())
    else:
        values = observations[tree.class_feature_index]
        branch = None
        if values == tree.value:
            branch = tree.left_child
        else:
            branch = tree.right_child
        return classify(observations, branch)


def prune_tree(tree: C45, minGain: float, valuation_function=entropy, debug=False) -> None:
    """
    Recursively prune each subtree using 
    :param tree: target tree
    :param minGain: sentinel
    :param valuation_function: what function to use for evaluation
    :param debug: print status to terminal
    :return: 
    """
    if tree.left_child.node_label is None:  # internal node
        prune_tree(tree.left_child, minGain, valuation_function, debug)
    if tree.right_child.node_label is None:  # internal node
        prune_tree(tree.right_child, minGain, valuation_function, debug)
    if tree.left_child.node_label is not None and tree.right_child.node_label is not None:  # both nodes are leaves
        lchild, rchild = [], []
        for values, columns in tree.left_child.node_label.items(): lchild += [[values]] * columns
        for values, columns in tree.right_child.node_label.items(): rchild += [[values]] * columns
        p = float(len(lchild)) / len(lchild + rchild)
        delta = valuation_function(lchild + rchild) - p * valuation_function(lchild) - (1 - p) * valuation_function(
            rchild)
        if delta < minGain:  # border between pruning
            if debug: print('The branch was pruned with gain = {0}'.format(delta))
            tree.left_child, tree.right_child = None, None
            tree.results = occurences(lchild + rchild)


def print_decision_tree(decision_tree: C45, indent=''):
    """
    Output decision tree
    :param decision_tree: input dataset  
    :param indent: spacing
    :return: string formatted tree
    """
    if decision_tree.node_label is not None:  # leaf node
        return str(decision_tree.node_label)
    decision = 'Column %s: x == %s?' % (decision_tree.class_feature_index, decision_tree.node_label)
    left_child = indent + 'yes -> ' + print_decision_tree(decision_tree.left_child, indent + '     ')
    right_child = indent + 'no  -> ' + print_decision_tree(decision_tree.right_child, indent + '      ')
    return decision + '\n' + left_child + '\n' + right_child


def load_data(file: str):
    """
    Load data file (separated comma)
    :param file: location
    :return: matrix containing the data
    """

    fle = open(file, "r")
    reader = fle.readlines()
    return [[item for item in row.strip("\n").split(",")] for row in reader]


def save_tree(file_name: str, tree: C45):
    """
    Save decision tree to file
    :param file_name: name of the file where to save
    :param tree: target tree to dump
    """
    with open(file_name, "wb") as fle:
        import pickle
        pickle.dump(tree, fle)
        print("Tree saved in \"{0}\"".format(file_name))


def load_tree(file_name: str):
    """
    Load a tree model from file
    :param file_name: name of the file
    :return: 
    """
    tree = None
    with open(file_name, "rb") as fle:
        import pickle
        tree = pickle.load(fle)
    return tree


def run(input_file="car.data"): pass


def get_random_test_samples(file="car.data"):
    f = open(file, "r")
    ll = []
    for lines in f.readlines():
        lines = lines.strip("\n").split(",")
        ll.append((lines[:-1], lines[-1]))
    return ll


def test1():
    trainingData = load_data('car.data')
    decisionTree = build_decision_tree(trainingData)
    print(print_decision_tree(decisionTree))
    print("##################################PRUNED######################################################")
    prune_tree(decisionTree, 0.5, debug=True)
    print(print_decision_tree(decisionTree))
    print("################################################################################################")
    print("For: " + " ".join(i for i in ["low", "high", "2", "4", "med", "low"]) + " result should be unacc")
    print(classify(["low", "high", "2", "4", "med", "low"], decisionTree))  # should be unacc
    # print("For : " + " ".join(i for i in ["vhigh", "med", "2", "4", "big", "high", "acc"]) + " result should be acc")
    # print(classify(["vhigh", "med", "2", "4", "big", "high", "acc"], decisionTree))  # should be acc


def build_save_tree():
    trainingData = load_data('car.data')
    decisionTree = build_decision_tree(trainingData)
    save_tree("cars.tree", decisionTree)


def load_tree_and_classify():
    tree = load_tree("cars.tree")
    prune_tree(tree, 0.5, debug=True)
    print(classify(["low", "high", "2", "4", "med", "low"], tree))  # should be unacc


def load_tree_and_classify2():
    tree = load_tree("cars.tree")
    prune_tree(tree, 0.5, debug=True)
    import random
    data = get_random_test_samples()
    ll = []
    for ftrs in range(random.randint(5, 10)):  # between 5 and 10 samples
        j = random.randint(0, len(data))
        ll.append(data[j])
    for i in ll:
        print(classify(i[0], tree), " should get ", i[1])
        # print(classify(["low", "high", "2", "4", "med", "low"], tree))  # should be unacc


if __name__ == '__main__':
    # build_save_tree()
    load_tree_and_classify2()
