import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
matplotlib.use('agg')

def create_graphy(topic, pool, result):
    plt.figure()
    relations = []
    list = result.split('\'')
    G = nx.DiGraph(), i = 0, step = 0, num = 1
    while i + 6 < len(list):
        temp = [list[i + 1], list[i + 3], list[i + 5]]
        relations.append(temp)
        i += 6
    for parent in pool:
        G.add_node(parent[0], level = num)
        num = num + step
        step = 1 - step
        for i in range(len(parent[1])):
            if(parent[1][i]!= parent[0]):
                G.add_node(parent[1][i], level = 0)
                G.add_edge(parent[0], parent[1][i], edge_type = 'child')
    for relation in relations:
        G.add_edge(relation[0], relation[2], edge_type = 'parent')
    pos = nx.kamada_kawai_layout(G)
    node_sizes = [500 * (G.nodes[n]['level'] == 0) + 1000 * (G.nodes[n]['level'] != 0) for n in G.nodes()]
    node_colors = ['lightblue' if G.nodes[n]['level'] == 0 else 'lightgreen'for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size = node_sizes, node_color = node_colors)
    parent_edges = [(u, v) for u, v, attrs in G.edges(data = True) if attrs['edge_type'] == 'parent']
    nx.draw_networkx_edges(G, pos, edgelist = parent_edges, arrowstyle = '->', arrowsize = 50, width = 5, edge_color = 'gray')
    child_edges = [(u, v) for u, v, attrs in G.edges(data = True) if attrs['edge_type'] == 'child']
    nx.draw_networkx_edges(G, pos, edgelist = child_edges, arrowstyle = '-', arrowsize = 15, width = 1, edge_color = 'blue')
    nx.draw_networkx_labels(G, pos, font_size = 8, font_family = 'sans-serif')

    
    patch1 = mpatches.Patch(color = 'gray', label = 'A->B, Denotes that A is the prior knowledge of B', linewidth = 5.0, linestyle = '-', )
    patch2 = mpatches.Patch(color = 'blue', label = 'Subknowledge, indicating that the blue knowledge is a Subknowledge of the connected green one', linewidth = 1.0, linestyle = '-', )
    plt.legend(handles = [patch1, patch2], loc = 'best')
    plt.title(topic, fontsize = 16)
    plt.axis('off')
    plt.savefig('output.jpeg', dpi = 300)