# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 17:00:22 2021

@author: nipat
"""
import osmnx as ox
import numpy as np
from plugins.streets.flow_control_geom import street_graph,bbox
from plugins.streets.agent_path_planning_geometric import PathPlanning,Path
from plugins.streets.open_airspace_grid import Cell, open_airspace
import math
import dill
from pyproj import  Transformer

import matplotlib.pyplot as plt


import matplotlib.patches as patches

from matplotlib.patches import Polygon

# Step 1: Import the graph we will be using

G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')

edges = ox.graph_to_gdfs(G)[1]
gdf=ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
print('Graph loaded!')


#Load the open airspace grid
#input_file=open("smaller_cells_open_airspace_grid.dill", 'rb')
input_file=open("open_airspace_final.dill", 'rb')
grid=dill.load(input_file)


# =============================================================================
# fig, ax = plt.subplots(1,1)
# plt.ylim([5333000,5335000])
# plt.xlim([596800,598500])
# 
# y = np.array([(597481.3078758691, 5333753.77912716), (597267.2533548912, 5333861.90225459), (597148.1071695259, 5334047.53428346), (597145.8963179928, 5334070.388227817), (597142.6392167907, 5334111.479788349), (597144.2541617001, 5334113.197119397), (597427.1830293979, 5334349.470963294), (597516.6771381629, 5334416.14656398), (597598.7605476324, 5334467.532467299), (597695.3203355772, 5334459.16404181), (597736.4108027463, 5334445.824338196), (597939.4920916636, 5334297.51806806), (597927.0666119275, 5333939.600522208)])
#    
# pol = Polygon(y, facecolor = "none",edgecolor="r")
# ax.add_patch(pol) 
# 
# y = np.array([[597397.6094564128, 5333605.189500969], [597063.0119142644, 5334160.689276934], [597780.3346441076, 5334592.7586183045], [598114.932186256, 5334037.25884234]])
#    
# pol = Polygon(y, facecolor = "none",edgecolor="b")
# ax.add_patch(pol)
# 
# =============================================================================
##Initialise the flow control entity
#input_file=open("Flow_control.dill", 'rb')
graph=street_graph(G,edges) 

fig, ax = ox.plot_graph(G,node_color="w",show=False,close=False)
ax.set_xlim([16.2,16.6])
ax.set_ylim([48.1,48.3])



origins=[(16.33250526, 48.15055387)] #TODO: define teh origin destination pairs
#destinations=[( 16.42270378, 48.15712307)]
destinations=[(16.3485847214, 48.1952774822)]#[(16.3739846152,48.262058079)]#
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

    plan = PathPlanning(aircraft_type,graph,gdf,origins[i][0], origins[i][1], destinations[i][0], destinations[i][1],0.05)
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








