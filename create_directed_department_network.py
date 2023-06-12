# idea: create directed graph from undirected
# duplicate each undirected edge
# normalize outgoing edges so that sum == 1


# this just plots the department network so that the edges do not have to be computed again when changing the plot

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


large_threshold=0.015


with open("institutes.csv") as institute_file:
    institutes = map(
        lambda x: x.strip().split(":"),
        institute_file.readlines()
    )

with open("authors.csv") as authors_file:
    authors_all_with_paper_number = list(map(
        lambda x: x.strip().split(":"),
        authors_file.readlines()
    ))


with open("department_edges_complete.csv") as f:
    edges1 = list(map(
        lambda x: (x.strip().split(";")[0],x.strip().split(";")[1],float(x.strip().split(";")[2])),
        f.readlines()
    ))

edges2=[]
for edge in edges1:
    edges2.append((edge[1], edge[0], edge[2]))
edges = edges1 + edges2

# now we have all edges
# next we need to normalize

G = nx.DiGraph()

for department, sum_papers in institutes:
    edges_by_department=[(edge[0], edge[1], edge[2]) for edge in edges if edge[0] == department]
    # check for error
    sum = 0.
    for edge in edges_by_department:
        sum = sum + edge[2]
    for edge in edges_by_department:
        G.add_edge(edge[0], edge[1], weight=edge[2]/sum)
#for edge in edges:
#    G.add_edge(edge[0], edge[1], weight=edge[2])


print(list(G)[0])
print(G.in_edges(nbunch=list(G)[0], data='weight'))

with open("department_in_degrees.csv", 'w') as department_in_degree_file:
    for department, degree in sorted(G.in_degree(weight='weight'),reverse=True,key=lambda n: n[1]):
        print(f"{department}:{degree}",file=department_in_degree_file)


elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > large_threshold]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= large_threshold]

pos = nx.kamada_kawai_layout(G)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=50)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
nx.draw_networkx_edges(
    G, pos, edgelist=esmall, width=0.5, alpha=0.5, edge_color="b", style="dashed"
)

# node labels
nx.draw_networkx_labels(G, pos, font_size=7, font_family="sans-serif")
# edge weight labels
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6)

#nx.draw_networkx(G, pos=pos, node_size=20, font_size=12, font_weight="light", font_color="red")

plt.show()