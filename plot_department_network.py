# this just plots the department network so that the edges do not have to be computed again when changing the plot

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


large_threshold=10


with open("institutes.csv") as institute_file:
    institutes = list(set(map(
        lambda x: x.strip().split(":")[0],
        institute_file.readlines()
    )))

with open("authors.csv") as authors_file:
    authors_all_with_paper_number = list(map(
        lambda x: x.strip().split(":"),
        authors_file.readlines()
    ))


with open("department_edges_complete.csv") as f:
    edges = list(map(
        lambda x: (x.strip().split(";")[0],x.strip().split(";")[1],int(x.strip().split(";")[2])),
        f.readlines()
    ))


G = nx.Graph();
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

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