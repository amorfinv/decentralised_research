# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 17:00:22 2021

@author: nipat
"""
import osmnx as ox
import numpy as np
from plugins.streets.flow_control import street_graph,bbox
from plugins.streets.agent_path_planning import PathPlanning,Path
from plugins.streets.open_airspace_grid import Cell, open_airspace
from origin_destination import PreGeneratedPaths,scenario_dills
import math
import dill
from pyproj import  Transformer

# Step 1: Import the graph we will be using

G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')

edges = ox.graph_to_gdfs(G)[1]
gdf=ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
print('Graph loaded!')


#Load the open airspace grid
#input_file=open("smaller_cells_open_airspace_grid.dill", 'rb')
input_file=open("open_airspace_final.dill", 'rb')
grid=dill.load(input_file)


##Initialise the flow control entity
#input_file=open("Flow_control.dill", 'rb')
graph=street_graph(G,edges,grid) 

fig, ax = ox.plot_graph(G,node_color="w",show=False,close=False)
ax.set_xlim([16.2,16.6])
ax.set_ylim([48.1,48.3])

origins=[(16.33250526, 48.15055387)] #TODO: define teh origin destination pairs
destinations=[( 16.42270378, 48.15712307)]
##test for only manhattan, only eucleadean , both and maybe a third one in heuristic
#test for different cost of turning in compute_c, maybe dependand on bearing?
lens=[]
turn_numbers=[]
airspace_type=[] # 0 for only constrained, 1 for only open, 2 for both
algorithm_repetitions=[]
flight_durations=[]

for i in range(len(origins)):
    aircraft_type=1 # mp20
    if aircraft_type==1:
        speed_max=10.29 ##20 knots
        turn_cost=6.7
    elif aircraft_type==2:
        speed_max=15.43 # 30 knots
        turn_cost=9.75

    plan = PathPlanning(aircraft_type,grid,graph,gdf,origins[i][0], origins[i][1], destinations[i][0], destinations[i][1],0.05)
    route,turns,edges,next_turn,groups,in_constrained,turn_speed,repetition_cnt=plan.plan()
    x_list=[]
    y_list=[]
    for r in route:
        x_list.append(r[0])
        y_list.append(r[1])
    
    ax.scatter(x_list,y_list,c="b")
    
    route_cart=[]
    leng=0
    transformer = Transformer.from_crs('epsg:4326','epsg:32633')
    for j in range(len(route)):
        p=transformer.transform(route[j][1],route[j][0])
        route_cart.append(p)
        if j>0:
            leng=leng+math.sqrt((p[0]-route_cart[j-1][0])*(p[0]-route_cart[j-1][0])+(p[1]-route_cart[j-1][1])*(p[1]-route_cart[j-1][1]))
        
    lens.append(leng)
    
    
    turns[-1]=False
    constr_turns=np.logical_and(turns,in_constrained) # only count turns in constrained
    turns_cnt=np.sum(constr_turns)  
    turn_numbers.append(turns_cnt)
    
    
    airtype=np.sum(in_constrained)
    if airtype==len(in_constrained):
        airtype=0
    elif airtype==0:
        airtype=1
    else:
        airtype=2
    airspace_type.append(airtype)
    
    algorithm_repetitions.append(repetition_cnt)
    
    flight_dur=leng/speed_max+turns_cnt*turn_cost






