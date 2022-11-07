# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 17:00:22 2021

@author: nipat
"""
import osmnx as ox
import numpy as np
from plugins.streets.flow_control import street_graph,bbox
from plugins.streets.agent_path_planning_small_cells import PathPlanning,Path
from plugins.streets.open_airspace_grid import Cell, open_airspace
import math
import dill
from pyproj import  Transformer

import matplotlib.pyplot as plt

import geopandas
from pympler import asizeof

import matplotlib.patches as patches

from matplotlib.patches import Polygon

import shapely.geometry



# Step 1: Import the graph we will be using

G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')

edges = ox.graph_to_gdfs(G)[1]
gdf=ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
print('Graph loaded!')


#Load the open airspace grid
input_file=open("smaller_cells_open_airspace_grid.dill", 'rb')
#input_file=open("open_airspace_final.dill", 'rb')
grid=dill.load(input_file)



##Initialise the flow control entity
#input_file=open("Flow_control.dill", 'rb')
graph=street_graph(G,edges,grid) 

fig, ax = ox.plot_graph(G,node_color="w",show=False,close=False)
ax.set_xlim([16.2,16.6])
ax.set_ylim([48.1,48.3])



countries_gdf = geopandas.read_file("airspace_design/geofences_big.gpkg")
city_gdf = geopandas.read_file("airspace_design/updated_constrained_airspace.gpkg")

fig, ax = plt.subplots(1,1)
plt.ylim([5330000,5350000])
plt.xlim([593000,609000])

countries_gdf.plot(ax=ax)


city_gdf.plot(ax=ax,facecolor="g")


transformer = Transformer.from_crs('epsg:4326','epsg:32633')
po=transformer.transform( 48.1754361401,16.3605530148)
pd=transformer.transform( 48.2218205729,16.2905608666)




origins=[(16.3791707414, 48.1563157781)] #TODO: define teh origin destination pairs
#destinations=[( 16.42270378, 48.15712307)]
destinations=[(16.4512130406, 48.169089774)]#[(16.3485847214, 48.1952774822)]#
i=0

or_p=transformer.transform(origins[i][1],origins[i][0])
des_node=transformer.transform(destinations[i][1],destinations[i][0])


plan = PathPlanning(1,grid,graph,gdf,origins[i][0], origins[i][1], destinations[i][0], destinations[i][1],0.05)
route,turns,edges,next_turn,groups,in_constrained,turn_speed,repetition_cnt=plan.plan()

print(asizeof.asizeof(plan))
del plan.flow_graph
print(asizeof.asizeof(plan))
ss= asizeof.asizeof(plan)

for i in range(len(grid.grid)):
    p=grid.grid[i]

    y = np.array([[p.p0[0], p.p0[1]], [p.p1[0], p.p1[1]], [p.p2[0] ,p.p2[1]], [p.p3[0], p.p3[1]]])
    if i !=1129 and i!=1130:
        pol = Polygon(y, facecolor = "none",edgecolor="k")
    
    
        #pol = Polygon(y, facecolor = "none",edgecolor="g")
    ax.add_patch(pol)



x_list=[]
y_list=[]
route_cart=[]
transformer = Transformer.from_crs('epsg:4326','epsg:32633')
for j in range(len(route)):
    p=transformer.transform(route[j][1],route[j][0])
    route_cart.append(p)
    x_list.append(p[0])
    y_list.append(p[1])
ax.scatter(x_list,y_list,c="r")
plt.plot(x_list,y_list,c="r")
ax.scatter(x_list[0],y_list[0],c="b")
ax.scatter(x_list[-1],y_list[-1],c="y")

#print constrained airspace intersection points
#ax.scatter(597697.7476655138, 5333831.029879483,c="k")#interssection
#ax.scatter(602848.1827974739, 5335215.000422393,c="k")
#ax.scatter(599223.3464280792, 5343795.70864978,c="y")



##print origin, destiantion
#ax.scatter(or_p[0],or_p[1],c="g")
#ax.scatter(des_node[0],des_node[1],c="k")



#constrained start point
#p=transformer.transform(48.165514369279606,16.364637686902217)
#ax.scatter(p[0],p[1],c="g")
#constrained dest point
#p=transformer.transform(48.165514369279606,16.364637686902217)
#ax.scatter(p[0],p[1],c="y")

plt.show()



