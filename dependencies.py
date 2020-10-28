import glob
import json
import re
import sys
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

import matplotlib.pyplot as plt

dependencies = nx.DiGraph()
files = {}
for i in glob.glob("./**/*.ts", recursive = True):
    if i[-8:]!=".spec.ts":
        with open(i, "r") as fi:
            files[i[:-3]] = list(map(lambda x: x[8:-2].split("} from ")[-1][1:].lower().replace("..", ".") ,re.findall("import \{.*?\} from [\"'].*?[\"'];", fi.read())))
# print(json.dumps(files))
# def depender(depends):
#     hasdependable = False
#     dependers = {}
#     for i in depends:
#         if i in files:
#             dependers[i] = depender(files[i])
#             hasdependable = True
#     if hasdependable:
#         return dependers
#     return depends

# for i in files:
#     dependencies.add_node(i)
# print('here')
for i in files:
    dependencies.add_node(i)
    for x in files[i]:
        if x in files:
            dependencies.add_edge(i, x, long = -1)



# pos = graphviz_layout(dependencies, prog="twopi", args="", root = "./app.module")
cycles = list(nx.simple_cycles(dependencies))
print(max(cycles, key = len))
print(sorted(cycles, key = len)[:5])
    # print(i)
dependentlength = []
root = sys.argv[1] if len(sys.argv)>1 else "./app.module"
nodes = {root}
for i in files:
    # print(i)

    if nx.has_path(dependencies, root, i) and i!=root:
        nodes.add(i)
        # print(list(map(len, nx.all_simple_paths(dependencies, "./app.module", i))))
        dependentlength.append((i, nx.shortest_path_length(dependencies, root, i)))#, nx.bellman_ford_path_length(dependencies, "./app.module", i, weight = "long")))#, max(map(len, nx.all_simple_paths(dependencies, "./app.module", i))),3))
dependencies = dependencies.subgraph(nodes).copy()
# print(dependentlength)
# print("\n".join([str(i[0]) for i in sorted(dependentlength, key = lambda x:x[1], reverse = True)]))
# plt.subplot()
# nx.draw(dependencies, with_labels = True)
# # print(json.dumps({"./app.module":depender(files["./app.module"])}))
# plt.draw()
# plt.show()
# plt.rcParams.update({'font.size': 1})

class incr:
    _vals = {}
    @classmethod
    def next(cls, level):
        if level not in cls._vals:
            cls._vals[level]=0
        else:
            cls._vals[level] = (abs(cls._vals[level])+1)*((-1)**(cls._vals[level]>0))
        return (level, cls._vals[level])

pos = {}
for i in dependentlength:
    t = incr.next(i[1])
    # print(t)
    pos[i[0]]=t#incr.next(i[1])
pos = {**pos,**{i:incr.next(0) for i in dependencies if i not in pos}}
print(pos)

fig = plt.figure(figsize=(8, 24))
ax = fig.add_subplot(111)
nx.draw(dependencies, pos, node_size=0, width = 0.1, alpha = 0.6, with_labels=True, font_size = 5)
plt.axis("tight")
# ax.set_aspect(.3)

plt.savefig("dependencies.svg")
plt.show()
