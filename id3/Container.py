from collections import Counter
from math import log


class Container:
    def __init__(self):
        self._params = None
        self.data = None
        self.training_instances = None
        self.counter = None
        self.data_entropy = None
        self.features = 0

    def get_parameters(self):
        return self._params

    def set_parameters(self, val):
        self._params = val

    def load_data(self, file_name, nr_params):
        """
            Load training data as comma separated values
        """
        self.features = nr_params + 1
        self.data = [[] for _ in range(self.features)]  # empty list for each param + 1 one for label
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()
        self.training_instances = len(lines)
        for line in lines:
            tokens = line.strip("\n").split(',')
            for i in range(self.features):
                self.data[i].append(tokens[i])
        self.basic_statistics()

    @staticmethod
    def entropy(results, nr):
        """
         Compute entropy for target val
        """
        entropy = 0.0
        for r in results:
            frequency = float(r) / nr
            entropy -= frequency * log(frequency, 2) if float(r) != 0.0 else 0
        return entropy

    def basic_statistics(self):
        """
            Create class features statistics ( class feature : #no_observations)
            Create data entropy values ( every feature type aka column)
        """
        self.counter = Counter(self.data[-1])
        self.data_entropy = self.entropy(self.counter.values(), self.training_instances)

    def entropy_for_category(self, target_category):
        """
            Compute entropy for target category
            :param target_category:  take a wild guess
            :return:  entropy value
        """
        counts = Counter(self.data[target_category])  # count for each value of parameter
        entropy = self.data_entropy
        for k, v in counts.items():
            count_result = Counter(
                [self.data[-1][i] for i in range(self.training_instances) if self.data[target_category][i] == k])
            entropy -= (v / self.training_instances) * self.entropy(count_result.values(), v)
        return entropy

    def get_all_entropy(self):
        return [(i, self.entropy_for_category(i)) for i in range(self.features - 1)]

    def get_best_param(self):
        return sorted(self.get_all_entropy(), key=lambda e: e[1], reverse=True)[0][0]

    def pure(self):
        """
            Pure category or 0 remaining features
            :return: eval
        """
        return self.training_instances in self.counter.values() or self.features == 1

    def _set_debug(self, p):
        self._params = p

    def debug(self):
        s = ""
        for i in range(self.training_instances):

            for j in range(self.features):
                s += "\t" + self.data[j][i]
        print(s)

    def set_training_instances(self, val):
        self.training_instances = val

    def get_training_instances(self):
        """
        Getter for training instances
        :return: 
        """
        return self.training_instances

    def get_features(self):
        """
        Getter for feature counter
        :return: 
        """
        return self.features


def create_subset_current_feature(source_data, target_feat, target_value):
    """
      Create subset of source data containing only the target feature with the target value
      :param source_data: original data
      :param target_feat: feature predicate
      :param target_value:  feature value
      :return:  subset
      """
    data = Container()
    data.data = [[] for _ in range(source_data.get_features())]
    data.set_training_instances(0)
    for i in range(source_data.get_training_instances()):
        if source_data.data[target_feat][i] == target_value:
            data.set_training_instances(data.get_training_instances() + 1)
            for j in range(source_data.get_features()):
                data.data[j].append(source_data.data[j][i])
    del data.data[target_feat]
    data.features = source_data.get_features() - 1
    data.basic_statistics()

    if source_data._params:  # debug only
        data._params = [p for p in source_data._params]
        del data._params[target_feat]

    return data
