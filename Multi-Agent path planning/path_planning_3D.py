import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

G = nx.Graph()
l,w,h = 10,10,10

#find another initializer
for i in range(l):
	for j in range(w):
		for k in range(h):
			G.add_node(w*h*i+h*j+k)

"""
Let's have a 50% chnace of having a 0 weight
"""
def node_num_to_xyz(node_num,l,w,h):
	x,y,z =0,0,0
	while (node_num - w*h) >= 0:
		x += 1
		node_num = node_num-w*h
	while (node_num - h) >= 0:
		y += 1
		node_num = node_num-h
	while(node_num-1) >=0:
		z += 1
		node_num -= 1
	return x,y,z

def com_ele_sam_ind(l1,l2):
	if len(l1) >= len(l2):
		a = len(l2)
	else:
		a = len(l1)
	for i in range(1,a-1):
		if l1[i] == l2[i]:
			return l1[i]
	return -1

def colis_check(l1,l2):
	if len(l1) >= len(l2):
		a = len(l2) 
	else:
		a = len(l1)	
	for i in range(a-1):
		if (l1[i] == l2[i+1]) and (l1[i+1] == l2[i]):
			return l1[i+1]
	return -1

#don't repeat already made edges
for i in range(l):
	for j in range(w):
		for k in range(h):
			node_num = w*h*i+h*j+k
			zero_or_not = random.randint(0,10)
			rand_weight = zero_or_not*random.randint(0,10)  
			if (i == l-1) and (j == w-1) and (k == h-1):   #last point
				continue
			elif (k == h-1) and (j == w-1): 
				G.add_edge(node_num,node_num+w*h,weight = rand_weight)
			elif (j == w-1) and (i == l-1):      
				G.add_edge(node_num,node_num+1,weight = rand_weight)
			elif (k== h-1) and (i == l-1):
				G.add_edge(node_num,node_num+h,weight = rand_weight)
			elif k == h-1:      #depth end
				G.add_edge(node_num,node_num+h,weight = rand_weight)
				G.add_edge(node_num,node_num+w*h,weight = random.randint(0,1)*random.randint(0,10))
			elif j == w-1:      #column end
				G.add_edge(node_num,node_num+1,weight = rand_weight)
				G.add_edge(node_num,node_num+w*h,weight = random.randint(0,1)*random.randint(0,10))
			elif i == l-1:      #column end
				G.add_edge(node_num,node_num+1,weight = rand_weight)
				G.add_edge(node_num,node_num+l,weight = random.randint(0,1)*random.randint(0,10))
			else:
				G.add_edge(node_num,node_num+1,weight = rand_weight)
				G.add_edge(node_num,node_num+h,weight = random.randint(0,1)*random.randint(0,10))
				G.add_edge(node_num,node_num+w*h ,weight = random.randint(0,1)*random.randint(0,10))


# G.remove_node(4)
# pos=nx.get_node_attributes(G,'pos')   
# nx.draw(G,with_labels=True)

no_of_inputs = int(input("How many sets: "))
start_and_goal = []
#taking nodes as input for now
for i in range(no_of_inputs):
	start = int(input("Start node: "))
	goal = int(input("Goal node: "))
	# node_num = w*h*x_pos+h*y_pos+z_pos
	start_and_goal.append([start,goal])
all_paths = []
for i in range(no_of_inputs):
	path = nx.shortest_path(G,source=start_and_goal[i][0],target=start_and_goal[i][1], weight='weight')
	# print(path)
	if len(all_paths)>0:
		for j in range(len(all_paths)):
			G_copy = G.copy()
			while (com_ele_sam_ind(list(path),all_paths[j]) != -1) or (colis_check(list(path),all_paths[j])!=-1):
				# print("Entered while", com_ele_sam_ind(list(path),all_paths[j]))
				if (com_ele_sam_ind(list(path),all_paths[j]) != -1):
					# G_copy = G.copy()
					same_node = com_ele_sam_ind(list(path),all_paths[j])
					if same_node != start and same_node != goal:
						G_copy.remove_node(same_node)
						# print("removed", same_node)
					path = nx.shortest_path(G_copy,source=start_and_goal[i][0],target=start_and_goal[i][1], weight='weight')
				else:
					colis_node = colis_check(list(path),all_paths[j])
					# print("ELSE removed",colis_node)
					G_copy = G.copy()
					G_copy.remove_node(colis_node)
					path = nx.shortest_path(G_copy,source=start_and_goal[i][0],target=start_and_goal[i][1], weight='weight')

	all_paths.append(list(path))

# print(all_paths)

fig = plt.figure(figsize=(l,w))
ax = plt.axes(projection='3d')

for i in range(len(all_paths)):
	xl,yl,zl =[],[],[]
	for j in range(len(all_paths[i])-1):
		node_num = all_paths[i][j]
		node_num_next = all_paths[i][j+1]
		x,y,z = node_num_to_xyz(node_num,l,w,h)
		x_n,y_n,z_n = node_num_to_xyz(node_num_next,l,w,h)
		# print(x,y,z)
		if x != x_n:
			x_line = np.linspace(x,x_n,50)
			shape = np.shape(x_line)
			xl.extend(x_line)
			yl.extend(y*np.ones(shape))
			zl.extend(z*np.ones(shape))
			# ax.plot3D(x_line, y*np.ones(shape), z*np.ones(shape))
		elif y != y_n:
			y_line = np.linspace(y,y_n,50)
			shape = np.shape(y_line)
			yl.extend(y_line)
			xl.extend(x*np.ones(shape))
			zl.extend(z*np.ones(shape))			
			# ax.plot3D(x*np.ones(shape), y_line, z*np.ones(shape))
		else:
			z_line = np.linspace(z,z_n,50)
			shape = np.shape(z_line)
			zl.extend(z_line)
			yl.extend(y*np.ones(shape))
			xl.extend(x*np.ones(shape))			
	ax.plot3D(xl,yl,zl)
			# ax.plot3D(x*np.ones(shape), y*np.ones(shape), z_line)
		# ax.scatter(x,y,z)
plt.show()