# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:26:18 2022

@author: nipat
"""
import dill
import geopandas as gpd
from shapely.geometry import Point

input_file=open("cluster_center_dills/Flow_control_clusters_centers1.dill", 'rb')

clusters2=dill.load(input_file)

points2 = [Point(geom) for geom in clusters2]

gdf2 = gpd.GeoDataFrame(geometry=points2, crs='epsg:32633')

gdf2.to_file("Flow_control_clusters_centers.gpkg",driver="GPKG",layer="centers_1")

input_file=open("cluster_center_dills/Flow_control_clusters_centers2.dill", 'rb')

clusters2=dill.load(input_file)

points2 = [Point(geom) for geom in clusters2]

gdf2 = gpd.GeoDataFrame(geometry=points2, crs='epsg:32633')

gdf2.to_file("Flow_control_clusters_centers.gpkg",driver="GPKG",layer="centers_2")

input_file=open("cluster_center_dills/Flow_control_clusters_centers3.dill", 'rb')

clusters2=dill.load(input_file)

points2 = [Point(geom) for geom in clusters2]

gdf2 = gpd.GeoDataFrame(geometry=points2, crs='epsg:32633')

gdf2.to_file("Flow_control_clusters_centers.gpkg",driver="GPKG",layer="centers_3")

input_file=open("cluster_center_dills/Flow_control_clusters_centers4.dill", 'rb')

clusters2=dill.load(input_file)

points2 = [Point(geom) for geom in clusters2]

gdf2 = gpd.GeoDataFrame(geometry=points2, crs='epsg:32633')

gdf2.to_file("Flow_control_clusters_centers.gpkg",driver="GPKG",layer="centers_4")

input_file=open("cluster_center_dills/Flow_control_clusters_centers5.dill", 'rb')

clusters2=dill.load(input_file)

points2 = [Point(geom) for geom in clusters2]

gdf2 = gpd.GeoDataFrame(geometry=points2, crs='epsg:32633')

gdf2.to_file("Flow_control_clusters_centers.gpkg",driver="GPKG",layer="centers_5")

input_file=open("cluster_center_dills/Flow_control_clusters_centers6.dill", 'rb')

clusters2=dill.load(input_file)

points2 = [Point(geom) for geom in clusters2]

gdf2 = gpd.GeoDataFrame(geometry=points2, crs='epsg:32633')

gdf2.to_file("whole_vienna/gis/Flow_control_clusters_centers.gpkg",driver="GPKG",layer="centers_6")