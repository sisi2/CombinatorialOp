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


def build_decision_tree(input_dataset: [[]], expand_strategy=entropy):
    """
    Build decision tree from data and gain function
    :param input_dataset: dataset
    :param expand_strategy: information gain property
    :return: decision tree
    """

    if len(input_dataset) == 0: return C45()  # empty tree
    current_score = expand_strategy(input_dataset)
    max_gain = 0.0
    best_split_attribute, bestSets = None, None
    for col in range(len(input_dataset[0]) - 1):
        column_values = [row[col] for row in input_dataset]
        for value in column_values:
            (set1, set2) = build_subset(input_dataset, col, value)
            p = float(len(set1)) / len(input_dataset)
            gain = current_score - p * expand_strategy(set1) - (1 - p) * expand_strategy(set2)
            if gain > max_gain and len(set1) > 0 and len(set2) > 0:
                max_gain = gain
                best_split_attribute = (col, value)
                bestSets = (set1, set2)

    if max_gain > 0:
        left_child = build_decision_tree(bestSets[0], expand_strategy)
        right_child = build_decision_tree(bestSets[1], expand_strategy)
        return C45(col=best_split_attribute[0], value=best_split_attribute[1], left_child=left_child,
                   right_child=right_child)
    else:
        return C45(label=occurences(input_dataset))


missing = False


def classify(input_set, tree: C45):
    """
    Classify data
    :param input_set: 
    :param tree: 
    :return: 
    """
    global missing
    if missing:
        return classify_missing(input_set, tree)
    else:
        return classify_not_missing(input_set, tree)


def classify_not_missing(input_set, tree):
    if tree.node_label is not None:  # leaf node
        out = ""
        for i in set(tree.node_label.keys()):
            out = i
        return out
    else:
        values = input_set[tree.class_feature_index]
        branch = None

        if numeric(values):  # handle numerical values
            if float(tree.value) <= float(values):
                branch = tree.left_child
            else:
                branch = tree.right_child

        else:

            if values == tree.value:
                branch = tree.left_child
            else:
                branch = tree.right_child
        return classify(input_set, branch)


def numeric(value) -> bool:
    """
    Determine current value is numeric or not
    :param value:  target  value
    :return: bool is numeric yes/no -> true/false
    """
    try:
        int(value)
        return True
    except:
        try:
            float(value)
            return True
        except:
            return False


def classify_missing(input_set, tree: C45):
    """
    Classification with missing data
    :param input_set: 
    :param tree: 
    :return: 
    """
    if tree.node_label is not None:  # leaf
        return tree.results
    else:
        values = input_set[tree.col]
        if values == "?":  # our dataset
            left_row = classify_missing(input_set, tree.left_child)
            right_row = classify_missing(input_set, tree.right_child)
            left_child_values = sum(left_row.values())
            right_child_values = sum(right_row.values())
            left_child_weights = float(left_child_values) / (left_child_values + right_child_values)
            right_child_wheights = float(right_child_values) / (left_child_values + right_child_values)
            out = collections.defaultdict(int)  # initialize empty dictionary
            for key, values in left_row.items(): out[key] += values * left_child_weights
            for key, values in right_row.items(): out[key] += values * right_child_wheights
            return dict(out)
        else:
            branch = None
            if numeric(values):
                if tree.value <= values:
                    branch = tree.left_child
                else:
                    branch = tree.right_child
            else:
                if values == tree.value:
                    branch = tree.left_child
                else:
                    branch = tree.falseBranch
        return classify_missing(input_set, branch)


def prune_tree(tree: C45, confidence: float, debug=False) -> None:
    """
    Recursively prune each subtree using 
    :param tree: target tree
    :param confidence: confidence in the subtree
    :param valuation_function: what function to use for evaluation
    :param debug: print status to terminal
    :return: 
    """
    if tree.left_child.node_label is None:  # internal node
        prune_tree(tree.left_child, confidence, valuation_function, debug)
    if tree.right_child.node_label is None:  # internal node
        prune_tree(tree.right_child, confidence, valuation_function, debug)
    if tree.left_child.node_label is not None and tree.right_child.node_label is not None:  # both nodes are leaves
        lchild, rchild = [], []
        for values, columns in tree.left_child.node_label.items(): lchild += [[values]] * columns
        for values, columns in tree.right_child.node_label.items(): rchild += [[values]] * columns
        p = float(len(lchild)) / len(lchild + rchild)
        delta = entropy(lchild + rchild) - p * entropy(lchild) - (1 - p) * entropy(
            rchild)
        if delta < confidence:  # border between pruning
            if debug: print('The branch was pruned with gain = {0}'.format(delta))
            tree.left_child, tree.right_child = None, None
            tree.results = occurences(lchild + rchild)


def print_decision_tree(tree: C45, indent=" "):
    """
    Output decision tree
    :param tree: input dataset  
    :param indent: spacing for depth
    :return: string formatted tree
    """
    if tree.node_label is not None:  # leaf node
        return str(tree.node_label)
    else:
        decision = decision_node_string(tree)
        left_child = child_string(indent, tree.left_child, "yes : ")
        right_child = child_string(indent, tree.right_child, "no : ")
        return decision + '\n' + left_child + '\n' + right_child


def child_string(indent: str, child, val):
    """
    Child string representation helper method
    :param indent: spacing
    :param child: take a wild guess
    :param val: yes/no
    :return: STRING
    """
    return indent + val + print_decision_tree(child, indent + "    ")


def decision_node_string(tree):
    if numeric(tree.value.strip()):
        decision = "Column {0}:  ** {1} <= x **".format(tree.class_feature_index, tree.value)
    else:
        decision = "Column {0}: ** x == {1} ** ".format(tree.class_feature_index, tree.value)
    return decision


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
    print("##########################################PRUNED################################################")
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
    print(print_decision_tree(tree))
    import random
    data = get_random_test_samples()
    ll = []
    for ftrs in range(random.randint(5, 10)):  # between 5 and 10 samples
        j = random.randint(0, len(data))
        ll.append(data[j])
    for i in ll:
        print("Test data: ", str(i[0]))
        print("Output of the test: \"", classify(i[0], tree), "\"", " should get ", "\"", i[1], "\"")
        # print(classify(["low", "high", "2", "4", "med", "low"], tree))  # should be unacc


if __name__ == '__main__':
    build_save_tree()
    load_tree_and_classify2()
