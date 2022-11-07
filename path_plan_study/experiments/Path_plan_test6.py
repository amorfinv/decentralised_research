# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 10:46:21 2022

@author: nipat
"""

import osmnx as ox
import numpy as np
import plugins.streets.flow_control as fc
import plugins.streets.flow_control_geom as fcg
import plugins.streets.agent_path_planning as pp
import plugins.streets.agent_path_planning_geometric as ppg
import plugins.streets.agent_path_planning_small_cells as ppsc
from plugins.streets.open_airspace_grid import Cell, open_airspace
from origin_destination import PreGeneratedPaths,scenario_dills
import math
import dill
from pyproj import  Transformer
import time
import copy
import shapely.geometry
import geopandas as gpd
import sys
from pympler import asizeof


# Step 1: Import the graph we will be using
G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')

edges = ox.graph_to_gdfs(G)[1]
gdf=ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
print('Graph loaded!')

#Load the open airspace grid
input_file=open("smaller_cells_open_airspace_grid.dill", 'rb')
grid_smaller_cells=dill.load(input_file)

input_file=open("open_airspace_final.dill", 'rb')
grid_orig=dill.load(input_file)

# load the geofence gdfs
geo_gdf = gpd.read_file('geofences.gpkg', driver='GPKG')

##configure teh origin-destination pairs
# Get Origin-Destination pairs list of all sending receiving nodes
# data is organized as (lon, lat, lon, lat)
pairs_list = PreGeneratedPaths()

# NOW JUST GET THE ONES THAT ARE IN THE SCENARIOS of Flight_intention_*_40*.scn
# THE ENTRIES INSIDE dill_list CORRESPOND TO AN INDEX IN pairs_list
dill_list = scenario_dills()

num_path_plans=1000
flight_plan_step=math.floor(len(dill_list)/num_path_plans)

path_plan_pairs=[]
pair_index=0
for i in range(num_path_plans):
     path_plan_pairs.append(pairs_list[dill_list[pair_index]])
     pair_index+=flight_plan_step
     
     
results_dict={}



##Original and heuristic tests
graph=fc.street_graph(copy.deepcopy(G),copy.deepcopy(edges),grid_orig) 

experiment=6
file1 = open("Turns_test6.txt","a")

if 1:
    pp.experiment_number=experiment
    lens=[]
    turn_numbers=[]
    intersection_numbers=[]
    airspace_type=[] # 0 for only constrained, 1 for only open, 2 for both
    dstar_repetitions=[]
    geom_repetitions=[]
    flight_durations=[]
    computation_time=[]
    aircraft_types=[]
    geobreach=[] #1 for geofence intersections
    memory_size=[]
    node_points=[] 
    for pair in path_plan_pairs:
        for aircraft_type in [1,2]:
            if aircraft_type==1:
                speed_max=10.29 ##20 knots
                turn_cost=6.7
            elif aircraft_type==2:
                speed_max=15.43 # 30 knots
                turn_cost=9.75
                
            aircraft_types.append(aircraft_type)  
            start=time.time()
            plan = pp.PathPlanning(aircraft_type,grid_orig,graph,gdf,pair[0], pair[1], pair[2], pair[3],0.05)
            route,turns,edges,next_turn,groups,in_constrained,turn_speed,repetition_cnt=plan.plan()
            end=time.time()
            
            computation_time.append(end-start)
            del plan.flow_graph
            ss=asizeof.asizeof(plan)
            memory_size.append(ss)
            if route==[]:
                lens.append(-1)
                turn_numbers.append(-1)
                airspace_type.append(-1)
                dstar_repetitions.append(-1)
                geom_repetitions.append(0)
                flight_durations.append(-1)
                geobreach.append(-1) 
                continue
            node_points+=route
            linestring = shapely.geometry.LineString(route)
        
            # loop through the geofence gdfs
            geo=0
            for idx, geofence in enumerate(geo_gdf.geometry):
                # check if the linestring intersects with the geofence
                if linestring.intersects(geofence):
                    geo=1
                
            geobreach.append(geo)              
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
            intersection_numbers.append(turns_cnt)
            turns_cnt=np.sum(turns)  
            turn_numbers.append(turns_cnt)
            for j in range(len(turns)):
                if turns[j]:
                    tt=str(route[j][0])+"-"+str(route[j][1])+"\n"
                    file1.write(tt)
            
            
            airtype=np.sum(in_constrained)
            if airtype==len(in_constrained):
                airtype=0
            elif airtype==0 or airtype==1:
                airtype=1
            else:
                airtype=2
            airspace_type.append(airtype)
            
            dstar_repetitions.append(repetition_cnt)
            geom_repetitions.append(0)
            
            flight_dur=leng/speed_max+turns_cnt*turn_cost
            flight_durations.append(flight_dur)
            
    orig_dict={}
    orig_dict["lens"]=lens
    orig_dict["turn_numbers"]=turn_numbers
    orig_dict["intersection_numbers"]=intersection_numbers
    orig_dict["airspace_type"]=airspace_type
    orig_dict["dstar_repetitions"]=dstar_repetitions
    orig_dict["geom_repetitions"]=geom_repetitions
    orig_dict["flight_durations"]=flight_durations
    orig_dict["computation_time"]=computation_time
    orig_dict["aircraft_types"]=aircraft_types
    orig_dict["geobreach"]=geobreach    
    orig_dict["memory_size"]=memory_size



output_file=open(f"Path_points_exp6.dill", 'wb')
dill.dump(node_points,output_file)
output_file.close()

output_file=open(f"Path_plan_results_experiment6.dill", 'wb')
dill.dump(orig_dict,output_file)
output_file.close()

file1.close()
