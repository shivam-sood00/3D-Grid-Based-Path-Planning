import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import globals

no_of_obstacles = 700
obs_det_rad = 4
G = nx.Graph()
l,w,h = 10,10,10

obstacle_list = []
# xl,yl,zl =[],[],[]

fig = plt.figure(figsize=(l,w))
ax = plt.axes(projection='3d')
for i in range(no_of_obstacles):
	obs_node = random.randint(1,l*w*h-2)
	if obs_node not in obstacle_list:
		obstacle_list.append(obs_node)


for i in range(l):
	for j in range(w):
		for k in range(h):
			G.add_node(w*h*i+h*j+k)

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

for i in range(len(obstacle_list)):
	x0,y0,z0 = node_num_to_xyz(obstacle_list[i],l,w,h)
	ax.scatter(x0,y0,z0)

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
				G.add_edge(node_num,node_num+w*h)
			elif (j == w-1) and (i == l-1):      
				G.add_edge(node_num,node_num+1)
			elif (k== h-1) and (i == l-1):
				G.add_edge(node_num,node_num+h)
			elif k == h-1:      #depth end
				G.add_edge(node_num,node_num+h)
				G.add_edge(node_num,node_num+w*h)
				G.add_edge(node_num,node_num+w*h+h)     
				G.add_edge(node_num+h,node_num+w*h) #width and length diagonal 2
			elif j == w-1:      #column end
				G.add_edge(node_num,node_num+1)
				G.add_edge(node_num,node_num+w*h)
				G.add_edge(node_num,node_num+w*h+1) 
				G.add_edge(node_num+1,node_num+w*h) #length and depth diagonal
			elif i == l-1:      #column end
				G.add_edge(node_num,node_num+1)
				G.add_edge(node_num,node_num+l)
				G.add_edge(node_num,node_num+h+1) 
				G.add_edge(node_num+h,node_num+1)   #depth and width diagonal
			else:
				G.add_edge(node_num,node_num+1) #depth
				G.add_edge(node_num,node_num+h) #width
				G.add_edge(node_num,node_num+w*h)  #length
				G.add_edge(node_num,node_num+w*h+h) #width and length diagonal
				G.add_edge(node_num+h,node_num+w*h) #width and length diagonal 2
				G.add_edge(node_num,node_num+h+1)   #depth and width diagonal
				G.add_edge(node_num+h,node_num+1)   #depth and width diagonal
				G.add_edge(node_num,node_num+w*h+1) #length and depth diagonal
				G.add_edge(node_num+1,node_num+w*h) #length and depth diagonal
				G.add_edge(node_num,node_num+w*h+h+1)   #Cube diagonal
				G.add_edge(node_num+h+1,node_num+w*h)   #Cube diagonal
				G.add_edge(node_num+h,node_num+w*h+1)   #Cube diagonal
				G.add_edge(node_num+1,node_num+w*h+h)   #Cube diagonal


# G.remove_node(4)
# pos=nx.get_node_attributes(G,'pos')   

G_copy = G.copy()

# def obstacle_in_radius(node,obs_det_rad):
# 	global obstacle_list
# 	rad_obs_list = []
# 	x,y,z = node_num_to_xyz(node,l,w,h)
# 	for obs_node in obstacle_list:
# 		x_o,y_o,z_o = node_num_to_xyz(obs_node,l,w,h)
# 		if (x-x_o)**2+(y-y_o)**2+(z-z_o)**2 <= obs_det_rad**2:
# 			rad_obs_list.append(obs_node)
# 			obstacle_list.remove(obs_node)
# 	return rad_obs_list

def optimal_path(start, goal,rad_obs_l,q):
	# node to xyz, cur_node to xyz, if eucl <= obs_det_rad then remove obstacle
	# rad_obs_l = obstacle_in_radius(start,obs_det_rad)
	for i in range(len(rad_obs_l)):
		G_copy.remove_node(rad_obs_l[i])

	# G_copy.remove_node(node_to_rem)

	# nx.draw(G_copy,with_labels=True)
	path = nx.shortest_path(G_copy,source=start,target=goal)
	q.put(path)