from drone_path_planning import optimal_path
import random
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import globals
import time

q = multiprocessing.Queue()
q2 = multiprocessing.Queue()
q2.put([0,0,0])
q3 = multiprocessing.Queue()
globals.initialize()
path = globals.path
no_of_obstacles = 400
obs_det_rad = 4
l,w,h = 10,10,10
obstacle_list = []
xl,yl,zl =[],[],[]
counter_node = 0

T_sim = 0
dis_timestep = 0

dt = 0.1
vel = 5

fig = plt.figure(figsize=(l,w))
ax = plt.axes(projection='3d')

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

for i in range(no_of_obstacles):
	obs_node = random.randint(1,l*w*h-2)
	if obs_node not in obstacle_list:
		obstacle_list.append(obs_node)


def update_state(vel,dt,q2,q3):
	val_list = q2.get()
	dis_timestep,T_sim,counter_node = val_list[0],val_list[1], val_list[2]
	dis_timestep += vel*dt
	T_sim+=dt
	print(dis_timestep)
	if np.abs(dis_timestep-1) <0.1 :
		dis_timestep = 0
		counter_node = 1
	else:
		counter_node = 0
	q2.put([dis_timestep,T_sim,counter_node])
	q3.put(counter_node)

def obstacle_in_radius(node,obs_det_rad):
	global obstacle_list
	rad_obs_list = []
	x,y,z = node_num_to_xyz(node,l,w,h)
	for obs_node in obstacle_list:
		x_o,y_o,z_o = node_num_to_xyz(obs_node,l,w,h)
		if (x-x_o)**2+(y-y_o)**2+(z-z_o)**2 <= obs_det_rad**2:
			rad_obs_list.append(obs_node)
			obstacle_list.remove(obs_node)
	return rad_obs_list

start = 0
goal = 999
global_path = [start]

if __name__ == '__main__':
	while(start != goal):
		print(path)

		rad_obs_l = obstacle_in_radius(start,obs_det_rad)
		# optimal_path(start,goal,rad_obs_l)
		p1 = multiprocessing.Process(target=optimal_path, args=(start,goal,rad_obs_l,q,))
		p2 = multiprocessing.Process(target=update_state, args=(vel,dt,q2,q3))
		p1.start()
		p2.start()	
		p1.join()
		p2.join()
		path = q.get()
		counter_node = q3.get()
		try:
			global_path.append(path[1])
		except:
			continue
		# update_state(vel,dt)
		print(counter_node)
		if counter_node== 1:
			start = path[1]

	for i in range(len(global_path)-1):
		node_num = global_path[i]
		node_num_next = global_path[i+1]
		x,y,z = node_num_to_xyz(node_num,l,w,h)
		x_n,y_n,z_n = node_num_to_xyz(node_num_next,l,w,h)
		x_line = np.linspace(x,x_n,10)
		y_line = np.linspace(y,y_n,10)
		z_line = np.linspace(z,z_n,10)
		xl.extend(x_line)
		yl.extend(y_line)
		zl.extend(z_line)		

	print("Time of simulation: ", T_sim)	
	ax.plot3D(xl,yl,zl)
	plt.show()