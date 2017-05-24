from Container import Container
from Tree import learn

d = Container()

d.load_from_file("car.data", 6)
d._set_debug(["buying", "maint", "doors", "persons", "lug_boot", "safety"])

tree = learn(d)

print(tree.debug(0))
print(tree.decide(["low", "high", "2", "4", "med", "low"]))
print(tree.decide(["low", "low", "2", "more", "small", "high"]))

# d = Data()
# d.load_from_file("tennis.data", 5)
# tree = learn(d)
# print(" tennis test : ")
# print(tree.decide(["overcast", "hot", "normal", "false"]))
b = Container()
b.load_from_file("tennis.data", 4)
tree = learn(b)
td = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'o', 'x', 'b', 'b', 'b', 'b', 'x', 'o', 'x', 'o', 'x',
      'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'o', 'b', 'b', 'b', 'b', 'b']  # outcome win
tb = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'o', 'x', 'b', 'b', 'b', 'b', 'x', 'o', 'x', 'o', 'x',
      'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'o', 'b', 'b', 'b', 'b', 'b', 'g']  # outcome win
t._set_debug(tb)
print(tree.decide(td))
