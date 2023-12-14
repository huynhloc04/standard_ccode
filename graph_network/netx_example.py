import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Sample embedding vectors
embeddings = {
    'A': np.array([0.2, 0.4, 0.8]),
    'B': np.array([-0.3, 0.1, -0.5]),
    'C': np.array([0.6, -0.2, 0.3]),
    'D': np.array([-0.1, -0.5, 0.9])
}

# Create an empty graph
G = nx.Graph()

# Add nodes to the graph
for node, embedding in embeddings.items():
    G.add_node(node)

# Calculate similarity between embeddings and add edges
for node1, embedding1 in embeddings.items():
    for node2, embedding2 in embeddings.items():
        if node1 != node2:
            # Calculate cosine similarity
            similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
            G.add_edge(node1, node2, weight=similarity)

# Get node positions
node_positions = nx.spring_layout(G)

# Draw the graph
plt.figure(figsize=(8, 8))
nx.draw(G, pos=node_positions, with_labels=True, node_color='lightblue', node_size=1000, font_size=12, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_labels)
plt.title('Similarity of Embedding Vectors in Graph Space')
plt.show()