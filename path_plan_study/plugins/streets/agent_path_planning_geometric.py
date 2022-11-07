# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 10:51:03 2021

@author: nipat
"""


import heapq
import numpy as np
import math
import copy
from shapely.geometry import Point,LineString
from shapely.geometry.polygon import Polygon
from pyproj import  Transformer
import shapely
from plugins.streets.flow_control_geom import street_graph,bbox
from plugins.streets.open_airspace_grid import Cell, open_airspace


#Find the nearest node used as entry point to constrained airspace
def get_nearest_entry_node(graph,p):
    transformer = Transformer.from_crs('epsg:4326','epsg:32633')  
    point=transformer.transform(p.y,p.x)
    entry_with_distances = [
        (
            entry,
            (point[0]-graph.nodes_graph[entry].x_cartesian)*(point[0]-graph.nodes_graph[entry].x_cartesian)+(point[1]-graph.nodes_graph[entry].y_cartesian)*(point[1]-graph.nodes_graph[entry].y_cartesian)
        )
        for entry in graph.entry_points_list
    ]
    entry_with_distances = sorted(entry_with_distances, key=lambda x: x[1])

    u = entry_with_distances[0][0]
    
    v=graph.nodes_graph[u].parents[0]
    
    return u,v

#Find the nearest node used as exit point from constrained airspace
def get_nearest_exit_node(graph,p):
    transformer = Transformer.from_crs('epsg:4326','epsg:32633')  
    point=transformer.transform(p.y,p.x)
    exit_with_distances = [
        (
            exit_n,
            (point[0]-graph.nodes_graph[exit_n].x_cartesian)*(point[0]-graph.nodes_graph[exit_n].x_cartesian)+(point[1]-graph.nodes_graph[exit_n].y_cartesian)*(point[1]-graph.nodes_graph[exit_n].y_cartesian)
        )
        for exit_n in graph.exit_points_list
    ]
    exit_with_distances = sorted(exit_with_distances, key=lambda x: x[1])

    u = exit_with_distances[0][0]
    
    v=graph.nodes_graph[u].children[0]
    
    return u,v

def find_closest_point_on_linesegment(line,point):
    ##https://diego.assencio.com/?index=ec3d5dfdfc0b6a0d147a656f0af332bd
    
    if line[0]==line[1]:
        return line[0]
    
    pp=[0,0]
    ls=((point[0]-line[0][0])*(line[1][0]-line[0][0])+(point[1]-line[0][1])*(line[1][1]-line[0][1]))/((line[1][0]-line[0][0])*(line[1][0]-line[0][0])+(line[1][1]-line[0][1])*(line[1][1]-line[0][1]))
    if ls<=0:
        pp=line[0]
    elif ls>=1:
        pp=line[1]
    else:
        pp[0]=line[0][0]+ls*(line[1][0]-line[0][0])
        pp[1]=line[0][1]+ls*(line[1][1]-line[0][1])
        
    return pp

def distance_point(A,B):
    R = 6372800  # Earth radius in meters
    lat1=A[1]
    lon1=A[0]
    lat2=B[1]
    lon2=B[0]
        
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
        
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))     

##Returns the nearest edge of a point
def get_nearest_edge(gdf, point):
    """
    Return the nearest edge to a pair of coordinates. Pass in a graph and a tuple
    with the coordinates. We first get all the edges in the graph. Secondly we compute
    the euclidean distance from the coordinates to the segments determined by each edge.
    The last step is to sort the edge segments in ascending order based on the distance
    from the coordinates to the edge. In the end, the first element in the list of edges
    will be the closest edge that we will return as a tuple containing the shapely
    geometry and the u, v nodes.
    Parameters
    ----------
    G : networkx multidigraph
    point : tuple
        The (lat, lng) or (y, x) point for which we will find the nearest edge
        in the graph
    Returns
    -------
    closest_edge_to_point : tuple (shapely.geometry, u, v)
        A geometry object representing the segment and the coordinates of the two
        nodes that determine the edge section, u and v, the OSM ids of the nodes.
    """
    
    transformer = Transformer.from_crs('epsg:4326','epsg:32633')
    graph_edges = gdf[["geometry"]].values.tolist()
    #print("graph_edges ",len(graph_edges))


    conv_graph_edges=[]

    for i in range(len(graph_edges)):

        
        tt=np.asarray(graph_edges[i][0].coords)

        tr=[]
        for item in tt:
            r1=transformer.transform(item[1],item[0])
            tr.append(r1)

        conv_graph_edges.append([LineString(tr)])
        
    #print("conv_graph_edges ",len(conv_graph_edges))
    graph_edges=conv_graph_edges
    graph_edges_indexes=gdf.index.tolist()
    for i in range(len(graph_edges)):# maybe do that faster?
        graph_edges[i].append(graph_edges_indexes[i][0])
        graph_edges[i].append(graph_edges_indexes[i][1])

   
   
    #2.5495288748492004e-05 740 580
    
    test_point=transformer.transform(point[0],point[1])
    #print(test_point)
    
    edges_with_distances = [
        (
            graph_edge,
            Point(test_point).distance(graph_edge[0])
            #Point(tuple(reversed(point))).distance(graph_edge[0])
        )
        for graph_edge in graph_edges
    ]
    
    edges_with_distances = sorted(edges_with_distances, key=lambda x: x[1])
 #   for i in range(10):
  #      print(edges_with_distances[i][1])
    closest_edge_to_point = edges_with_distances[0][0]

    
    geometry, u, v = closest_edge_to_point
    distance=edges_with_distances[0][1]

    #print(geometry)
    #print(u,v)

    return geometry, u, v,distance

##from geo.py
def rwgs84(latd):
    """ Calculate the earths radius with WGS'84 geoid definition
        In:  lat [deg] (latitude)
        Out: R   [m]   (earth radius) """
    lat    = np.radians(latd)
    a      = 6378137.0       # [m] Major semi-axis WGS-84
    b      = 6356752.314245  # [m] Minor semi-axis WGS-84
    coslat = np.cos(lat)
    sinlat = np.sin(lat)

    an     = a * a * coslat
    bn     = b * b * sinlat
    ad     = a * coslat
    bd     = b * sinlat

    # Calculate radius in meters
    r = np.sqrt((an * an + bn * bn) / (ad * ad + bd * bd))

    return r

##from geo.py
def qdrdist(latd1, lond1, latd2, lond2):
    """ Calculate bearing and distance, using WGS'84
        In:
            latd1,lond1 en latd2, lond2 [deg] :positions 1 & 2
        Out:
            qdr [deg] = heading from 1 to 2
            d [nm]    = distance from 1 to 2 in nm """

    # Haversine with average radius for direction

    # Constants
    nm  = 1852.  # m       1 nautical mile

    # Check for hemisphere crossing,
    # when simple average would not work

    # res1 for same hemisphere
    res1 = rwgs84(0.5 * (latd1 + latd2))

    # res2 :different hemisphere
    a    = 6378137.0       # [m] Major semi-axis WGS-84
    r1   = rwgs84(latd1)
    r2   = rwgs84(latd2)
    res2 = 0.5 * (abs(latd1) * (r1 + a) + abs(latd2) * (r2 + a)) / \
        (np.maximum(0.000001,abs(latd1) + abs(latd2)))

    # Condition
    sw   = (latd1 * latd2 >= 0.)

    r    = sw * res1 + (1 - sw) * res2

    # Convert to radians
    lat1 = np.radians(latd1)
    lon1 = np.radians(lond1)
    lat2 = np.radians(latd2)
    lon2 = np.radians(lond2)



    coslat1 = np.cos(lat1)
    coslat2 = np.cos(lat2)

    qdr = np.degrees(np.arctan2(np.sin(lon2 - lon1) * coslat2,
                                coslat1 * np.sin(lat2) -
                                np.sin(lat1) * coslat2 * np.cos(lon2 - lon1)))

    return qdr,0

        
class Path:
    def __init__(self,start,goal,speed,graph):
        self.start=start
        self.goal=goal
        self.k_m=0
        self.queue=[]
        self.origin_node_index=None
        self.speed=speed
        self.graph=graph
        
##Initialise the path planning      
def initialise(path,flow_graph):
    path.queue=[]
    path.k_m=0
    path.graph.rhs_list[path.goal]=0  #path.goal.rhs=0
    path.graph.inQueue_list[path.goal]=True #path.goal.inQueue=True
    h=heuristic(path.start,path.goal,path.speed,flow_graph,path.graph) #path.goal.h=heuristic(path.start,path.goal,path.speed,flow_graph)
    path.graph.expanded_list[path.goal]=True   #path.goal.expanded=True
    gg=copy.deepcopy(path.goal)
    heapq.heappush(path.queue, (h,0,path.goal))
    path.origin_node_index=path.start
 

##Compare the keys of two nodes
def compare_keys(key1,key2):
    if key1[0]<key2[0]:
        return True
    elif key1[0]==key2[0] and key1[1]<key2[1]:
        return True
    return False
    
##Calculate the keys of a node    
def calculateKey(node,start, path,flow_graph,graph):

    return (min(graph.g_list[node], graph.rhs_list[node]) + heuristic(node,start,path.speed,flow_graph,graph) + path.k_m, min(graph.g_list[node], graph.rhs_list[node]))
    #return (min(node.g, node.rhs) + heuristic(node,start,path.speed,flow_graph) + path.k_m, min(node.g, node.rhs))

##Calculate the distance of two points in cartesian coordinates
def eucledean_distance(p1,p2):
    return  math.sqrt((p1.x_cartesian-p2.x_cartesian)*(p1.x_cartesian-p2.x_cartesian)+ (p1.y_cartesian-p2.y_cartesian)*(p1.y_cartesian-p2.y_cartesian) )    

def heuristic(current, goal,speed,flow_graph,graph):
    cc=flow_graph.nodes_graph[graph.key_indices_list[current]]
    gg=flow_graph.nodes_graph[graph.key_indices_list[goal]]



    av_speed_vertical=5.0


    h=(abs(cc.x_cartesian-gg.x_cartesian)+abs(cc.y_cartesian-gg.y_cartesian))/speed
    
    if graph.groups_list[current]!=graph.groups_list[goal]:
        h=h+9.144/av_speed_vertical

                     
    return h


##Compute the cost of moving from a node to its neighborh node
def compute_c(current,neigh,edges_speed,flow_graph,speed,graph):
    av_speed_vertical=5.0
    g=1
    cc=flow_graph.nodes_graph[graph.key_indices_list[current]]
    nn=flow_graph.nodes_graph[graph.key_indices_list[neigh]]

    if graph.groups_list[current]!=graph.groups_list[neigh]:

        g=9.144/av_speed_vertical
        
    else:
            #check if the group is changing (the drone needs to turn)
        if graph.groups_list[current]==graph.groups_list[neigh]:
            if edges_speed[graph.key_indices_list[current]][graph.key_indices_list[neigh]]==0:
                g=float('inf')
    
            else:
                g=flow_graph.edges_graph[graph.key_indices_list[current]][graph.key_indices_list[neigh]].length/min(edges_speed[graph.key_indices_list[current]][graph.key_indices_list[neigh]],speed)
    return g    

##Return the top key of the queue 
def top_key(q):
    if len(q) > 0:
        return [q[0][0],q[0][1]]
    else:
        #print('empty queue!')
        return [float('inf'), float('inf')]
    
##Update the vertex of a node
def update_vertex(path,node,flow_graph,graph):

    if graph.g_list[node]!=graph.rhs_list[node] and graph.inQueue_list[node]:     
        #Update
        id_in_queue = [item for item in path.queue if node==item[2]]
        if id_in_queue != []:
            if len(id_in_queue) != 1:
                raise ValueError('more than one ' + str(node) + ' in the queue!')
            graph.key_list[node]=calculateKey(node, path.start, path,flow_graph,graph)
            path.queue[path.queue.index(id_in_queue[0])]=path.queue[-1]
            path.queue.pop()
            heapq.heapify(path.queue)
            heapq.heappush(path.queue, (graph.key_list[node][0],graph.key_list[node][1],node))
            
    elif graph.g_list[node]!=graph.rhs_list[node] and (not graph.inQueue_list[node]):
        #Insert
        graph.inQueue_list[node]=True
        graph.key_list[node]=calculateKey(node, path.start, path,flow_graph,graph)
        heapq.heappush(path.queue, (graph.key_list[node][0],graph.key_list[node][1],node))
        
    elif graph.g_list[node]==graph.rhs_list[node] and graph.inQueue_list[node]: 
        #remove
        id_in_queue = [item for item in path.queue if node==item[2]]
        
        if id_in_queue != []:
            if len(id_in_queue) != 1:
                raise ValueError('more than one ' + id + ' in the queue!')
            graph.inQueue_list[node]=False
            path.queue[path.queue.index(id_in_queue[0])]=path.queue[-1]
            path.queue.pop()
            heapq.heapify(path.queue)
          

          
##Compute the shortest path using D* Lite
##returns flase if no path was found
def compute_shortest_path(path,graph,edges_speed,flow_graph):

    graph.key_list[path.start]=calculateKey(path.start, path.start, path,flow_graph,graph)
    k_old=top_key(path.queue)
    
    repetition_cnt=0
   
    while graph.rhs_list[path.start]>graph.g_list[path.start] or compare_keys(k_old,graph.key_list[path.start]):

        if len(path.queue)==0:
            #print("No path found!")
            return 0
        repetition_cnt=repetition_cnt+1

        k_old=top_key(path.queue)
        current_node=path.queue[0][2]#get the node with the highest priority
        graph.expanded_list[current_node]=True

        
        k_new=calculateKey(current_node, path.start, path,flow_graph,graph)
        
        if compare_keys(k_old, k_new):
            heapq.heappop(path.queue)
            graph.key_list[current_node]=k_new
            graph.inQueue_list[current_node]=True
            graph.expanded_list[current_node]=True
            heapq.heappush(path.queue, (graph.key_list[current_node][0],graph.key_list[current_node][1],current_node))
            
        elif graph.g_list[current_node]>graph.rhs_list[current_node]:
            graph.g_list[current_node]=graph.rhs_list[current_node]
            heapq.heappop(path.queue)
            graph.inQueue_list[current_node]=False

            for p in graph.parents_list[current_node]:
                if p==65535:
                    break

                if p!=path.goal:
                    graph.rhs_list[p]=min(graph.rhs_list[p],graph.g_list[current_node]+compute_c(p,current_node,edges_speed,flow_graph,path.speed,graph))
                update_vertex(path, p,flow_graph,graph)
        else:
            g_old=copy.deepcopy(graph.g_list[current_node])
            graph.g_list[current_node]=float('inf')
            pred_node=current_node

                    
            for p in graph.parents_list[current_node]:
                if p==65535:
                    break
                if graph.rhs_list[p]==(g_old+compute_c(p,current_node,edges_speed,flow_graph,path.speed,graph)):
                    if(p!=path.goal):
                        tt=[]
                        for ch in graph.children_list[p]:
                            if ch==65535:
                                break

                            tt.append(graph.g_list[ch]+compute_c(p,ch,edges_speed,flow_graph,path.speed,graph))
                        graph.rhs_list[p]=min(tt)
                update_vertex(path, p,flow_graph,graph)
            if graph.rhs_list[pred_node]==g_old:
                if pred_node!= path.goal:
                    tt=[]
                    for ch in graph.children_list[pred_node]:
                        if ch==65535:
                            break
                        tt.append(graph.g_list[ch]+compute_c(pred_node,ch,edges_speed,flow_graph,path.speed,graph))
                    graph.rhs_list[pred_node]=min(tt)
            update_vertex(path, pred_node,flow_graph,graph)               

        k_old=top_key(path.queue)
        graph.key_list[path.start]=calculateKey(path.start, path.start, path,flow_graph,graph)
        

    graph.g_list[path.start]=graph.rhs_list[path.start]
            
    return 'Path found!' ,repetition_cnt



class SearchGraph:
    def __init__(self,key_indices_list,groups_list,parents_list,children_list,g_list,rhs_list,key_list,inQueue_list,expanded_list):
        
        self.start_ind=-1
        self.goal_ind=-1
        self.start_point=Point(tuple((-1,-1)))
        self.goal_point=Point(tuple((-1,-1)))

        self.key_indices_list=np.array(key_indices_list,dtype=np.uint16)
        self.groups_list=np.array(groups_list,dtype=np.uint16)

        self.g_list=np.array(g_list,dtype=np.float32) 
        self.rhs_list=np.array(rhs_list,dtype=np.float32)
        self.key_list=np.array(key_list,dtype=np.float64)
        self.inQueue_list=np.array(inQueue_list,dtype=np.bool8)
        self.expanded_list=np.array(expanded_list,dtype=np.bool8)

        self.parents_list = np.ones([len(parents_list),len(max(parents_list,key = lambda x: len(x)))],dtype=np.uint16)*65535
        for i,j in enumerate(parents_list):
            self.parents_list[i][0:len(j)] =j
            
        #65535 means empty
        self.children_list = np.ones([len(children_list),len(max(children_list,key = lambda x: len(x)))],dtype=np.uint16)*65535
        for i,j in enumerate(children_list):
            self.children_list[i][0:len(j)] =j

        
class PathPlanning:
    
    def __init__(self,aircraft_type,flow_control_graph,gdf,lon_start,lat_start,lon_dest,lat_dest,exp_const=0.01):
        self.aircraft_type=aircraft_type
        self.start_index=None
        self.start_index_previous=None
        self.start_in_open=True
        self.goal_index=None
        self.goal_index_next=None
        self.dest_in_open=True
        self.open_airspace_grid=None#open_airspace_grid
        self.flow_graph=flow_control_graph # that is shared memory so it shoudl be fine
        self.flow_control_graph=copy.deepcopy(flow_control_graph)
        self.gdf=gdf
        self.G = None
        self.edge_gdf={} 
        self.path=None

        
        self.route=[]
        self.turns=[]
        self.priority=1 #4,3,2,1 in decreasing priority
        self.loitering=False
        self.init_succesful=True
        self.loitering_edges=None
        self.only_in_open=True
        
        self.start_point=Point(tuple((lon_start,lat_start)))
        self.goal_point=Point(tuple((lon_dest,lat_dest)))
        
        self.start_point_orig=Point(tuple((lon_start,lat_start)))
        self.goal_point_orig=Point(tuple((lon_dest,lat_dest)))

        


        self.cutoff_angle=25
        
        self.open_airspace_cells=[]
        
        if self.aircraft_type==1:
            self.speed_max=10.29 ##20 knots
        elif self.aircraft_type==2:
            self.speed_max=15.43 # 30 knots
            
  
        ##Check if origina and destination points are in constrained airspace
        transformer = Transformer.from_crs('epsg:4326','epsg:32633')  
        p=transformer.transform(lat_start,lon_start)
        point_s = Point(p[0],p[1])
        if flow_control_graph.constrained_poly_buff.contains(point_s):
            self.start_in_open=False
        p=p=transformer.transform(lat_dest,lon_dest)
        point_d = Point(p[0],p[1])
        if flow_control_graph.constrained_poly_buff.contains(point_d):
            self.dest_in_open=False

            
        if self.start_in_open or self.dest_in_open:
            line = [(point_s.x,point_s.y), (point_d.x, point_d.y)]
            shapely_line = LineString(line)
   
            intersection_line=flow_control_graph.constrained_poly.intersection(shapely_line)

            if intersection_line.is_empty :
                self.only_in_open=True
            else:
                self.only_in_open=False

    
                if  intersection_line.geom_type=='Point':
                    coords = list(intersection_line.coords)
                elif intersection_line.geom_type=='GeometryCollection':
                    #print(intersection_line)
                    coords=[]
                    for l in intersection_line:
                        if l.geom_type=='LineString':
                            for lp in list(l.coords):
                                coords.append(lp)
                        else:
                            coords.append(l.coords)

                elif intersection_line.geom_type=='MultiLineString':
                    coords=[]
                    for l in intersection_line:
                        for lp in list(l.coords):
                            coords.append(lp)
                elif intersection_line.geom_type=='LineString':
                    coords = list(intersection_line.coords)


                #coords = list(intersection_line.coords)
                transformer = Transformer.from_crs('epsg:32633','epsg:4326') 
                if self.start_in_open and self.dest_in_open:
                    ds1=float("inf")
                    ps_index=-1
                    dd1=float("inf")
                    pd_index=-1
                    for i in range(len(coords)):
                        ds2=(coords[i][0]-point_s.x)*(coords[i][0]-point_s.x)+(coords[i][1]-point_s.y)*(coords[i][1]-point_s.y) 
                        dd2=(coords[i][0]-point_d.x)*(coords[i][0]-point_d.x)+(coords[i][1]-point_d.y)*(coords[i][1]-point_d.y) 
                        if ds2<ds1:
                            ps_index=i
                            ds1=ds2
                        if dd2<dd1:
                            pd_index=i
                            dd1=dd2
                    pp=transformer.transform(coords[pd_index][0],coords[pd_index][1])
                    self.goal_point=Point(tuple((pp[1],pp[0]))) 

                    pp=transformer.transform(coords[ps_index][0],coords[ps_index][1])
                    self.start_point=Point(tuple((pp[1],pp[0])))  
            
                elif self.start_in_open:
                    d1=float("inf")
                    p_index=-1
                    for i in range(len(coords)):
                        d2=(coords[i][0]-point_s.x)*(coords[i][0]-point_s.x)+(coords[i][1]-point_s.y)*(coords[i][1]-point_s.y) 
                        if d2<d1:
                            p_index=i
                            d1=d2
                    pp=transformer.transform(coords[p_index][0],coords[p_index][1])
                    self.start_point=Point(tuple((pp[1],pp[0])))                    
                elif self.dest_in_open:
                    d1=float("inf")
                    p_index=-1
                    for i in range(len(coords)):
                        d2=(coords[i][0]-point_d.x)*(coords[i][0]-point_d.x)+(coords[i][1]-point_d.y)*(coords[i][1]-point_d.y) 
                        if d2<d1:
                            p_index=i
                            d1=d2

                    pp=transformer.transform(coords[p_index][0],coords[p_index][1])
                    self.goal_point=Point(tuple((pp[1],pp[0]))) 
                
        else:
            self.only_in_open=False
            
        if self.only_in_open:
            del self.flow_control_graph #empty these, we do not need it any more
            del self.gdf
            return
            
        ##Find the index of the start and dest in teh constrained graph    
        
                 

        if self.start_in_open:
            point=Point(self.start_point.y,self.start_point.x)
            u,v=get_nearest_entry_node(self.flow_graph, point)
            self.start_index=u
            self.start_index_previous=v
            self.start_point=Point(tuple((self.flow_graph.nodes_graph[self.start_index].lon,self.flow_graph.nodes_graph[self.start_index].lat)))
        else:
            point=(self.start_point.y,self.start_point.x)
            geometry, u, v,distance=get_nearest_edge(self.gdf, point) 
            self.start_index=v
            self.start_index_previous=u
        if self.dest_in_open:

            point=Point(self.goal_point.y,self.goal_point.x)
            u,v=get_nearest_exit_node(self.flow_graph, point)
            self.goal_index_next=v
            self.goal_index=u
            self.goal_point=Point(tuple((self.flow_graph.nodes_graph[self.goal_index].lon,self.flow_graph.nodes_graph[self.goal_index].lat)))

        else:
            point=(self.goal_point.y,self.goal_point.x)
            geometry, u, v,distance=get_nearest_edge(self.gdf, point)
            self.goal_index_next=v
            self.goal_index=u

        lats=[self.start_point.y,self.goal_point.y,self.flow_graph.nodes_graph[self.start_index].lat,self.flow_graph.nodes_graph[self.start_index_previous].lat,self.flow_graph.nodes_graph[self.goal_index].lat,self.flow_graph.nodes_graph[self.goal_index_next].lat]
        lons=[self.start_point.x,self.goal_point.x,self.flow_graph.nodes_graph[self.start_index].lon,self.flow_graph.nodes_graph[self.goal_index].lon]
        box=bbox(min(lats)-exp_const,min(lons)-exp_const,max(lats)+exp_const,max(lons)+exp_const) 
            
        G,edges=self.flow_control_graph.extract_subgraph(box)
        self.G=copy.deepcopy(G)
        for k in list(edges.keys()):
            for kk in list(edges[k].keys()):
                key=str(k)+'-'+str(kk)
                self.edge_gdf[key]=edges[k][kk].speed

        del self.flow_control_graph #empty these, we do not need it any more
        del self.gdf
        
        
        #Create the graph
        
        key_indices_list=[]
        groups_list=[]
        parents_list=[]
        children_list=[]
        g_list=[]
        rhs_list=[]
        key_list=[]
        inQueue_list=[]
        expanded_list=[]
        
        omsnx_keys_list=list(self.G.keys())
        os_keys2_indices=[]
        tmp_dict={}
        tmp_cnt=0
        omsnx_keys_list.sort()

        new_nodes_counter=0
        for i in range(len(omsnx_keys_list)):
           key=omsnx_keys_list[i]

           parents=self.G[key].parents
           children=self.G[key].children
           my_group={} 

           ii=0
           tmp=[]#list if the groups that the node has been added
           for p in parents:

               if not ii:
                   if (str(p)+'-'+str(key)) in list(self.edge_gdf.keys()): 

                       group=np.uint16(int(self.flow_graph.edges_graph[p][key].stroke_group))
                       key_indices_list.append(key)
                       groups_list.append(group)
                       g_list.append(float("inf"))
                       rhs_list.append(float("inf"))
                       key_list.append([0.0,0.0])
                       inQueue_list.append(False)
                       expanded_list.append(False)
                       children_list.append([])
                       parents_list.append([])
                       my_group.update({i+new_nodes_counter:group})
                       tmp.append(group)
                       ii=ii+1

                       if key not in tmp_dict.keys():
                           tmp_dict[key]=tmp_cnt
                           tmp_cnt=tmp_cnt+1
                           os_keys2_indices.append([key,i+new_nodes_counter])

                       elif (i+new_nodes_counter)  not in os_keys2_indices[tmp_dict[key]][1:]:
                           os_keys2_indices[tmp_dict[key]].append(i+new_nodes_counter)

                               
               else: 
                if (str(p)+'-'+str(key)) in list(self.edge_gdf.keys()):  
                        new_nodes_counter=new_nodes_counter+1
                        group=np.uint16(int(self.flow_graph.edges_graph[p][key].stroke_group))
                        key_indices_list.append(key)
                        groups_list.append(group)
                        g_list.append(float("inf"))
                        rhs_list.append(float("inf"))
                        key_list.append([0.0,0.0])
                        inQueue_list.append(False)
                        expanded_list.append(False)
                        children_list.append([])
                        parents_list.append([])
                        my_group.update({i+new_nodes_counter:group})
                        tmp.append(group)
                        ii=ii+1
                        if key not in tmp_dict.keys():
                           tmp_dict[key]=tmp_cnt
                           tmp_cnt=tmp_cnt+1
                           os_keys2_indices.append([key,i+new_nodes_counter])
 
                             
                        elif (i+new_nodes_counter)  not in os_keys2_indices[tmp_dict[key]][1:]:
                           os_keys2_indices[tmp_dict[key]].append(i+new_nodes_counter)

                           
           for ch in children:
                group=np.uint16(int(self.flow_graph.edges_graph[key][ch].stroke_group))
                if not group in tmp:
                    if not ii:
                        my_group.update({i+new_nodes_counter:group})
                        key_indices_list.append(key)
                        groups_list.append(group)
                        g_list.append(float("inf"))
                        rhs_list.append(float("inf"))
                        key_list.append([0.0,0.0])
                        inQueue_list.append(False)
                        expanded_list.append(False)
                        children_list.append([])
                        parents_list.append([])
                        tmp.append(group)
                        ii=ii+1
                        if key not in tmp_dict.keys():
                           tmp_dict[key]=tmp_cnt
                           tmp_cnt=tmp_cnt+1
                           os_keys2_indices.append([key,i+new_nodes_counter])
                        elif (i+new_nodes_counter)  not in os_keys2_indices[tmp_dict[key]][1:]:
                            os_keys2_indices[tmp_dict[key]].append(i+new_nodes_counter)

                        
                    else:
                        new_nodes_counter=new_nodes_counter+1
                        key_indices_list.append(key)
                        groups_list.append(group)
                        g_list.append(float("inf"))
                        rhs_list.append(float("inf"))
                        key_list.append([0.0,0.0])
                        inQueue_list.append(False)
                        expanded_list.append(False)
                        children_list.append([])
                        parents_list.append([])
                        my_group.update({i+new_nodes_counter:group})
                        tmp.append(group)
                        ii=ii+1
                        if key not in tmp_dict.keys():
                           tmp_dict[key]=tmp_cnt
                           tmp_cnt=tmp_cnt+1
                           os_keys2_indices.append([key,i+new_nodes_counter])
                        elif (i+new_nodes_counter)  not in os_keys2_indices[tmp_dict[key]][1:]:
                            os_keys2_indices[tmp_dict[key]].append(i+new_nodes_counter)
                        
           if ii==0:
               key_indices_list.append(key)
               groups_list.append(2000)
               g_list.append(float("inf"))
               rhs_list.append(float("inf"))
               key_list.append([0.0,0.0])
               inQueue_list.append(False)
               expanded_list.append(False)
               children_list.append([])
               parents_list.append([])

                        
           if len(my_group)>1:
               for index in my_group:
                   for index_ in my_group:
                        if my_group[index]!=my_group[index_] and index!=index_:
                            children_list[index].append(index_)
                            parents_list[index].append(index_)     
                            
        #add the children and parents to each node                
        for ii,i in enumerate(key_indices_list):
            if 1:
                key=i
                parents=self.G[key].parents
                children=self.G[key].children
                for p in parents:
                    for jj,j in enumerate(key_indices_list):
                        if p==j and (groups_list[jj]==groups_list[ii] or groups_list[ii] ==2000) :
                            parents_list[ii].append(jj)                 
                            if i not in tmp_dict.keys():
                               tmp_dict[i]=tmp_cnt
                               tmp_cnt=tmp_cnt+1
                               os_keys2_indices.append([i,ii])
                            elif ii  not in os_keys2_indices[tmp_dict[i]][1:]:
                               os_keys2_indices[tmp_dict[i]].append(ii)                            
                            break
              
                for ch in children:
                    for jj,j in enumerate(key_indices_list):
                        if ch==j and (groups_list[jj]==groups_list[ii] or groups_list[ii] ==2000) :
                            children_list[ii].append(jj)
                            if i not in tmp_dict.keys():
                               tmp_dict[i]=tmp_cnt
                               tmp_cnt=tmp_cnt+1
                               os_keys2_indices.append([i,ii])
                            elif ii  not in os_keys2_indices[tmp_dict[i]][1:]:
                               os_keys2_indices[tmp_dict[i]].append(ii)                      
                            break


        del self.G
        del self.edge_gdf
        self.graph=SearchGraph(key_indices_list,groups_list,parents_list,children_list,g_list,rhs_list,key_list,inQueue_list,expanded_list)
        

        transformer = Transformer.from_crs('epsg:4326','epsg:32633')
        p=transformer.transform(lat_start,lon_start)
        self.graph.start_point=Point(tuple((p[0],p[1])))
        p=transformer.transform(lat_dest,lon_dest)
        self.graph.goal_point=Point(tuple((p[0],p[1])))
        if self.dest_in_open:
            self.graph.goal_ind=self.goal_index
        if self.start_in_open:
            self.graph.start_ind=self.start_index
         
        self.os_keys2_indices = np.ones([len(os_keys2_indices),len(max(os_keys2_indices,key = lambda x: len(x)))],dtype=np.uint16)*65535
        for i,j in enumerate(os_keys2_indices):
            self.os_keys2_indices[i][0:len(j)] =j
        

    ##Function handling the path planning process
    ##Retruns: route,turns,edges_list,next_turn_point,groups,in_constrained,turn_speed
    ##route is the list of waypoints (lon,lat)
    ##turns is the list of booleans indicating for every waypoint if it is a turn
    ##edges_list is the list of the edges
    ##next_turn_point is a list containing the coord of every point that is a turn point
    ##groups is the list of the group in which each waypoint belongs to
    ##in_constrained is the list of booleans indicating for every waypoint if it is in constarined airspace
    ##turn_speed is teh list if speed to be used if the waypoint is a turning waypoint   
    def plan(self):
        next_turn_point=[]
        repetition_cnt=0
        geom_rep=0
        
        if self.only_in_open:
            route,turns,edges_list,groups,in_constrained,turn_speed,geom_rep=self.compute_open_path(self.start_point_orig, self.goal_point_orig,True)

            
        else:
            if self.start_in_open and self.dest_in_open:
                route_open,turns_open,edges_list_open,groups_open,in_constrained_open,turn_speed_open,geom_rep=self.compute_open_path(self.start_point_orig, self.flow_graph.entries_dict[self.start_index])
                route_open_g,turns_open_g,edges_list_open_g,groups_open_g,in_constrained_open_g,turn_speed_open_g,geom_rep_d=self.compute_open_path(self.flow_graph.exits_dict[self.goal_index], self.goal_point_orig,False)

                geom_rep+=geom_rep_d
            elif self.start_in_open :
                #print(self.flow_graph.entries_dict[self.start_index])
                route_open,turns_open,edges_list_open,groups_open,in_constrained_open,turn_speed_open,geom_rep=self.compute_open_path(self.start_point_orig, self.flow_graph.entries_dict[self.start_index])
            elif self.dest_in_open:
                route_open,turns_open,edges_list_open,groups_open,in_constrained_open,turn_speed_open,geom_rep=self.compute_open_path(self.flow_graph.exits_dict[self.goal_index], self.goal_point_orig,False)

            
            start_id=None
            goal_id=None
            
            
            result = np.where(self.os_keys2_indices ==self.start_index)
            rr=np.where(result[1] ==0)
            if 1:
                for ii in self.os_keys2_indices[result[0][rr]][0][1:]:
                    if ii==65535:
                        break
                    for p in self.graph.parents_list[ii]:
                        if p ==65535:
                            break
                        if self.start_index_previous==self.graph.key_indices_list[p]:
                            start_id=ii
                            break
                    if start_id !=None:
                        break
            result = np.where(self.os_keys2_indices ==self.goal_index)
            rr=np.where(result[1] ==0)
            if 1:
                for ii in self.os_keys2_indices[result[0][rr]][0][1:]:
                    if ii==65535:
                        break
                    for p in self.graph.children_list[ii]:
                        if p ==65535:
                            break
                        if self.goal_index_next==self.graph.key_indices_list[p]:
                            goal_id=ii
                            break
                    if goal_id !=None:
                        break 
    
                
            start_node=start_id
            goal_node=goal_id
    
    
            self.path=Path(start_node,goal_node,self.speed_max,self.graph)
            
            initialise(self.path,self.flow_graph)
            
            path_found,repetition_cnt=compute_shortest_path(self.path,self.graph,self.flow_graph.edges_init_speed,self.flow_graph)        
            route=[]
            turns=[]
            edges_list=[]
            next_turn_point=[]
            indices_nodes=[]
            #turn_indices=[]
            if path_found:
                route,turns,indices_nodes,turn_coord,groups,in_constrained,turn_speed,init_groups=self.get_path(self.path,self.graph,self.flow_graph.edges_init_speed,self.flow_graph.edges_graph)
    
                if route==None:
                    print("No path found")
                    #No path was found
                    return [],[],[],[],[],[],[],[]
                
                os_id1=self.start_index_previous
    
                os_id2=indices_nodes[0]

                if not( init_groups[0]==2000 and init_groups[2]!=2000) :
                    edges_list.append((os_id1,os_id2))
                        
                    nodes_index=1
        
                for i in range(len(init_groups)-1):
                    edges_list.append((os_id1,os_id2))
                    if nodes_index>len(init_groups)-2:
                        break
                    if nodes_index<len(init_groups)-1 and indices_nodes[nodes_index+1]==os_id2:
                        nodes_index=nodes_index+1
                        continue
  
                    nodes_index=nodes_index+1
                    os_id1=os_id2
                    os_id2=indices_nodes[nodes_index]
    
    
                    
                cnt=0
                for i in range(len(turns)):
                    if turns[i]:# and in_constrained[i]:
                        next_turn_point.append(turn_coord[cnt])
                        cnt=cnt+1
                    else:
                        next_turn_point.append(turn_coord[cnt])    
                        
                turns[-1]=True
                turn_speed[-1]=5                        
                
            if self.start_in_open and self.dest_in_open:

                route=route_open+route+route_open_g#[::-1]
                turns=turns_open+turns+turns_open_g#[::-1]
                edges_list=edges_list_open+edges_list+edges_list_open_g
                groups=groups_open+groups+groups_open_g
                in_constrained=in_constrained_open+in_constrained+in_constrained_open_g
                turn_speed=turn_speed_open+turn_speed+turn_speed_open_g#[::-1]
            elif self.start_in_open :
                route=route_open+route
                turns=turns_open+turns
                edges_list=edges_list_open+edges_list
                groups=groups_open+groups
                in_constrained=in_constrained_open+in_constrained
                turn_speed=turn_speed_open+turn_speed
            elif self.dest_in_open:
                route=route+route_open#[::-1]
                turns=turns+turns_open#[::-1]
                edges_list=edges_list+edges_list_open
                groups=groups+groups_open
                in_constrained=in_constrained+in_constrained_open
                turn_speed=turn_speed+turn_speed_open#[::-1]


        self.route=np.array(route,dtype=np.float64)
        self.turns=np.array(turns,dtype=np.bool8) 
        self.edges_list=np.array(edges_list) 
        self.next_turn_point=next_turn_point
        self.groups=np.array(groups,dtype=np.uint16)
        self.in_constrained=np.array(in_constrained,dtype=np.bool8)
        self.turn_speed=np.array(turn_speed,dtype=np.uint16())
        
        return route,turns,edges_list,next_turn_point,groups,in_constrained,turn_speed ,repetition_cnt,geom_rep
    
    ##Function to compute the path for open airspace
    #P1 should always be the point in open and p2 the open in constrained, except if both point in open
    #if p2 in constarined teh function may update teh entry/exit point, to be used from D*
    #if the path is from constrained to destination the input variable entry shoudl be set to False
    def compute_open_path(self,p1, p2,entry=True):
        rep=1
        route=[(p1.x,p1.y)]
        turns=[False]
        edges_list=[(5999,6000)]
        next_turn_point=[(-999,-999)]
        groups=[2000]
        in_constrained=[False]
        turn_speed=[0]
        
        transformer = Transformer.from_crs('epsg:4326','epsg:32633')  
        p=transformer.transform(p1.y,p1.x)
        pp1 = Point(p[0],p[1])
        p=transformer.transform(p2.y,p2.x)
        pp2 = Point(p[0],p[1])

       
        
# =============================================================================
#         ##If p2 entry or exit point, it should get moved towards open airspace
#         if not self.only_in_open:
#             th=math.atan2(pp1.x-pp2.x,pp1.y-pp2.y)
#             pp2=Point(pp2.x+2*math.cos(th),pp2.y+2*math.sin(th))
# =============================================================================

            

        
        line = [(pp1.x,pp1.y), (pp2.x, pp2.y)]
        shapely_line = LineString(line)

        
        poly_intersection_points=[]
        poly_indices=[]
        for i,p in enumerate(self.flow_graph.nfz_list):
            intersection_line=p.intersection(shapely_line)
            if intersection_line.is_empty or intersection_line.geom_type=='Point':
                continue
            if intersection_line.geom_type=='GeometryCollection':
                intersection_line=intersection_line[0]
            if intersection_line.geom_type=='MultiLineString':
                points=[]
                for l in intersection_line:
                    for lp in list(l.coords):
                        points.append(lp)
            else:
                try:
                    points=list(intersection_line.coords)
                except:
                    print(intersection_line.geom_type)
            for p_i in points:
                poly_intersection_points.append(p_i)
                poly_indices.append(i) ## Debug_note that was outsie the for p_i in points
            
        if poly_indices==[]:
            #No intersection with nfzs
            route.append((p2.x,p2.y))
            turns.append(False)
            edges_list.append((5999,6000))
            next_turn_point.append((-999,-999))
            groups.append(2000)
            in_constrained.append(False)
            turn_speed.append(5)
        else:
            #Find the closest intersection point

           
            rep+=1

            
            ##Find the closest polygon point of teh extra augmented polygons to the closets intersection point and add it to route after converting it to geodetic 
            
            poly_indices_set=set(poly_indices)
            #print(poly_indices_set)
            
            poly_intersection_points=[]
            poly_indices=[]

            for i in poly_indices_set:
                p=self.flow_graph.nfz_augm_list[i]
                intersection_line=p.intersection(shapely_line)
                if intersection_line.is_empty or intersection_line.geom_type=='Point':
                    continue
                if intersection_line.geom_type=='GeometryCollection':
                    intersection_line=intersection_line[0]
                if intersection_line.geom_type=='MultiLineString':
                    points=[]
                    for l in intersection_line:
                        for lp in list(l.coords):
                            points.append(lp)
                else:
                    try:
                        points=list(intersection_line.coords)
                    except:
                        print(intersection_line.geom_type)
                for p_i in points:
                    poly_intersection_points.append(p_i)
                    poly_indices.append(i)
            distance_list=[]
            
            for p in poly_intersection_points:
                d=(p[0]-pp1.x)*(p[0]-pp1.x)+(p[1]-pp1.y)*(p[1]-pp1.y)
                distance_list.append(d)
            min_d=min(distance_list)
            i=distance_list.index(min_d)
            poly_index=poly_indices[i]
  
            closest_intersection_point=poly_intersection_points[i]
            #print(closest_intersection_point)
            #print(poly_index)

            poly=self.flow_graph.nfz_augm_list[poly_index]
            poly_direction={}
            
            transformer = Transformer.from_crs('epsg:32633','epsg:4326')  

            p_tmp=transformer.transform(closest_intersection_point[0],closest_intersection_point[1])
            
            route.append((p_tmp[1],p_tmp[0]))
            turns.append(False)
            edges_list.append((5999,6000))
            next_turn_point.append((-999,-999))
            groups.append(2000)
            in_constrained.append(False)
            turn_speed.append(5)

            i,direction=get_neighbouring_poly_vertice_and_direction(poly,closest_intersection_point,pp2)
            
            
            pp_tmp1=Point(list(poly.exterior.coords)[i][0],list(poly.exterior.coords)[i][1])

            pp1=pp_tmp1
            poly_direction[poly_index]=[[i],direction]

            p_tmp=transformer.transform(pp1.x,pp1.y)
            p_intermediate= Point(p[1],p[0])
            route.append((p_tmp[1],p_tmp[0]))
            turns.append(False)
            edges_list.append((5999,6000))
            next_turn_point.append((-999,-999))
            groups.append(2000)
            in_constrained.append(False)
            turn_speed.append(0)
            
            ##Draw new line from current point to p2 
            line = [(pp1.x,pp1.y), (pp2.x, pp2.y)]
            shapely_line = LineString(line)
            
            ##If path only in open check if teh line inetrsects any geofences repeat the process until it does not 
            if 1:#self.path_only_in_open:#TODO look if for entry and exit points an extra step should be added to updated the entry/exit node
                intersection=True
            
                poly_intersection_points=[]
                poly_indices=[]
                for i,p in enumerate(self.flow_graph.nfz_list):
                    intersection_line=p.intersection(shapely_line)
                    if intersection_line.is_empty or intersection_line.geom_type=='Point':
                        continue
                 
                    if intersection_line.geom_type=='GeometryCollection':
                        intersection_line=intersection_line[0]
                    if intersection_line.geom_type=='MultiLineString':
                        #print(i)
                        #print(intersection_line)
                        points=[]
                        for l in intersection_line:
                            for lp in list(l.coords):
                                points.append(lp)
                    else:
                        try:
                            points=list(intersection_line.coords)
                        except:
                            print(intersection_line.geom_type)
                    for p_i in points:
                        poly_intersection_points.append(p_i)
                        poly_indices.append(i) ## Debug_note that was outsie the for p_i in points
                if poly_indices==[]:
                    intersection=False
                while intersection:
                    #print(poly_indices)
                    #Find the closest intersection point
                    distance_list=[]
                    for p in poly_intersection_points:
                        d=(p[0]-pp1.x)*(p[0]-pp1.x)+(p[1]-pp1.y)*(p[1]-pp1.y)
                        distance_list.append(d)
                    min_d=min(distance_list)
                    i=distance_list.index(min_d)
                    poly_index=poly_indices[i]
                    #print(poly_index)
                    
                    p_intermediate= Point(poly_intersection_points[i][0],poly_intersection_points[i][1])   
                    rep+=1

                    ##Find the closest polygon point of teh extra augmented polygons to the closets intersection point and add it to route after converting it to geodetic 

                    poly=self.flow_graph.nfz_augm_list[poly_index]
                    coords=list(poly.exterior.coords)[:-1]#coords=list(poly.convex_hull.exterior.coords)[:-1]
                    if poly_index in poly_direction.keys():
                        if poly_direction[poly_index][1]==0:
                            i=poly_direction[poly_index][0][0]
                            poly_p=coords[(i+1)%len(coords)]
                            d1=(poly_p[0]-pp2.x)*(poly_p[0]-pp2.x)+(poly_p[1]-pp2.y)*(poly_p[1]-pp2.y)
                            poly_p=coords[(i-1+len(coords))%(len(coords))]
                            d2=(poly_p[0]-pp2.x)*(poly_p[0]-pp2.x)+(poly_p[1]-pp2.y)*(poly_p[1]-pp2.y)
                            if d1<d2:
                                poly_direction[poly_index][1]=1 ##TODO :find a better way to decide on the direction
                                poly_direction[poly_index][0].append((i+1)%(len(coords)))
                                i=(i+1)%len(coords)
                                pp1=Point(coords[i][0],coords[i][1])
                            else:
                                poly_direction[poly_index][1]=-1
                                poly_direction[poly_index][0].append((i-1+len(coords))%(len(coords)))
                                i=(i-1+len(coords))%(len(coords))
                                pp1=Point(coords[i][0],coords[i][1])
                        elif poly_direction[poly_index][1]==1:
                            i=poly_direction[poly_index][0][-1]
                            poly_direction[poly_index][0].append((i+1)%(len(coords)))
                            i=(i+1)%(len(coords))
                            pp1=Point(coords[i][0],coords[i][1])
                        else:
                           i=poly_direction[poly_index][0][-1]
                           poly_direction[poly_index][0].append((i-1+len(coords))%(len(coords)))
                           i=(i-1+len(coords))%(len(coords))
                           pp1=Point(coords[i][0],coords[i][1])
                           
                    else:
                        poly=self.flow_graph.nfz_augm_list[poly_index]
                        #coords=list(poly.exterior.coords)[:-1]
                        #distance_list=[]
                        #for poly_p in coords:
                        #    d=(poly_p[0]-p_intermediate.x)*(poly_p[0]-p_intermediate.x)+(poly_p[1]-p_intermediate.y)*(poly_p[1]-p_intermediate.y)
  #                          distance_list.append(d)
  #                      min_d=min(distance_list)
  #                      i=distance_list.index(min_d)   
  #                      poly_direction[poly_index]=[[i],0]  
  #                      pp_tmp1=Point(list(poly.exterior.coords)[i][0],list(poly.exterior.coords)[i][1])

                        poly_intersection_points=[]
                     

                        #for i,p in enumerate(self.flow_graph.nfz_augm_list):
                        if 1:
                            p=poly
                            intersection_line=p.intersection(shapely_line)
                            if intersection_line.is_empty or intersection_line.geom_type=='Point':
                                continue
                           
                            if intersection_line.geom_type=='GeometryCollection':
                                intersection_line=intersection_line[0]
                            if intersection_line.geom_type=='MultiLineString':
                                points=[]
                                for l in intersection_line:
                                    for lp in list(l.coords):
                                        points.append(lp)
                            else:
                                try:
                                    points=list(intersection_line.coords)
                                except:
                                    print(intersection_line.geom_type)
                                for p_i in points:
                                    poly_intersection_points.append(p_i)
                        distance_list=[]
            
                        for p in poly_intersection_points:
                            d=(p[0]-pp1.x)*(p[0]-pp1.x)+(p[1]-pp1.y)*(p[1]-pp1.y)
                           
                            if d<0.5:
                                d=float("inf")
                            distance_list.append(d)
                        min_d=min(distance_list)
                      
                        i=distance_list.index(min_d)

                        closest_intersection_point=poly_intersection_points[i]
                       # print(closest_intersection_point)
              

            
                        transformer = Transformer.from_crs('epsg:32633','epsg:4326')  

                        p_tmp=transformer.transform(closest_intersection_point[0],closest_intersection_point[1])
            
                        route.append((p_tmp[1],p_tmp[0]))
                        turns.append(False)
                        edges_list.append((5999,6000))
                        next_turn_point.append((-999,-999))
                        groups.append(2000)
                        in_constrained.append(False)
                        turn_speed.append(5)

                      
                       
                        i,direction=get_neighbouring_poly_vertice_and_direction(poly,closest_intersection_point,pp2)
                        

                        pp_tmp1=Point(list(poly.exterior.coords)[i][0],list(poly.exterior.coords)[i][1])
                        
                        poly_direction[poly_index]=[[i],direction] 

                        pp1=pp_tmp1
                        

       
                    
                    transformer = Transformer.from_crs('epsg:32633','epsg:4326')  
                    p_tmp=transformer.transform(pp1.x,pp1.y)

                    #print(poly_index,pp1.x,pp1.y)
                    route.append((p_tmp[1],p_tmp[0]))
                    #print(route)
                    
                    turns.append(False)
                    edges_list.append((5999,6000))
                    next_turn_point.append((-999,-999))
                    groups.append(2000)
                    in_constrained.append(False)
                    turn_speed.append(0)
                    
                    ##Draw new line from current point to p2 
                    line = [(pp1.x,pp1.y), (pp2.x, pp2.y)]
                    shapely_line = LineString(line)

                    poly_intersection_points=[]
                    poly_indices=[]
                    for i,p in enumerate(self.flow_graph.nfz_list):
                        intersection_line=p.intersection(shapely_line)
                        if intersection_line.is_empty or intersection_line.geom_type=='Point':
                            continue
                     
                        if intersection_line.geom_type=='GeometryCollection':
                            intersection_line=intersection_line[0]  ##TODO: the new border nodes, still seem to intersect with the constrained, taht is a work around
                        if intersection_line.geom_type=='MultiLineString':
                            points=[]
                            for l in intersection_line:
                                for lp in list(l.coords):
                                    points.append(lp)
                        else:
                            try:
                                points=list(intersection_line.coords)
                            except:
                                print(intersection_line.geom_type)
                        for p_i in points:
                            poly_intersection_points.append(p_i)
                            poly_indices.append(i)
                           
                    if poly_indices==[]:
                        intersection=False
                        
                route.append((p2.x,p2.y))
                turns.append(True)
                edges_list.append((5999,6000))
                next_turn_point.append((-999,-999))
                groups.append(2000)
                in_constrained.append(False)
                turn_speed.append(5)

                    
            ##If path not only in ope
            #is going to entry point, draw line from current point to orig goal, find constrained intersection and update enrty/exit points #TODO
            elif entry:         
                ##Draw line from curent point to entry and if it intersects nfz repaet process #TODO
                a=1
            else:
                a=1
            
            
            
        
            ##At the end check for turns 
            ##Check for turn points
            lat_prev=p1.y
            lon_prev=p1.x
            turn_coords=[]

            for i in range(1,len(groups)-1):
                lat_cur=route[i][1]
                lon_cur=route[i][0]
                lat_next=route[i+1][1]
                lon_next=route[i+1][0]
                ##Check the angle between the prev point- current point and the current point- next point  

                d1=qdrdist(lat_prev,lon_prev,lat_cur,lon_cur)
                d2=qdrdist(lat_cur,lon_cur,lat_next,lon_next)
    
                angle=abs(d2[0]-d1[0])
                
                if angle>180:
                    angle=360-angle
    

                if angle>self.cutoff_angle:
                    turns[i]=True
                    tmp=(route[i][1],route[i][0])
                    turn_coords.append(tmp)
                    turn_speed[i]=15
            if not self.only_in_open and entry:
                turn_coords.append((self.start_point.x,self.start_point.y))
                
              
        return route,turns,edges_list,groups,in_constrained,turn_speed,rep
        
    
    ##Function to export the route based on the D* search graph
    ##Retruns: route,turns,next_node_index,turn_coord,groups
    ##route is the list of waypoints (lon,lat)
    ##turns is the list of booleans indicating for every waypoint if it is a turn
    ##next_node_index is the list of the next osmnx node for every waypoint
    ##turn_coord is a list containing the coord of every point that is a turn point
    ##groups_numbers is the list of the group in which each waypoint belongs to
    ##in_constrained is the list of booleans indicating for every waypoint if it is in constarined airspace
    ##turn_speed is teh list if speed to be used if the waypoint is a turning waypoint
    def get_path(self,path,graph,edges_speed, edges,edges_old=None,change=False,change_list=[]):

        route=[]
        next_node_index=[]
        group_numbers=[]
        turns=[]
        turn_coords=[]
 
        in_constrained=[] #list indicating in every waypoint is in constrained airspace (value=1) or in open airspace (value =0)
        
        path_found=True
        

        next_node_index.append(self.start_index)
        tmp=(self.start_point.x,self.start_point.y)
        group_numbers.append(graph.groups_list[path.start])
        route.append(tmp)
        turns.append(False)
        


        if 1 :    

            linestring=edges[self.start_index_previous][self.start_index].geometry
            coords = list(linestring.coords)

            
            
            d=float("inf")
            i=4000
            transformer = Transformer.from_crs('epsg:4326','epsg:32633')
            ps=transformer.transform(self.start_point.y,self.start_point.x)
            for c in range(len(coords)-1):
                transformer = Transformer.from_crs('epsg:4326','epsg:32633')
                p1=transformer.transform(coords[c][1],coords[c][0])
                p2=transformer.transform(coords[c+1][1],coords[c+1][0])
                p=find_closest_point_on_linesegment([p1,p2],ps)

                if distance_point(ps,p)<d:
                    d=distance_point(ps,p)
                    i=c
                    
            for c in range(len(coords)-1):
                if c>i:
                    tmp=(coords[c][0],coords[c][1]) #the points before the first node
                    route.append(tmp) 
                    group_numbers.append(graph.groups_list[path.start])
                    next_node_index.append(self.start_index)
                    turns.append(False)
                
            next_node_index.append(self.start_index)
            
            tmp=(self.flow_graph.nodes_graph[graph.key_indices_list[path.start]].lon,self.flow_graph.nodes_graph[graph.key_indices_list[path.start]].lat)
            group_numbers.append(graph.groups_list[path.start])
            route.append(tmp)
            turns.append(False)

        
        group=graph.groups_list[path.start]           

        
        selected_nodes_index=[]
        selected_nodes_index.append(path.start)


        while graph.key_indices_list[path.start]!=graph.key_indices_list[path.goal] :
            
    
            current_node=path.start
            minim=float('inf')
  
            for ch in graph.children_list[path.start]:
                if ch==65535:
                    break
               
                if compute_c(path.start, ch,edges_speed,self.flow_graph,path.speed,graph)+graph.g_list[ch]<minim:
                    minim=compute_c(path.start, ch,edges_speed,self.flow_graph,path.speed,graph)+graph.g_list[ch]
                    current_node=ch
                    
                    
            if current_node in selected_nodes_index:
                #print(selected_nodes_index)
                #print(current_node)
                #print("Path planning failed")
                #print("get_path stack !! Please report this!")
                return None,None,None,None,None,None,None,None
                
            selected_nodes_index.append(current_node)

            if graph.key_indices_list[current_node]!=graph.key_indices_list[path.start]:
                
                if 1:
                    #find the intermediate points
                    #pp=1
                    linestring=edges[graph.key_indices_list[path.start]][graph.key_indices_list[current_node]].geometry #if the start index should go first need to get checked
                    coords = list(linestring.coords)
                    for c in range(len(coords)-1):
                        if not c==0:
                            tmp=(coords[c][0],coords[c][1]) #the intermediate point
                            route.append(tmp) 
                            group_numbers.append(graph.groups_list[current_node])
                            next_node_index.append(graph.key_indices_list[current_node])
                            turns.append(False)

                if 1 :

                    next_node_index.append(graph.key_indices_list[current_node])
                    tmp=(self.flow_graph.nodes_graph[graph.key_indices_list[current_node]].lon,self.flow_graph.nodes_graph[graph.key_indices_list[current_node]].lat) #the next node
                    route.append(tmp)
                    
                    group_numbers.append(graph.groups_list[current_node])
                    turns.append(False) 

                
                
   
            path.start=current_node            

        if 1: 
    
            linestring=edges[self.goal_index][self.goal_index_next].geometry
            coords = list(linestring.coords)
            p0=self.flow_graph.nodes_graph[graph.key_indices_list[path.goal]].lon
            p1=self.flow_graph.nodes_graph[graph.key_indices_list[path.goal]].lat
            
            d=float("inf")
            i=0
            transformer = Transformer.from_crs('epsg:4326','epsg:32633')
            ps=transformer.transform(self.goal_point.y,self.goal_point.x)
            for c in range(len(coords)-1):
                p1=transformer.transform(coords[c][1],coords[c][0])
                p2=transformer.transform(coords[c+1][1],coords[c+1][0])
                p=find_closest_point_on_linesegment([p1,p2],ps)

                if distance_point(ps,p)<d:
                    d=distance_point(ps,p)
                    i=c            

            for c in range(1,len(coords)-1):
                if c<=i:
                     tmp=(coords[c][0],coords[c][1]) #the points before the first node
                     route.append(tmp) 
                     group_numbers.append(graph.groups_list[path.goal])
                     next_node_index.append(self.goal_index_next)
                     turns.append(False)

            tmp=(self.goal_point.x,self.goal_point.y)
            route.append(tmp)
            group_numbers.append(graph.groups_list[path.goal])
            next_node_index.append(self.goal_index_next)
            turns.append(False)   

        ##Check for turn points
        lat_prev=self.start_point.y
        lon_prev=self.start_point.x
        
        turn_speed=copy.deepcopy(turns)
        #speed set to 0 for open airspace or for no turn
        #speed to 10 knots for angles smaller than 45 degrees
        #speed to 5 knots for turning angles between 45 and 90 degrees
        #speed to 2 knots for turning angles larger tha 90 degrees


        for i in range(1,len(group_numbers)-1):
            lat_cur=route[i][1]
            lon_cur=route[i][0]
            lat_next=route[i+1][1]
            lon_next=route[i+1][0]
            ##Check the angle between the prev point- current point and the current point- next point  
            #line_string_1 = [(lat_prev,lon_prev), (lat_cur,lon_cur)]
            #line_string_2 = [(lat_cur,lon_cur), (lat_next,lon_next)]
            d1=qdrdist(lat_prev,lon_prev,lat_cur,lon_cur)
            d2=qdrdist(lat_cur,lon_cur,lat_next,lon_next)

            angle=abs(d2[0]-d1[0])
            
            if angle>180:
                angle=360-angle


            if angle>self.cutoff_angle  :
                turns[i]=True
                tmp=(route[i][1],route[i][0])
                turn_coords.append(tmp)
                if angle<100:
                    turn_speed[i]=10
                elif angle<150:
                    turn_speed[i]=5
                else:
                    turn_speed[i]=2


                
            lat_prev=lat_cur
            lon_prev=lon_cur
            if group_numbers[i]==group_numbers[i+1] :
                continue
            elif turns[i]!=True:
                turns[i]=True
                tmp=(route[i][1],route[i][0])
                turn_coords.append(tmp)
                if not turn_speed[i]:
                    turn_speed[i]=10

        turn_coords.append((-999,-999))
        turns[0]=False

        for g,i in enumerate(group_numbers):

            in_constrained.append(True)        


        init_groups=copy.deepcopy(group_numbers)
        return route,turns,next_node_index,turn_coords,group_numbers,in_constrained,turn_speed,init_groups
 
def point2linesegmentDistance(x1, y1, x2, y2, x3, y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    norm = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist = dx*dx + dy*dy

    return dist

def get_neighbouring_poly_vertice(poly,point):
    
    coords=list(poly.exterior.coords)[:-1]
    min_i=-1
    d=float("inf")
    for i in range(len(coords)):
        p1=coords[i]
        p2=coords[(i+1)%(len(coords))]
        dd=point2linesegmentDistance(p1[0],p1[1],p2[0],p2[1],point[0],point[1])
        if dd<d:
            min_i=i 
            d=dd
    if d>20:
        print("too large",d)
        #print(list(poly.exterior.coords))
    p1=coords[min_i]  
    p2=coords[(min_i+1)%(len(coords))]
    d1=(p1[0]-point[0])*(p1[0]-point[0])+(p1[1]-point[1])*(p1[1]-point[1])
    d2=(p2[0]-point[0])*(p2[0]-point[0])+(p2[1]-point[1])*(p2[1]-point[1])

    if d1<=d2:
        return min_i
    else:
        return (min_i+1)%(len(coords))

def get_neighbouring_poly_vertice_and_direction(poly,point,pp2):
    
    
    coords=list(poly.exterior.coords)[:-1]
    min_i=-1
    pp2_i=-1
    d_pp2=float("inf")
    d=float("inf")
    for i in range(len(coords)):
        p1=coords[i]
        p2=coords[(i+1)%(len(coords))]
        dd=point2linesegmentDistance(p1[0],p1[1],p2[0],p2[1],point[0],point[1])
    
        if dd<d:
            min_i=i 
            d=dd
        dd_pp2=(p1[0]-pp2.x)*(p1[0]-pp2.x)+(p1[1]-pp2.y)*(p1[1]-pp2.y)
        if dd_pp2<d_pp2:
            pp2_i=i 
            d_pp2=dd_pp2


    if d>20:
        print("too large",d)
        print(len(coords))
    p1=coords[min_i]  
    p2=coords[(min_i+1)%(len(coords))]
    d1=(p1[0]-point[0])*(p1[0]-point[0])+(p1[1]-point[1])*(p1[1]-point[1])
    d2=(p2[0]-point[0])*(p2[0]-point[0])+(p2[1]-point[1])*(p2[1]-point[1])

   # if d1>d2:
   #     min_i=(min_i+1)%(len(coords)-1)

    direction=0
    d1=0
    d2=0
    d3=0
    d4=0
    ii=min_i
    #print(ii,pp2_i,len(coords))
    while ii%(len(coords)) !=pp2_i:
        p1=coords[ii%(len(coords))]  
        p2=coords[(ii+1)%(len(coords))]
        d1+=(p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])
        ii+=1

    ii=(min_i+1)%(len(coords))
    while ii%(len(coords)) !=pp2_i:
        p1=coords[ii%(len(coords))]  
        p2=coords[(ii+1)%(len(coords))]
        d2+=(p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])
        ii+=1
    ii=min_i
    while (ii+len(coords)-1)%(len(coords)) !=pp2_i:
        p1=coords[(ii+len(coords)-1)%(len(coords))]  
        p2=coords[(ii+1)%(len(coords))]
        d3+=(p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])
        ii-=1

    ii=(min_i+1)%(len(coords))
    while (ii+len(coords)-1)%(len(coords)) !=pp2_i:
        p1=coords[(ii+len(coords)-1)%(len(coords))]  
        p2=coords[(ii+1)%(len(coords))]
        d4+=(p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])
        ii-=1
    if d1<=d2 and d1<=d3 and d1<=d4:
        direction=1
    elif d2<d1 and d2<=d3 and d2<=d4:
        min_i=(min_i+1)%(len(coords))
        direction=1
    elif d3<d1 and d3<d2 and d3<=d4:
        direction=-1
    else:
        min_i=(min_i+1)%(len(coords))
        direction=-1
    return min_i,direction
  

