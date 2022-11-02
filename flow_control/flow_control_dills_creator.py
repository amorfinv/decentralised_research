# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 17:00:22 2021

@author: nipat
"""
import osmnx as ox
import numpy as np

#from plugins.streets.flow_control import street_graph,bbox
from plugins.streets.flow_control_clusters2 import street_graph,bbox#unocmment that and comment the previous line to create teh flow control dill for clusters

from plugins.streets.agent_path_planning import PathPlanning,Path
from plugins.streets.open_airspace_grid import Cell, open_airspace
import os
import dill
import json
import sys
from pympler import asizeof
import math
from shapely.geometry import LineString
import shapely.geometry
from pyproj import  Transformer
from os import path

# set folder where dill will be saved
dill_folder = 'graph_data/M2_baseline'

# Step 1: Import the graph we will be using
G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')
#G = ox.io.load_graphml('processed_graph.graphml')
edges = ox.graph_to_gdfs(G)[1]
gdf=ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
print('Graph loaded!')



#Load the open airspace grid
input_file=open("airspace_design/open_airspace_final.dill", 'rb')
#input_file=open("open_airspace_grid_updated.dill", 'rb')##for 3d path planning
grid=dill.load(input_file)


##Initialise the flow control entity
graph=street_graph(G,edges,grid) 






output_file=open(f"Flow_control.dill", 'wb')
dill.dump(graph,output_file)
output_file.close()




