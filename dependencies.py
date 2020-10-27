import glob
import json
import re
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
            dependencies.add_edge(i, x)



# pos = graphviz_layout(dependencies, prog="twopi", args="", root = "./app.module")


dependentlength = []
for i in files:
    # print(i)

    if nx.has_path(dependencies, "./app.module", i) and i!="./app.module":
        # print(list(map(len, nx.all_simple_paths(dependencies, "./app.module", i))))
        dependentlength.append((i, nx.shortest_path_length(dependencies, "./app.module", i)))#, max(map(len, nx.all_simple_paths(dependencies, "./app.module", i))),3))
# print(dependentlength)
print("\n".join([str(i[0]) for i in sorted(dependentlength, key = lambda x:x[1], reverse = True)]))
# plt.subplot()
# nx.draw(dependencies, with_labels = True)
# # print(json.dumps({"./app.module":depender(files["./app.module"])}))
# plt.draw()
# plt.show()
# plt.rcParams.update({'font.size': 1})
def inc():
    i = -1
    while True:
        i+=1
        yield i+1
a = inc()
pos = {i:(-1,next(a)) for i in dependencies}
for i in dependentlength:
    pos[i[0]]=(i[1],pos[i[0]][1])
print(pos)

fig = plt.figure(figsize=(8, 24))
ax = fig.add_subplot(111)
nx.draw(dependencies, pos, node_size=0, width = 0.1, alpha = 0.6, with_labels=True, font_size = 5)
plt.axis("tight")
# ax.set_aspect(.3)
# plt.show()
plt.savefig("dependencies.svg")