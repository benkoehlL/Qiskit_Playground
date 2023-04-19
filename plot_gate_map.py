import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import os

os.environ["QT_QPA_PLATFORM"] = "xcb"

G = nx.DiGraph()
G.add_edges_from(
    [('e1', 'q1'), ('e1', 'q2'), ('e1', 'q3'), ('e1', 'e2'),
      ('e2', 'q4'), ('e2', 'q5'), ('e2', 'q6'), ("e2", "e3"),
       ('e3', 'q7'), ('e3', 'q8'), ('e3', 'q9'), ('e3', 'e2') ])
color_map = []
for node in G:
    if node.find("e") != -1:
        color_map.append('blue')
    else: 
        color_map.append('red')  
pos = nx.layout.shell_layout(G)
nx.draw(G, with_labels=True, node_size=500, alpha=0.95, linewidths=15, node_color=color_map, pos=pos)
plt.show()