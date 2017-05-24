from utils import compute_gain, get_subtables


def c45(table, result):
    """
    
    :param table:  data
    :param result: class features 
    :return: 
    """
    col = max([(k, compute_gain(table, k, result)) for k in table.keys() if k != result],
              key=lambda x: x[1])[0]
    tree = []
    for subt in get_subtables(table, col):
        v = subt[col][0]
        if pure_mono(subt[result]):
            tree.append(['%s=%s' % (col, v),
                         '%s=%s' % (result, subt[result][0])])
        else:
            del subt[col]
            tree.append(['%s=%s' % (col, v)] + c45(subt, result))
    return tree


def __tree_to_rules(tree, rule=''):
    """
    Convert tree to rules
    :param tree:  target tree
    :param rule:  
    :return: 
    """
    rules = []
    for node in tree:
        if isinstance(node, basestring):
            rule += node + ','
        else:
            rules += __tree_to_rules(node, rule)
    if rules:
        return rules
    return [rule]


def validate_table(table):
    assert isinstance(table, dict)
    for k, v in table.items():
        assert k
        assert isinstance(k, basestring)
        assert len(v) == len(table.values()[0])
        for i in v: assert i


def test(table): pass


data = {
    "arg1": ["left", "left", "right", "right"],
    "arg2": ["down", "up", "down", "down"],
    "arg3": ["no", "yes", "yes", "no"]
}

res = {"result": ["yes", "no", "yes", "no"]}
c45(data, res)
