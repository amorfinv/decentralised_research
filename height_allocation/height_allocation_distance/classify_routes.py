import os
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
# read the csv and classify the routes into five different bins
density = ['high']
list_intentions = os.listdir(f'Flight_intentions_{density[0]}')

list_dist = []
for flight_intention in list_intentions:
    # start by reading the file
    with open(f'Flight_intentions_{density[0]}/' + flight_intention, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        ll = line.split(',')
        coords = "".join(ll[4:-7])[2:~2]
        origin = coords.split(')""(')[0].split(" ")
        destination = coords.split(')""(')[1].split(" ")
        

        origin =  Point([float(origin[0]), float(origin[1])])
        destination =  Point([float(destination[0]), float(destination[1])])

        point_df = gpd.GeoSeries([origin, destination], crs=4326)

        point_df = point_df.to_crs('epsg:32633')
        
        distance = point_df.loc[0].distance(point_df.loc[1])
        
        list_dist.append(distance)


list_array = np.sort(np.array(list_dist))
split_array = np.array_split(list_array, 5)
print(len(split_array))

# get the splitting borders

# bin 1 is for values between 0 and the smallest values of array 2

l1 = [0, split_array[1][0]]
print(f'Distances for first layer: {l1}')

print('--------------')

l2 = [split_array[1][0], split_array[2][0]]
print(f'Distances for second layer: {l2}')


print('--------------')

l3 = [split_array[2][0], split_array[3][0]]        
print(f'Distances for third layer: {l3}')

print('--------------')

l4 = [split_array[3][0], split_array[4][0]]        
print(f'Distances for fourth layer: {l4}')

print('--------------')

l5 = [split_array[4][0], split_array[4][-1]]
print(f'Distances for fifth layer: {l5}')



