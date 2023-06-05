import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

with open("connections.csv") as f:
    edges = list(map(
        lambda x: x.strip().split(";"),
        f.readlines()
    ))

# The graph to visualize
G = nx.from_edgelist(edges)

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
G0 = G.subgraph(Gcc[5]).copy()

remove = [node for node, degree in G0.degree() if degree < 2]
G0.remove_nodes_from(remove)

# 3d spring layout
pos = nx.kamada_kawai_layout(G0)

nx.draw_networkx(G0, pos=pos, node_size=20, font_size=6, font_weight="light")

plt.show()

"""# Extract node and edge positions from the layout
node_xyz = np.array([pos[v] for v in sorted(G)])
edge_xyz = np.array([(pos[u], pos[v]) for u, v in G.edges()])

# Create the 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Plot the nodes - alpha is scaled by "depth" automatically
ax.scatter(*node_xyz.T, s=100, ec="w")

# Plot the edges
for vizedge in edge_xyz:
    ax.plot(*vizedge.T, color="tab:gray")


def _format_axes(ax):
    # Visualization options for the 3D axes.
    # Turn gridlines off
    ax.grid(False)
    # Suppress tick labels
    for dim in (ax.xaxis, ax.yaxis, ax.zaxis):
        dim.set_ticks([])
    # Set axes labels
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")


_format_axes(ax)
fig.tight_layout()
plt.show()
"""