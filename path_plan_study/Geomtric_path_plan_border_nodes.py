# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 16:21:57 2022

@author: nipat
"""
import json
from pyproj import  Transformer
import osmnx as ox
import geopandas as gpd
import shapely.geometry
import dill

f = open('airspace_design/entries.txt','r')      
contents = f.read()
f.close()
entry_points_list_tmp=[int(x) for x in contents.split(",")]
         
f = open('airspace_design/exits.txt','r')
contents = f.read()
f.close()
exit_points_list_tmp=[int(x) for x in contents.split(",")]  

with open('whole_vienna/gis/old_to_new_nodes.json', 'r') as filename:
            old2new_nodes_dict = json.load(filename)
          
            
entry_points_list=[] 
exit_points_list=[]             
for i in   entry_points_list_tmp   :
    entry_points_list.append(old2new_nodes_dict[str(i)])
for i in   exit_points_list_tmp   :
    exit_points_list.append(old2new_nodes_dict[str(i)])  
          
G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')
transformer = Transformer.from_crs('epsg:4326','epsg:32633')

border_nodes = gpd.read_file('airspace_design/offset_border_nodes.gpkg')





input_file=open("airspace_design/extra_augmented_nfz_open.dill", 'rb')
constrained_poly=dill.load(input_file)
nfz_augm_list=[]
for p in constrained_poly:
    poly=shapely.geometry.Polygon(p)
    nfz_augm_list.append(poly) 

entry_points_dict={}

exit_points_dict={}

for index in entry_points_list:
    lon=G._node[index]['x']
    lat=G._node[index]['y']
    p=transformer.transform(lat,lon)
    ##find closest point
    d=float("inf")
    min_index=-1
    for ii, poi in border_nodes.iterrows():
        point=border_nodes.loc[ii]["geometry"]
        dd=(p[0]-point.x)*(p[0]-point.x)+(p[1]-point.y)*(p[1]-point.y)
        if dd<d:
            d=dd
            min_index=ii

    point=border_nodes.loc[min_index]["geometry"]
    in_geofence=False
    for poly in nfz_augm_list:
        if poly.contains(point):
            in_geofence=True
            break
    if not in_geofence:
        entry_points_dict[index]=shapely.geometry.Point(border_nodes.loc[min_index].x,border_nodes.loc[min_index].y)

for index in exit_points_list:
    lon=G._node[index]['x']
    lat=G._node[index]['y']
    p=transformer.transform(lat,lon)
    ##find closest point
    d=float("inf")
    min_index=-1
    for ii, poi in border_nodes.iterrows():
        point=border_nodes.loc[ii]["geometry"]
        dd=(p[0]-point.x)*(p[0]-point.x)+(p[1]-point.y)*(p[1]-point.y)
        if dd<d:
            d=dd
            min_index=ii
    point=border_nodes.loc[min_index]["geometry"]
    in_geofence=False
    for poly in nfz_augm_list:
        if poly.contains(point):
            in_geofence=True
            break
    if not in_geofence:
        exit_points_dict[index]=shapely.geometry.Point(border_nodes.loc[min_index].x,border_nodes.loc[min_index].y)
            

output_file=open("airspace_design/geom_entries.dill", 'wb')
dill.dump(entry_points_dict,output_file)
output_file.close()  

output_file=open("airspace_design/geom_exits.dill", 'wb')
dill.dump(exit_points_dict,output_file)
output_file.close()         