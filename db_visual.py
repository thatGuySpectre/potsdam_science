import networkx as nx
import matplotlib.pyplot as plt

from db import edges_full

while True:
    G = nx.from_edgelist(
        edges_full(input())
    )

    pos = nx.kamada_kawai_layout(G)

    nx.draw_networkx(G, pos=pos, node_size=20, font_size=12, font_weight="light", font_color="red")

    plt.show()