# this just plots the department network so that the edges do not have to be computed again when changing the plot

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

G = nx.DiGraph();

G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,1)

pos = nx.kamada_kawai_layout(G)

nx.draw_networkx(G, pos=pos, node_size=20, font_size=12, font_weight="light", font_color="red")

plt.show()

a = [1,2,3]
b = [4,5,6]
c = a + b
print(a)
print(b)
print(c)