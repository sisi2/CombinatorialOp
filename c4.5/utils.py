import math
from collections import OrderedDict


def freq(table, target_column, target_feature):
    """
    Compute frequency of value v in column v of table
    :param table: dataset
    :param target_column: target column
    :param target_feature:  target feature
    :return: 
    """
    return table[target_column].count(target_feature)


def info(data, target_column):
    """
    Compute entropy of the table for target_column
    :param data: 
    :param target_column: 
    :return: 
    """
    s = 0  # sum
    for v in remove_duplicates(data[target_column]):
        p = freq(data, target_column, v) / float(len(data[target_column]))
        s += p * math.log(p, 2)
    return -s


def compute_entropy_of_subtable(data, col, res_col):
    """
    Compute entropy of the table splir by col
    :param data: 
    :param col: 
    :param res_col: 
    :return: 
    """
    s = 0  # sum
    for subt in get_subtables(data, col):
        s += (float(len(subt[col])) / len(data[col])) * info(subt, res_col)
    return s


def compute_gain(data, x, result_column):
    """
    Find splitting criterion
    :param data: 
    :param x: 
    :param result_column: 
    :return: 
    """
    return info(data, result_column) - compute_entropy_of_subtable(data, x, result_column)


def remove_duplicates(li):
    """"
    Remove duplicates from list
    """
    return list(OrderedDict.fromkeys(li))


def pure(t):
    """ Returns True if all values of _t_ are equal
        and False otherwise.
    """
    for i in t:
        if i != t[0]:
            return False
    return True


def get_indexes(data, target_column, target_value):
    """
    Retrieve indexes of target_value in target_column
    :param data:  dataset
    :param target_column: object column 
    :param target_value:  
    :return: 
    """
    li = []
    start = 0
    for row in data[target_column]:
        if row == target_value:
            index = data[target_column].index(row, start)
            li.append(index)
            start = index + 1
    return li


def get_values(t, col, indexes):
    """ Returns values of _indexes_ in column _col_
        of the table _t_.
    """
    return [t[col][i] for i in range(len(t[col])) if i in indexes]


def create_subset(original_data, target_features):
    """
    Create subset of data with values ind
    :param original_data: 
    :param target_features: 
    :return: subset of original dataset
    """
    return {k: [v[i] for i in range(len(v)) if i in target_features] for k, v in original_data.items()}


def preety_list(tree, tab=''):
    """ Prints list of nested lists in
        hierarchical form.
    """
    print('%s[' % tab)
    for node in tree:
        if isinstance(node, basestring):
            print('%s  %s' % (tab, node))
        else:
            preety_list(node, tab + '  ')
    print('%s]' % tab)


def formalize_rules(list_rules):
    """ Gives an list of rules where
        facts are separeted by coma.
        Returns string with rules in
        convinient form (such as
        'If' and 'Then' words, etc.).
    """
    text = ''
    for r in list_rules:
        t = [i for i in r.split(',') if i]
        text += 'If %s,\n' % t[0]
        for i in t[1:-1]:
            text += '   %s,\n' % i
        text += 'Then: %s.\n' % t[-1]
    return text


def get_subtables(data, target_columns):
    """
    Create subtables set from original data
    :param data:  original data
    :param target_columns: 
    :return: 
    """
    return [create_subset(data, get_indexes(data, target_columns, v)) for v in remove_duplicates(data[target_columns])]
