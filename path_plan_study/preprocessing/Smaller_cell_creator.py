# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:30:57 2022

@author: nipat
"""

import osmnx as ox
import numpy as np
from plugins.streets.flow_control import street_graph,bbox
from plugins.streets.agent_path_planning import PathPlanning,Path
from plugins.streets.open_airspace_grid import Cell, open_airspace
import os
import dill
import json
import sys
from pympler import asizeof
import geopandas
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
from pyproj import  Transformer
import shapely.geometry 
import copy



#Load the open airspace grid
input_file=open("open_airspace_final.dill", 'rb')
#input_file=open("open_airspace_grid_updated.dill", 'rb')##for 3d path planning
grid=dill.load(input_file)

##################
##Update cells borders
grid_list=[]
tmp_grid_list=[]
for i in range(len(grid.grid)):
    p=grid.grid[i]
    if i==139 or i==216:
        continue
    if i>218:

        continue
    if p.p0[0]==p.p1[0] and  p.p2[0]==p.p3[0] :
        a=p.p0[1]-p.p1[1]
        b=p.p3[1]-p.p2[1]
        width=p.p0[0]-p.p2[0]
        w_rep=math.ceil(width/1000)
        w_const=width/w_rep

        for k in range(w_rep):
                
                c=Cell()
                
                x0=p.p2[0]+(k+1)*w_const
                x1=p.p2[0]+(k+1)*w_const
                x2=p.p2[0]+k*w_const
                x3=p.p2[0]+k*w_const
                
                if p.p1[1]!=p.p2[1]:
                    a2=(p.p1[1]-p.p2[1])/(p.p1[0]-p.p2[0])
                    b2=p.p1[1]-a2*p.p1[0]
                    
                    y1=a2*x1+b2
                    y2=a2*x2+b2
                else:
                    y1=p.p1[1]
                    y2=p.p2[1]
                    
                if p.p0[1]!=p.p3[1]: 
                    a1=(p.p0[1]-p.p3[1])/(p.p0[0]-p.p3[0])
                    b1=p.p0[1]-a1*p.p0[0]
    
                    y0=a1*x0+b1
                    y3=a1*x3+b1
                else:
                    y0=p.p0[1]
                    y3=p.p3[1]
                
                c.p0=[x0,y0]
                c.p1=[x1,y1]
                c.p2=[x2,y2]
                c.p3=[x3,y3]
                c.entry_list=p.entry_list
                c.exit_list=p.exit_list
                c.neighbors=p.neighbors
                c.key_index=p.key_index

                tmp_grid_list.append(c)
        
new_cells_ids=4481
for i in range(len(tmp_grid_list)):
    p=tmp_grid_list[i]

    if p.p0[0]==p.p1[0] and  p.p2[0]==p.p3[0]:
        a=p.p0[1]-p.p1[1]
        b=p.p3[1]-p.p2[1]

        c=min(a,b)
        rep=math.ceil(c/500)
        r_const=a/rep
        l_const=b/rep

        for j in range(rep):
                
            c=Cell()
            c.id=p.key_index
            c.key_index=new_cells_ids
                
            y0=min(p.p1[1]+(j+1)*r_const,p.p0[1])
            y1=p.p1[1]+r_const*j
            y2=p.p2[1]+l_const*j
            y3=min(p.p2[1]+(j+1)*l_const,p.p3[1])
                
            c.p0=[p.p0[0],y0]
            c.p1=[p.p1[0],y1]
            c.p2=[p.p2[0],y2]
            c.p3=[p.p3[0],y3]
            c.center_x=(c.p0[0]+c.p1[0])/2
            c.center_y=(c.p0[1]+c.p1[1]+c.p2[1]+c.p3[1])/4
            c.entry_list=copy.deepcopy(p.entry_list)
            c.exit_list=copy.deepcopy(p.exit_list)
            c.neighbors=copy.deepcopy(p.neighbors)
                
            new_cells_ids=new_cells_ids+1
            grid_list.append(c)
            
for i in range(len(grid.grid)):
    p=grid.grid[i]

    if i>218:
        c=copy.deepcopy(p)
        
        c.id=c.key_index
        c.key_index=new_cells_ids
        grid_list.append(c)
        new_cells_ids=new_cells_ids+1
        continue        

######

########
##Load exit and entry points
entry_points_list_old=[]
exit_points_list_old=[]
entry_points_list=[]
exit_points_list=[]
entry_nodes_dict={}
exit_nodes_dict={}
G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')
        
f = open('airspace_design/entries.txt','r')      
contents = f.read()
f.close()
entry_points_list_old=[int(x) for x in contents.split(",")]
         
f = open('airspace_design/exits.txt','r')
contents = f.read()
f.close()
exit_points_list_old=[int(x) for x in contents.split(",")] 


##Convert to updated node keys
with open('whole_vienna/gis/old_to_new_nodes.json', 'r') as filename:
    old2new_nodes_dict = json.load(filename)
    
for i in  entry_points_list_old:
    entry_points_list.append(old2new_nodes_dict[str(i)])           
for i in  exit_points_list_old:
    exit_points_list.append(old2new_nodes_dict[str(i)])       
    
#Compute node coords in cartesian and save them 
transformer = Transformer.from_crs('epsg:4326','epsg:32633')   
         
for index in entry_points_list:
    lon=G._node[index]['x']
    lat=G._node[index]['y']
    p=transformer.transform(lat,lon)
    entry_nodes_dict[index]=[p[0],p[1]]
             
for index in exit_points_list:
    lon=G._node[index]['x']
    lat=G._node[index]['y']
    p=transformer.transform(lat,lon)
    exit_nodes_dict[index]=[p[0],p[1]]


entry_cells_dict={}
exit_cells_dict={}
for i in range(len(grid_list)):
    p=grid_list[i]
    if p.entry_list==[] and p.exit_list==[]:
        continue
    for v in p.entry_list:
        if v in entry_cells_dict.keys():
            entry_cells_dict[v].append(p.key_index)
        else:
            entry_cells_dict[v]=[p.key_index]
    for v in p.exit_list:
        if v in exit_cells_dict.keys():
            exit_cells_dict[v].append(p.key_index)
        else:
            exit_cells_dict[v]=[p.key_index]
########


#########
##Update cells enrty and exit points
def distance_to_line(A, B, E) :
    if A==B:
        return(math.sqrt( (A[0]-E[0])*(A[0]-E[0])+(A[1]-E[1])*(A[1]-E[1])))
    # vector AB
    AB = [None, None]
    AB[0] = B[0] - A[0]
    AB[1] = B[1] - A[1]
 
    # vector BP
    BE = [None, None]
    BE[0] = E[0] - B[0]
    BE[1] = E[1] - B[1]
 
    # vector AP
    AE = [None, None];
    AE[0] = E[0] - A[0]
    AE[1] = E[1] - A[1]
 
    # Variables to store dot product
 
    # Calculating the dot product
    AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1]
 
    # Minimum distance from
    # point E to the line segment
    reqAns = 0
 
    # Case 1
    if (AB_BE > 0) :
 
        # Finding the magnitude
        y = E[1] - B[1]
        x = E[0] - B[0]
        reqAns = math.sqrt(x * x + y * y)

    # Case 2
    elif (AB_AE < 0) :
        y = E[1] - A[1]
        x = E[0] - A[0]
        reqAns = math.sqrt(x * x + y * y)
 
    # Case 3
    else:
 
        # Finding the perpendicular distance
        x1 = AB[0]
        y1 = AB[1]
        x2 = AE[0]
        y2 = AE[1]
        mod = math.sqrt(x1 * x1 + y1 * y1)
        reqAns = abs(x1 * y2 - y1 * x2) / mod
     
    return reqAns

def find_closest_cell(cells,p):
    cell_id=-1
    dist=float("inf")
    index=-1
    for i,cc in enumerate(cells):
        c=grid_list[cc-4481]
        d1=distance_to_line(c.p0, c.p1, p) 
        d2=distance_to_line(c.p1, c.p2, p) 
        d3=distance_to_line(c.p2, c.p3, p) 
        d4=distance_to_line(c.p0, c.p3, p) 
        dd=min(d1,d2,d3,d4)
        if dd<dist:
            dist=dd
            cell_id=c.key_index
            index=i
    
    return cell_id,index

for v in entry_cells_dict.keys():
    if len(entry_cells_dict[v])==1:
        continue
        
    point = shapely.geometry.Point(entry_nodes_dict[v][0],entry_nodes_dict[v][1])
    tmp_cell_list=[]
    for c in entry_cells_dict[v]:
       p=grid_list[c-4481]
       p0=(p.p0[0],p.p0[1])
       p1=(p.p1[0],p.p1[1])
       p2=(p.p2[0],p.p2[1])
       p3=(p.p3[0],p.p3[1])
       polygon = shapely.geometry.Polygon([p0, p1,p2,p3])
       if polygon.contains(point):
           tmp_cell_list.append(c)
           
    if len(tmp_cell_list)==1:
        for c in entry_cells_dict[v]:
            if c in tmp_cell_list:
                continue
            grid_list[c-4481].entry_list.remove(v)
            
        entry_cells_dict[v]=[tmp_cell_list[0]]

    elif len(tmp_cell_list)>1:
        print(v)
    else:
        ##the nearest cells has to be found
        cell_id,index=find_closest_cell(entry_cells_dict[v],[point.x,point.y])
        for c in entry_cells_dict[v]:
            if c==cell_id:
                continue
            grid_list[c-4481].entry_list.remove(v)
            
        entry_cells_dict[v]=[cell_id]

for v in exit_cells_dict.keys():
    if len(exit_cells_dict[v])==1:
        continue
        
    point = shapely.geometry.Point(exit_nodes_dict[v][0],exit_nodes_dict[v][1])
    tmp_cell_list=[]
    for c in exit_cells_dict[v]:
       p=grid_list[c-4481]
       p0=(p.p0[0],p.p0[1])
       p1=(p.p1[0],p.p1[1])
       p2=(p.p2[0],p.p2[1])
       p3=(p.p3[0],p.p3[1])
       polygon = shapely.geometry.Polygon([p0, p1,p2,p3])
       if polygon.contains(point):
           tmp_cell_list.append(c)
           
    if len(tmp_cell_list)==1:
        for c in exit_cells_dict[v]:
            if c in tmp_cell_list:
                continue
            grid_list[c-4481].exit_list.remove(v)
            
        exit_cells_dict[v]=[tmp_cell_list[0]]
    elif len(tmp_cell_list)>1:
        print(v)
    else:
        cell_id,index=find_closest_cell(exit_cells_dict[v],[point.x,point.y])
        for c in exit_cells_dict[v]:
            if c==cell_id:
                continue
            grid_list[c-4481].exit_list.remove(v)
            
        exit_cells_dict[v]=[cell_id]
    

#############

#########
##Update neighbors
old2new_cells_dict={}
for i in grid_list:
    if i.id in old2new_cells_dict.keys():
        old2new_cells_dict[i.id].append(i.key_index)
    else:
        old2new_cells_dict[i.id]=[i.key_index]

for i in grid_list:
    if i.p1[0]==i.p0[0]:
        h_a1=None
        v_a1=i.p1[0]
    else:
        h_a1=(i.p1[1]-i.p0[1])/(i.p1[0]-i.p0[0])
        v_a1=i.p1[1]-h_a1*i.p1[0]
        h_a1=round(h_a1,6)
    if i.p1[0]==i.p2[0]:
        h_b1=None
        v_b1=i.p1[0]
    else:
        h_b1=(i.p2[1]-i.p1[1])/(i.p2[0]-i.p1[0])
        v_b1=i.p1[1]-h_b1*i.p1[0]
        h_b1=round(h_b1,6)
    if i.p2[0]==i.p3[0]:
        h_c1=None
        v_c1=i.p2[0]
    else:
        h_c1=(i.p3[1]-i.p2[1])/(i.p3[0]-i.p2[0])
        v_c1=i.p2[1]-h_c1*i.p2[0]
        h_c1=round(h_c1,6)
    if i.p3[0]==i.p0[0]:
        h_d1=None
        v_d1=i.p3[0]
    else:
        h_d1=(i.p0[1]-i.p3[1])/(i.p0[0]-i.p3[0])
        v_d1=i.p3[1]-h_d1*i.p3[0]
        h_d1=round(h_d1,6)  
        
    v_a1=round(v_a1,2)
    v_b1=round(v_b1,2)
    v_c1=round(v_c1,2)
    v_d1=round(v_d1,2) 
    
    possible_neig=copy.deepcopy(old2new_cells_dict[i.id])
    possible_neig.remove(i.key_index)
    
    for n in i.neighbors:
        possible_neig=possible_neig+old2new_cells_dict[n]

    i.neighbors=[]
    for n in possible_neig:
        #check if it is neighboring
        nn=grid_list[n-4481]
        if nn.p1[0]==nn.p0[0]:
            h_a2=None
            v_a2=nn.p1[0]
        else:
            h_a2=(nn.p1[1]-nn.p0[1])/(nn.p1[0]-nn.p0[0])
            v_a2=nn.p1[1]-h_a2*nn.p1[0]
            h_a2=round(h_a2,6)
        if nn.p1[0]==nn.p2[0]:
            h_b2=None
            v_b2=nn.p1[0]
        else:
            h_b2=(nn.p2[1]-nn.p1[1])/(nn.p2[0]-nn.p1[0])
            v_b2=nn.p1[1]-h_b2*nn.p1[0]
            h_b2=round(h_b2,6)
        if nn.p2[0]==nn.p3[0]:
            h_c2=None
            v_c2=nn.p2[0]
        else:
            h_c2=(nn.p3[1]-nn.p2[1])/(nn.p3[0]-nn.p2[0])
            v_c2=nn.p2[1]-h_c2*nn.p2[0]
            h_c2=round(h_c2,6)
        if nn.p3[0]==nn.p0[0]:
            h_d2=None
            v_d2=nn.p3[0]
        else:
            h_d2=(nn.p0[1]-nn.p3[1])/(nn.p0[0]-nn.p3[0])
            v_d2=nn.p3[1]-h_d2*nn.p3[0]
            h_d2=round(h_d2,6)  
            
       
        v_a2=round(v_a2,2)
        v_b2=round(v_b2,2)
        v_c2=round(v_c2,2)
        v_d2=round(v_d2,2) 
        
        neigh_bool=False

        
        if h_a1==h_c2 and v_a1==v_c2:
            if i.p0[1]>= i.p1[1]:
                if i.p0[1]>= nn.p3[1] >= i.p1[1] or i.p0[1]>= nn.p2[1] >= i.p1[1] :
                    neigh_bool=True
            else:
                if i.p0[1]<= nn.p3[1] <= i.p1[1] or i.p0[1]<= nn.p2[1] <= i.p1[1] :
                    neigh_bool=True  
            if nn.p3[1]>= nn.p2[1]:
                if  nn.p3[1]>= i.p0[1] >= nn.p2[1] or nn.p3[1]>= i.p1[1] >= nn.p2[1]:
                    neigh_bool=True
            else:
                if  nn.p3[1]<= i.p0[1] <= nn.p2[1] or nn.p3[1]<= i.p1[1] <= nn.p2[1]:
                    neigh_bool=True                     
        if h_a1==h_b2 and v_a1==v_b2:
            if i.p0[1]>= i.p1[1]:
                if i.p0[1]>= nn.p1[1] >= i.p1[1] or i.p0[1]>= nn.p2[1] >= i.p1[1] :
                    neigh_bool=True
            else:
                if i.p0[1]<= nn.p1[1] <= i.p1[1] or i.p0[1]<= nn.p2[1] <= i.p1[1] :
                    neigh_bool=True  
            if nn.p1[1]>= nn.p2[1]:
                if  nn.p1[1]>= i.p0[1] >= nn.p2[1] or nn.p1[1]>= i.p1[1] >= nn.p2[1]:
                    neigh_bool=True
            else:
                if  nn.p1[1]<= i.p0[1] <= nn.p2[1] or nn.p1[1]<= i.p1[1] <= nn.p2[1]:
                    neigh_bool=True   
        if h_a1==h_d2 and v_a1==v_d2:
            if i.p0[1]>= i.p1[1]:
                if i.p0[1]>= nn.p3[1] >= i.p1[1] or i.p0[1]>= nn.p0[1] >= i.p1[1] :
                    neigh_bool=True
            else:
                if i.p0[1]<= nn.p3[1] <= i.p1[1] or i.p0[1]<= nn.p0[1] <= i.p1[1] :
                    neigh_bool=True  
            if nn.p3[1]>= nn.p0[1]:
                if  nn.p3[1]>= i.p0[1] >= nn.p0[1] or nn.p3[1]>= i.p1[1] >= nn.p0[1]:
                    neigh_bool=True
            else:
                if  nn.p3[1]<= i.p0[1] <= nn.p0[1] or nn.p3[1]<= i.p1[1] <= nn.p0[1]:
                    neigh_bool=True                           
        if h_c1==h_a2 and v_c1==v_a2:
            if i.p3[1]>= i.p2[1]:
                if i.p3[1]>= nn.p0[1] >= i.p2[1] or i.p3[1]>= nn.p1[1] >= i.p2[1] :
                    neigh_bool=True
            else:
                if i.p3[1]<= nn.p0[1] <= i.p2[1] or i.p3[1]<= nn.p1[1] <= i.p2[1] :
                    neigh_bool=True  
            if nn.p0[1]>= nn.p1[1]:
                if  nn.p0[1]>= i.p2[1] >= nn.p1[1] or nn.p0[1]>= i.p3[1] >= nn.p1[1]:
                    neigh_bool=True
            else:
                if  nn.p0[1]<= i.p2[1] <= nn.p1[1] or nn.p0[1]<= i.p3[1] <= nn.p1[1]:
                    neigh_bool=True   
        if h_c1==h_b2 and v_c1==v_b2:
            if i.p3[1]>= i.p2[1]:
                if i.p3[1]>= nn.p2[1] >= i.p2[1] or i.p3[1]>= nn.p1[1] >= i.p2[1] :
                    neigh_bool=True
            else:
                if i.p3[1]<= nn.p2[1] <= i.p2[1] or i.p3[1]<= nn.p1[1] <= i.p2[1] :
                    neigh_bool=True  
            if nn.p2[1]>= nn.p1[1]:
                if  nn.p2[1]>= i.p2[1] >= nn.p1[1] or nn.p2[1]>= i.p3[1] >= nn.p1[1]:
                    neigh_bool=True
            else:
                if  nn.p2[1]<= i.p2[1] <= nn.p1[1] or nn.p2[1]<= i.p3[1] <= nn.p1[1]:
                    neigh_bool=True  
        if h_c1==h_d2 and v_c1==v_d2:
            if i.p3[1]>= i.p2[1]:
                if i.p3[1]>= nn.p0[1] >= i.p2[1] or i.p3[1]>= nn.p3[1] >= i.p2[1] :
                    neigh_bool=True
            else:
                if i.p3[1]<= nn.p0[1] <= i.p2[1] or i.p3[1]<= nn.p3[1] <= i.p2[1] :
                    neigh_bool=True  
            if nn.p0[1]>= nn.p3[1]:
                if  nn.p0[1]>= i.p2[1] >= nn.p3[1] or nn.p0[1]>= i.p3[1] >= nn.p3[1]:
                    neigh_bool=True
            else:
                if  nn.p0[1]<= i.p2[1] <= nn.p3[1] or nn.p0[1]<= i.p3[1] <= nn.p3[1]:
                    neigh_bool=True                       
        if h_b1==h_a2 and v_b1==v_a2:
            if i.p1[1]>= i.p2[1]:
                if i.p1[1]>= nn.p0[1] >= i.p2[1] or i.p1[1]>= nn.p1[1] >= i.p2[1] :
                    neigh_bool=True
            else:
                if i.p1[1]<= nn.p0[1] <= i.p2[1] or i.p1[1]<= nn.p1[1] <= i.p2[1] :
                    neigh_bool=True  
            if nn.p0[1]>= nn.p1[1]:
                if  nn.p0[1]>= i.p2[1] >= nn.p1[1] or nn.p0[1]>= i.p1[1] >= nn.p1[1]:
                    neigh_bool=True
            else:
                if  nn.p0[1]<= i.p2[1] <= nn.p1[1] or nn.p0[1]<= i.p1[1] <= nn.p1[1]:
                    neigh_bool=True   
        if h_d1==h_a2 and v_d1==v_a2:
            if i.p3[1]>= i.p0[1]:
                if i.p3[1]>= nn.p0[1] >= i.p0[1] or i.p3[1]>= nn.p1[1] >= i.p0[1] :
                    neigh_bool=True
            else:
                if i.p3[1]<= nn.p0[1] <= i.p0[1] or i.p3[1]<= nn.p1[1] <= i.p0[1] :
                    neigh_bool=True  
            if nn.p0[1]>= nn.p1[1]:
                if  nn.p0[1]>= i.p0[1] >= nn.p1[1] or nn.p0[1]>= i.p3[1] >= nn.p1[1]:
                    neigh_bool=True
            else:
                if  nn.p0[1]<= i.p0[1] <= nn.p1[1] or nn.p0[1]<= i.p3[1] <= nn.p1[1]:
                    neigh_bool=True                        
        if h_d1==h_b2 and v_d1==v_b2:
            if i.p0[1]>= i.p3[1]:
                if i.p0[1]>= nn.p2[1] >= i.p3[1] or i.p0[1]>= nn.p1[1] >= i.p3[1] :
                    neigh_bool=True
            else:
                if i.p0[1]<= nn.p2[1] <= i.p3[1] or i.p0[1]<= nn.p1[1] <= i.p3[1] :
                    neigh_bool=True  
            if nn.p2[1]>= nn.p1[1]:
                if  nn.p2[1]>= i.p0[1] >= nn.p1[1] or nn.p2[1]>= i.p3[1] >= nn.p1[1]:
                    neigh_bool=True
            else:
                if  nn.p2[1]<= i.p0[1] <= nn.p1[1] or nn.p2[1]<= i.p3[1] <= nn.p1[1]:
                    neigh_bool=True   
        if h_d1==h_c2 and v_d1==v_c2:
            if i.p3[1]>= i.p0[1]:
                if i.p3[1]>= nn.p2[1] >= i.p0[1] or i.p3[1]>= nn.p3[1] >= i.p0[1] :
                    neigh_bool=True
            else:
                if i.p3[1]<= nn.p2[1] <= i.p0[1] or i.p3[1]<= nn.p3[1] <= i.p0[1] :
                    neigh_bool=True  
            if nn.p2[1]>= nn.p3[1]:
                if  nn.p2[1]>= i.p3[1] >= nn.p3[1] or nn.p2[1]>= i.p0[1] >= nn.p3[1]:
                    neigh_bool=True
            else:
                if  nn.p2[1]<= i.p3[1] <= nn.p3[1] or nn.p2[1]<= i.p0[1] <= nn.p3[1]:
                    neigh_bool=True                           
        if h_b1==h_d2 and v_b1==v_d2:
            if i.p1[1]>= i.p2[1]:
                if i.p1[1]>= nn.p0[1] >= i.p2[1] or i.p1[1]>= nn.p3[1] >= i.p2[1] :
                    neigh_bool=True
            else:
                if i.p1[1]<= nn.p0[1] <= i.p2[1] or i.p1[1]<= nn.p3[1] <= i.p2[1] :
                    neigh_bool=True  
            if nn.p0[1]>= nn.p3[1]:
                if  nn.p0[1]>= i.p2[1] >= nn.p3[1] or nn.p0[1]>= i.p1[1] >= nn.p3[1]:
                    neigh_bool=True
            else:
                if  nn.p0[1]<= i.p2[1] <= nn.p3[1] or nn.p0[1]<= i.p1[1] <= nn.p3[1]:
                    neigh_bool=True  
        if h_b1==h_c2 and v_b1==v_c2:
            if i.p1[1]>= i.p2[1]:
                if i.p1[1]>= nn.p3[1] >= i.p2[1] or i.p1[1]>= nn.p2[1] >= i.p2[1] :
                    neigh_bool=True
            else:
                if i.p1[1]<= nn.p3[1] <= i.p2[1] or i.p1[1]<= nn.p2[1] <= i.p2[1] :
                    neigh_bool=True  
            if nn.p3[1]>= nn.p2[1]:
                if  nn.p3[1]>= i.p2[1] >= nn.p2[1] or nn.p3[1]>= i.p1[1] >= nn.p2[1]:
                    neigh_bool=True
            else:
                if  nn.p3[1]<= i.p2[1] <= nn.p2[1] or nn.p3[1]<= i.p1[1] <= nn.p2[1]:
                    neigh_bool=True              

        if neigh_bool:
            i.neighbors.append(n)
            
    if i.neighbors==[]:
        print(i.key_index)

##########



fig, ax = plt.subplots(1,1)
plt.ylim([5330000,5350000])
plt.xlim([593000,609000])


for i in range(len(grid.grid)):
    p=grid.grid[i]

    y = np.array([[p.p0[0], p.p0[1]], [p.p1[0], p.p1[1]], [p.p2[0] ,p.p2[1]], [p.p3[0], p.p3[1]]])

    pol = Polygon(y, facecolor = "none",edgecolor="b")

    ax.add_patch(pol)
    
for i in range(len(grid_list)):
    p=grid_list[i]

    y = np.array([[p.p0[0], p.p0[1]], [p.p1[0], p.p1[1]], [p.p2[0] ,p.p2[1]], [p.p3[0], p.p3[1]]])

    pol = Polygon(y, facecolor = "none",edgecolor="r")


    ax.add_patch(pol) 
    
grid.grid=grid_list
    
##Dill the new grid
# =============================================================================
# output_file=open("smaller_cells_open_airspace_grid.dill", 'wb')
# dill.dump(grid,output_file)
# output_file.close()
# =============================================================================

# =============================================================================
# exit_nodes_in_use=[]
# for i in exit_cells_dict.keys():
#     exit_nodes_in_use.append(i)
# 
# entry_nodes_in_use=[]
# for i in entry_cells_dict.keys():
#     entry_nodes_in_use.append(i)    
# 
# output_file=open("entry_nodes.dill", 'wb')
# dill.dump(entry_nodes_in_use,output_file)
# output_file.close()
# 
# output_file=open("exit_nodes.dill", 'wb')
# dill.dump(exit_nodes_in_use,output_file)
# output_file.close()
# =============================================================================
