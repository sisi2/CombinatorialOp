class Split:
    """
    Class implementing the splitting criterion
    """

    def __init__(self, name="Default impl"):
        self.name = name


class Splitster(Split):  # numerical
    def __init__(self):
        Split.__init__(self)

    def primary_split(self, index, value, data):
        """
        Test split
        :param index: what label to split on
        :param value: attr value 
        :param data: lists from input
        :return: 2 lists
        right -> values >= value at index
        """
        left, right = list(), list()
        for row in data:
            if row[index] < value:
                left.append(row)
            else:
                right.append(row)
        return left, right

    def split(self, data):
        from Impurity import Gini as Gini
        gini = Gini()
        class_values = list(set(row[-1] for row in data))
        b_index, b_value, b_score, b_groups = 999, 999, 999, None
        for index in range(len(data[0]) - 1):
            for row in data:
                groups = self.primary_split(index, row[index], data)
                gini_score = gini.index(groups, class_values)
                if gini_score < b_score:
                    b_index, b_value, b_score, b_groups = index, row[index], gini_score, groups

        return {'index': b_index, 'value': b_value, 'groups': b_groups}


if __name__ == '__main__':
    dataset = [[2.771244718, 1.784783929, 0],
               [1.728571309, 1.169761413, 0],
               [3.678319846, 2.81281357, 0],
               [3.961043357, 2.61995032, 0],
               [2.999208922, 2.209014212, 0],
               [7.497545867, 3.162953546, 1],
               [9.00220326, 3.339047188, 1],
               [7.444542326, 0.476683375, 1],
               [10.12493903, 3.234550982, 1],
               [6.642287351, 3.319983761, 1]]
    splitster = Splitster()
    split = splitster.split(dataset)
    print('Split: [X%d < %.3f]' % ((split['index'] + 1), split['value']))
