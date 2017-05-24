from collections import Counter
from math import log


class Container:
    def __init__(self):
        self._params = None
        self.n = 0

    def load_from_file(self, file_name, nr_params):
        """Load training data set from a file in which every line        
        represent a instance and has values for every parameter 
        separated by a comma. Last value is the label: unacc,acc,good or vgood.
        """
        self.n = nr_params + 1
        self.data = [[] for _ in range(self.n)]  # empty list for each param + 1 one for label
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()
        self.nr = len(lines)
        for line in lines:
            line = line[:-1]
            tokens = line.split(',')
            for i in range(self.n):
                self.data[i].append(tokens[i])
        self.basic_statistics()

    def entropy(self, results, nr):
        "Compute entropy for nr"
        e = 0.0
        for r in results:
            r = float(r)
            frequency = r / nr
            e -= (frequency) * log(frequency, 2) if r != 0.0 else 0
        return e

    def basic_statistics(self):
        """
        Compute basic statistics
        :return: 
        """

        self.counter = Counter(self.data[-1])
        self.data_entropy = self.entropy(self.counter.values(), self.nr)

    def get_entropy(self, target_feature):
        """
        Compute entropy for target feature
        :param target_feature: 
        :return: 
        """
        counts = Counter(self.data[target_feature])  # count for each value of parameter
        entropy = self.data_entropy
        for k, v in counts.items():
            count_result = Counter([self.data[-1][i] for i in range(self.nr) if self.data[target_feature][i] == k])
            entropy -= (v / self.nr) * self.entropy(count_result.values(), v)
        return entropy

    def get_all_entropy(self):
        return [(i, self.get_entropy(i)) for i in range(self.n - 1)]

    def get_best_param(self):
        return sorted(self.get_all_entropy(), key=lambda e: e[1], reverse=True)[0][0]

    def is_final(self):
        """
        Compute stopping condition (set is pure or no more attrs)
        """
        return self.nr in self.counter.values() or self.n == 1

    def get_params(self):
        return self._params

    def set_params(self, val):
        self._params = val

    def _set_debug(self, p):
        self._params = p


def create_subset(data, target_column, target_value):
    """
    Create subset removing param = value
    :param data: 
    :param target_column: 
    :param target_value: 
    :return: 
    """
    data = Container()
    data.data = [[] for _ in range(data.n)]
    data.nr = 0
    for i in range(data.nr):
        if data.data[target_column][i] == target_value:
            data.nr += 1
            for j in range(data.n):
                data.data[j].append(data.data[j][i])
    del data.data[target_column]
    data.n = data.n - 1
    data.basic_statistics()

    if data.get_params():  # debug only
        data._params = [p for p in data.get_params()]
        del data.params[target_column]

    return data
