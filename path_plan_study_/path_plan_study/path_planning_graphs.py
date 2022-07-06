# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 17:00:22 2021

@author: nipat
"""
import osmnx as ox
import numpy as np
from plugins.streets.flow_control import street_graph,bbox
from plugins.streets.agent_path_planning_graphs import PathPlanning,Path
from plugins.streets.open_airspace_grid import Cell, open_airspace
from origin_destination import PreGeneratedPaths,scenario_dills
import math
import dill
from pyproj import  Transformer

import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry 
from matplotlib.patches import Polygon
import geopandas

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

countries_gdf = geopandas.read_file("airspace_design/geofences_big.gpkg")
city_gdf = geopandas.read_file("airspace_design/updated_constrained_airspace.gpkg")

fig, ax = plt.subplots(1,1)
plt.ylim([5330000,5350000])
plt.xlim([593000,609000])

countries_gdf.plot(ax=ax)


city_gdf.plot(ax=ax,facecolor="g")


origins=[(16.33250526, 48.15055387)] #TODO: define teh origin destination pairs
destinations=[( 16.42270378, 48.15712307)]
oo=[596050,5335330]
dd=[597855,5333593]
dd=[597711,5333369]
transformer = Transformer.from_crs('epsg:32633','epsg:4326')
p=transformer.transform(oo[0],oo[1])
origins=[(p[1], p[0])]
p=transformer.transform(dd[0],dd[1])
destinations=[(p[1], p[0])]

plan = PathPlanning(1,grid,graph,gdf,origins[0][0], origins[0][1], destinations[0][0], destinations[0][1],0.05)
route,nodes,turns,edges,next_turn,groups,in_constrained,turn_speed,repetition_cnt=plan.plan()

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

x_list=[]
y_list=[]
n_cart=[]
for j in range(len(nodes)):
    p=transformer.transform(nodes[j][1],nodes[j][0])
    n_cart.append(p)
    x_list.append(p[0])
    y_list.append(p[1])
ax.scatter(x_list,y_list,c="y")
plt.plot(x_list,y_list,c="y")
plt.show()


