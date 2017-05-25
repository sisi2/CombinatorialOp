from math import log


class C45:
    """
    Class implementing a C4.5 decision tree
    """

    def __init__(self, col=-1, value=None, left_child=None, right_child=None, label=None):
        self.class_feature_index = col
        self.value = value  # Feature value stored in the node
        self.left_child = left_child
        self.right_child = right_child
        self.node_label = label  # If leaf store class label, else None


def build_subset(data, target_column, target_value):
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


def occurences(rows):
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


def entropy(data):
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


def compute_gini_impurity(data):
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


def compute_variance(rows):
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


def build_decision_tree(rows, grow_strategy=entropy):
    """
    Build decision tree from data and gain function
    :param rows: dataset
    :param grow_strategy: information gain property
    :return: decision tree
    """

    if len(rows) == 0: return C45()
    currentScore = grow_strategy(rows)
    bestGain = 0.0
    bestAttribute = None
    bestSets = None
    columnCount = len(rows[0]) - 1  # last column is the result/target column
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


def classify(observations, tree):
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
        v = observations[tree.class_feature_index]
        branch = None

        if v == tree.value:
            branch = tree.left_child
        else:
            branch = tree.right_child
        return classify(observations, branch)


def toString(decision_tree, indent=''):
    """
    Output decision tree
    :param decision_tree: input dataset  
    :param indent: spacing
    :return: string formatted tree
    """
    if decision_tree.node_label is not None:  # leaf node
        return str(decision_tree.node_label)
    decision = 'Column %s: x == %s?' % (decision_tree.class_feature_index, decision_tree.node_label)
    left_child = indent + 'yes -> ' + toString(decision_tree.left_child, indent + '     ')
    right_child = indent + 'no  -> ' + toString(decision_tree.right_child, indent + '      ')
    return decision + '\n' + left_child + '\n' + right_child


def load_data(file):
    """
    Load data file (separated comma)
    :param file: 
    :return: 
    """

    fle = open(file, "r")
    reader = fle.readlines()
    return [[item for item in row.strip("\n").split(",")] for row in reader]


if __name__ == '__main__':
    trainingData = load_data('car.data')
    decisionTree = build_decision_tree(trainingData)
    print(toString(decisionTree))
    print("For: " + " ".join(i for i in ["low", "high", "2", "4", "med", "low"]) + " result should be unacc")
    print(classify(["low", "high", "2", "4", "med", "low"], decisionTree))  # should be unacc
    print("For : " + " ".join(i for i in ["vhigh", "med", "2", "4", "big", "high", "acc"]) + " result should be acc")
    print(classify(["vhigh", "med", "2", "4", "big", "high", "acc"], decisionTree))  # should be acc
