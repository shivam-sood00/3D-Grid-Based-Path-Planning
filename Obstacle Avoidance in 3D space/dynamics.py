import numpy as np
# from drone_path_planning import global_path
dt = 0.1
# T_sim = 0
# dis_timestep = 0

def next_node(dis_timestep):
    if np.abs(dis_timestep - 1) <0.05:
        dis_timestep = 0
        return 1

def update_state(vel,dt,dis_timestep,T_sim):
    dis_timestep += vel*dt
    T_sim+=dt
    next_node(dis_timestep)

# update_state(1,0.1)
# print(dis_timestep)