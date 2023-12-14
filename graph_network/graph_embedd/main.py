import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from karateclub.node_embedding.neighbourhood.deepwalk import DeepWalk

G = nx.random_tree(50)

# Get node positions
# node_positions = nx.spring_layout(G)

# Draw the graph
# plt.figure(figsize=(0.5, 1))
nx.draw_networkx(G, with_labels=True, node_color='lightblue')
plt.show()
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, edge_labels=edge_labels)
plt.title('Similarity of Embedding Vectors in Graph Space')