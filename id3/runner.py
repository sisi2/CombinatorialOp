from Container import Container
from Tree import learn

d = Container()
d.load_data("car.data", 5)
tree = learn(d)
print(tree.decide(["low", "high", "2", "4", "med", "low"]))
print(tree.decide(["low", "low", "2", "more", "small", "high"]))

d = Container()
d.load_data("tennis.data", 4)
tree = learn(d)
print(tree.learn(["rainy", "mild", "high", "true"]))  # expected no
