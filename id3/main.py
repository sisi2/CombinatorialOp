from Data import Data
from Tree import learn

d = Data()

d.load_from_file("car.data", 6)
tree = learn(d)
print(tree.debug(0))
print(tree.decide(["low", "high", "2", "4", "med", "low"]))
print(tree.decide(["low", "low", "2", "more", "small", "high"]))

d = Data()
d.load_from_file("tennis.csv", 4)
