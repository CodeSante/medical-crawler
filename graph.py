import json
import networkx as nx
import matplotlib.pyplot as plt

# Charger les données
with open('data.json') as f:
    data = json.load(f)

# Initialisation du graph
G = nx.Graph()

# Ajout des nœuds et des arêtes
for page in data:
    url = page['url']
    G.add_node(url)
    for keyword in page['keywords_title'] + page['keywords_description'] + page['keywords_h'] + page['keywords_p']:
        G.add_node(keyword)
        G.add_edge(url, keyword)

# Positionnement des nœuds sur le plan 2D
pos = nx.spring_layout(G)

# Tracé du graph
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
nx.draw_networkx_edges(G, pos, edge_color='gray')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

# Affichage du graph
plt.axis('off')
plt.show()
