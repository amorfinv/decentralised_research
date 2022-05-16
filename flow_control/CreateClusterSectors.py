from pyproj import  Transformer
import matplotlib.pyplot as plt
from k_means_constrained import KMeansConstrained
import numpy as np
import matplotlib.pyplot as plt
from shapely.ops import polygonize,unary_union,cascaded_union
from shapely.geometry import LineString, MultiPolygon, MultiPoint, Point
from scipy.spatial import Voronoi,voronoi_plot_2d
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import dill
import geopandas as gpd
from shapely.geometry import Point

points=[[0.55428776, 0.5186973 ],
 [0.10756755 ,0.72728379],
 [0.76319104, 0.247727  ],
 [0.66897646, 0.9475545 ],
 [0.30037569, 0.10555964],
 [0.73659942, 0.74014518],
 [0.56356975, 0.11637416],
 [0.99941163,0.81745842],
 [0.47962557 ,0.75795864],
 [0.34912874, 0.08554759]]

#points = [ [141.48149, 3.7037036], [137.03703, -4.814815], [153.7037, -26.666668], [-2.2222223, 5.5555558], [0.0, 9.6296301], [10.74074, 20.74074], [2.2222223, 54.074074], [4.0740738, 50.740742], [34.444443, 46.296295], [11.481482, 1.4814816], [24.074076, -2.9629631], [74.814819, 79.259254], [67.777779, 152.22223], [57.037041, 127.03704], [89.259262, 12.222222]]
points = np.array(points)
conflog_file = open("CONFLOG_Flight_intention_very_low_40_8_R2_20220201_17-13-56.log", "r")
transformer = Transformer.from_crs('epsg:4326','epsg:32633')
conflog_list = list()
cnt = 0
for line in conflog_file:#load conflicts
    cnt = cnt + 1
    if cnt < 10:
        continue
    line_list = line.split(",")
    tmp_list = []

    for iv, value in enumerate(line_list):
        if  iv==9:
            tmp_list.append(float(value))
        elif iv==10:
            tmp_list.append(float(value[:-2]))
    p=transformer.transform(tmp_list[0],tmp_list[1])
    conflog_list.append([p[0],p[1]])
fig,ax = plt.subplots(1,1)
smal=[]
for i in range (100): #make small array 
    smal.append(conflog_list[i])

points=np.array(smal)   #test with small aray instead of fixed array
clf = KMeansConstrained(
     n_clusters=10,
     size_min=1,
     size_max=30,
     random_state=0
) 
clf.fit_predict(points)#cluster
label=clf.labels_
u_labels=np.unique(label)
centre=clf.cluster_centers_
# =============================================================================
# for i in u_labels:#plot clusters
#     plt.scatter(points[label == i , 0] , points[label == i , 1] , label = i,s=3)
# 
# plt.show()
# 
# points=centre#use cluster center for voronoi
# vor = Voronoi(points,qhull_options='Qbb Qc Qx')#make and plot voronoi
# fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange',
#                 line_width=2, line_alpha=0.6, point_size=2)
# plt.show()
# #make shapely polygons
# lines = [
#     LineString(vor.vertices[line])
#     for line in vor.ridge_vertices if -1 not in line
# ]
# 
# convex_hull = MultiPoint([Point(i) for i in points]).convex_hull.buffer(100)#convex hul with 100 offset
# result = MultiPolygon(
#     [poly.intersection(convex_hull) for poly in polygonize(lines)])
# result = MultiPolygon(
#     [p for p in result]
#     + [p for p in convex_hull.difference(unary_union(result))])
# pointss=np.array(smal) #show all points in next plot
# plt.plot(pointss[:,0], pointss[:,1], 'ko')
# 
# for r in result:#draw polygons
#     plt.fill(*zip(*np.array(list(
#         zip(r.boundary.coords.xy[0][:-1], r.boundary.coords.xy[1][:-1])))),
#         alpha=0.4)
# =============================================================================


#code to merge polygons built from points of the same cluster
# index=[]
# for i in range(len(points)):
#     shpoint = Point(points[i][0],points[i][1])
#     for j in range(len(result)):    
#         if(result[j].contains(shpoint)):
#             index.append(j)
#             break
# clustersh=[]        
# for i in range(10):        
#     clustersh.append([])
# for i in range(len(points)):
#     clustersh[label[i]].append(result[index[i]])
# clusteres=[]
# for i in range(len(clustersh)):
#     clusteres.append(cascaded_union(clustersh[i]))
# for r in clusteres:
#     plt.fill(*zip(*np.array(list(
#         zip(r.boundary.coords.xy[0][:-1], r.boundary.coords.xy[1][:-1])))),
#         alpha=0.4)    
    
# plt.show()

input_file=open("Flow_control_clusters_centers2.dill", 'rb')

clusters2=dill.load(input_file)

points2 = [Point(geom) for geom in clusters2]

gdf2 = gpd.GeoDataFrame(geometry=points2, crs='epsg:32633')

