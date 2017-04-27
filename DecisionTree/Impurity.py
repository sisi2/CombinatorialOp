class Impurity:
    """
    Base class for impurity computation
    """

    def __init__(self, name):
        self.name = name


class Gini(Impurity):
    """
    Implementation of the Gini cost function
    best case : 0
    worst case : 1.0
    """

    def __init__(self):
        Impurity.__init__(self, "Gini")

    def index(self, groups, values):
        """
        Calculate the gini index
        :param groups: list of groups
        :param values: known class values
        :return: 
        """
        score = 0.0  # initial score
        for value in values:
            for group in groups:
                try:
                    proportion = [row[-1] for row in group].count(value) / float(len(group))
                    score += proportion * (1.0 - proportion)
                except ZeroDivisionError as error:
                    continue
        return score
