from matplotlib import pyplot as plt
import matplotlib as mpl
import networkx as nx

from db import *


def color(components, graph):
    out = []

    for n in graph.nodes:
        for i, m in enumerate(components):
            if n in m:
                out.append(i)
                break

    low, high = min(out), max(out)
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.gist_rainbow)

    return [mapper.to_rgba(i) for i in out]


edges = edges_simple(Abteilungen="Institut für Physik und Astronomie", Erscheinungsjahr=list(range(1990, 2000)))

G = nx.from_edgelist(edges)

G = G.subgraph(max(nx.connected_components(G), key=len).copy())

modules = nx.community.greedy_modularity_communities(G)

nx.draw_networkx(G, node_size=20, font_size=6, font_weight="light", node_color=color(modules, G))

plt.show()
