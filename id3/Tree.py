from copy import deepcopy

from Container import create_subset_current_feature


class Node:
    def __init__(self):
        self.name = None
        self.param = None
        self.children = {}  # pair value : child

    def decide(self, instance):
        if self.children:  # is not a leaf
            i = deepcopy(instance)
            for k, v in self.children.items():
                if instance[self.param] == k:
                    break
            del i[self.param]
            return v.decide(i)
        else:
            raise Exception("Something bad really happened")



def learn(data):
    node = Node()
    if data.pure():
        node.children = None
        node.value = sorted(data.counter.items(), key=lambda c: [1], reverse=True)[0][0]
    else:
        node.param = data.get_best_param()
        node.name = data._params[node.param]
        for value in sorted(set(data.data[node.param])):
            node.children[value] = learn(create_subset_current_feature(data, node.param, value))
    return node
