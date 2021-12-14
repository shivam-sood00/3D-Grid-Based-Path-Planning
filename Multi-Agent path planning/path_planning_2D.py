import networkx as nx
import matplotlib.pyplot as plt
import random
G = nx.Graph()
l,w,h = 6,6,10

#find another initializer
for i in range(l):
    for j in range(w):
        G.add_node(w*i+j, pos = (i,j))

"""
Let's have a 50% chnace of having a 0 weight
"""


#don't repeat already made edges
for i in range(l):
    for j in range(w):
        node_num = w*i+j
        zero_or_not = random.randint(0,10)
        rand_weight = zero_or_not*random.randint(0,10)  
        if (i == l-1) and (j == w-1):   #last point
            continue
        elif j == w-1:      #row end
            G.add_edge(node_num,node_num+w,weight = rand_weight)
        elif i == l-1:      #column end
            G.add_edge(node_num,node_num+1,weight = rand_weight)
        else:
            G.add_edge(node_num,node_num+1,weight = rand_weight)
            G.add_edge(node_num,node_num+w ,weight = random.randint(0,1)*random.randint(0,10))


# G.remove_node(4)
pos=nx.get_node_attributes(G,'pos')   
nx.draw(G,pos,with_labels=True)

labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
path = nx.shortest_path(G,source=3,target=30, weight='weight')
print(path)
path_edges = list(zip(path,path[1:]))
nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='r')
nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color='r',width=10)
plt.axis('equal')
plt.show()