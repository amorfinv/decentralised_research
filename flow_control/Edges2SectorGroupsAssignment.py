# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 12:09:49 2022

@author: nipat
"""

import osmnx as ox
import geopandas as gd
import shapely.geometry
import pandas as pd


G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')

nodes, edges = ox.graph_to_gdfs(G)

edges=edges.to_crs(epsg='32633')

flow_grid=gd.read_file("whole_vienna/gis/grid.gpkg")

edges2flowgroup_dict={}

for ii, edg in edges.iterrows():
    edge_index=edg.index
     
    #edges_indices=list(flow_grid.sindex.intersection(edges.loc[ii]["geometry"].bounds))
    edges_indices=list(flow_grid.sindex.query(edges.loc[ii]["geometry"],predicate="intersects"))
    if edges_indices==[]:
        print("No flow group match")
    elif len(edges_indices)>1:
        lens_list=[]
        for i in edges_indices:
            grid_poly=flow_grid.loc[i]["geometry"]

            intersection_points=grid_poly.intersection(edges.loc[ii]["geometry"])
            line_seg_len=intersection_points.length
            lens_list.append(line_seg_len)
            if line_seg_len==0.0:
                print(intersection_points)
                print(i,ii)
        max_len=max(lens_list)
        flow_index=lens_list.index(max_len)
        edges_indices=[edges_indices[flow_index]]
            
    # add one to index because grid starts with index 1 and the gdf starts with index 0
    edges2flowgroup_dict[ii]=edges_indices[0] + 1
    
# drop the old flow_group column
edges.drop(columns=["flow_group"],inplace=True)    
edges['flow_group'] = pd.Series(edges2flowgroup_dict)   
edges=edges.to_crs(epsg='4326')

g=ox.graph_from_gdfs(nodes,edges)

ox.save_graphml(g,"whole_vienna/gis/graph_sector_group.graphml")

ox.save_graph_geopackage(g,"whole_vienna/gis/graph_sector_group.gpkg",directed=True)

# %%
