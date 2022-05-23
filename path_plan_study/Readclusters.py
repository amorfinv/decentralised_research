# -*- coding: utf-8 -*-
"""
Created on Mon May 16 12:01:10 2022

@author: nipat
"""
import dill
import shapely
#import geopandas as gpd
import matplotlib.pyplot as plt

from pyproj import  Transformer

# =============================================================================
# input_file=open("Flow_control_clusters_centers1.dill", 'rb')
# clusters=dill.load(input_file)
# =============================================================================



input_file=open("airspace_design/constrained_poly.dill", 'rb')
constrained_poly=dill.load(input_file)
constrained_poly=shapely.geometry.Polygon(constrained_poly)

# =============================================================================
# x,y = constrained_poly.exterior.xy
# plt.plot(x,y)
# =============================================================================

input_file=open("airspace_design/geovector_geometry.dill", 'rb')
constrained_poly=dill.load(input_file)
nfz_list=[]
for p in constrained_poly:
    poly=shapely.geometry.Polygon(p)
    nfz_list.append(poly)

x,y = nfz_list[-1].exterior.xy
plt.plot(x,y)

# =============================================================================
# plt.xlim([596000,598000])
# plt.ylim([5338000,5340000])
# 
# =============================================================================
plt.xlim([596500,597000])
plt.ylim([5338000,5338500])
 
input_file=open("airspace_design/extra_augmented_nfz_open.dill", 'rb')
constrained_poly=dill.load(input_file)
nfz_augm_list=[]
for p in constrained_poly:
    poly=shapely.geometry.Polygon(p)
    nfz_augm_list.append(poly)  
# =============================================================================
#     x,y = poly.exterior.xy
#     plt.plot(x,y)
# =============================================================================
del nfz_augm_list[-1]

# =============================================================================
# border_polygon = gpd.read_file('airspace_design/offset_border_polygon.gpkg')
# nfz_augm_list.append(border_polygon.loc[0]["geometry"])
# =============================================================================

        
input_file=open("airspace_design/geom_entries.dill", 'rb')
entries_dict=dill.load(input_file)
input_file=open("airspace_design/geom_exits.dill", 'rb')
exits_dict=dill.load(input_file)

transformer = Transformer.from_crs('epsg:4326','epsg:32633') 
for p in entries_dict.values():
     
    point=transformer.transform(p.y,p.x)
    plt.scatter(point[0],point[1])
for p in exits_dict.values():
     
    point=transformer.transform(p.y,p.x)
    plt.scatter(point[0],point[1])        