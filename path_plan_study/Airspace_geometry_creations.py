# -*- coding: utf-8 -*-
"""
Created on Mon May 23 11:55:11 2022

@author: nipat
"""

import shapely.geometry
import dill
import geopandas as gpd
from shapely.ops import transform
import pyproj


    # Read in the geopackage
constrained_airspace = gpd.read_file('airspace_design/updated_constrained_airspace.gpkg').to_crs(epsg=4326)

    # get geometry
poly_geom = list(constrained_airspace.loc[0, 'geometry'].boundary.coords)


x,y = constrained_airspace.loc[0, 'geometry'].boundary.coords.xy
    
transformer = pyproj.Transformer.from_crs( 'epsg:4326','epsg:32633')



polygon_points=[]

for i in range(len(x)):
    pp=transformer.transform(y[i],x[i])
    polygon_points.append(pp)

constrained_poly=shapely.geometry.Polygon(polygon_points)
print(constrained_poly)

output_file=open(f"airspace_design/constrained_poly.dill", 'wb')
dill.dump(constrained_poly,output_file)
output_file.close()
