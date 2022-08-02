# %%
import geopandas as gpd
import os
from shapely.geometry import Point
from shapely import wkt

# %%
# step 1: get all *.txt files inside results folder
results_files = os.listdir('results')

# remove anything that does not end with .txt
results_files = ['results/' + f for f in results_files if f.endswith('.txt')]

# step 2: read each file
for result_file in results_files:
    with open(result_file) as f:
        lines = f.read().splitlines()
    
    # put into shapely
    points = []
    for coords in lines:
        lon, lat = coords.split('-')
        coord = float(lon), float(lat)
        points.append(Point(coord))

    # make a geoseries
    gseries = gpd.GeoSeries(points, crs='epsg:4326')
    gseries = gseries.to_crs('epsg:32633')
    # save as file
    gseries.to_file(f'gpkgs/{result_file[8:-4]}.gpkg')


# %%