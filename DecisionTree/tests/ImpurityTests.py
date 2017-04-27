import unittest

from DecisionTree.Impurity import Gini as Gini


class TestGini(unittest.TestCase):
    def test_perfect_split(self):
        gini = Gini()
        self.assertEqual(1.0, gini.index([[[1, 1], [1, 0]], [[1, 1], [1, 0]]], [0, 1]))

    def test_wors_split(self):
        gini = Gini()
        self.assertEqual(0.0, gini.index([[[1, 0], [1, 0]], [[1, 1], [1, 1]]], [0, 1]))


if __name__ == '__main__':
    unittest.main()
