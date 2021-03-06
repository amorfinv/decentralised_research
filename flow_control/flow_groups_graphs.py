# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:50:17 2022

@author: nipat
"""

import json
import dill
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.patches import PathPatch
import matplotlib
import matplotlib.colors as mc
import colorsys
import math
import numpy as np


with open('grid_sectors/flows.json', 'r') as filename:
    grid_flows_dict = json.load(filename)
    
with open('grid_sectors/flow_length.json', 'r') as filename:
    grid_flows_lengths= json.load(filename)
    
    
with open('cluster_sectors/flows.json', 'r') as filename:
    cluster_flows_dict = json.load(filename)
    
with open('cluster_sectors/flow_length.json', 'r') as filename:
    cluster_flows_lengths= json.load(filename)
    
with open('airspace_design/flows.json', 'r') as filename:
    orig_flows_dict = json.load(filename)
    
with open('airspace_design/flow_length.json', 'r') as filename:
    orig_flows_lengths= json.load(filename)
    
with open('clusters_5/flows.json', 'r') as filename:
    cluster2_flows_dict = json.load(filename)
    
with open('clusters_5/flow_length.json', 'r') as filename:
    cluster2_flows_lengths= json.load(filename)
    
grid_flows={}
grid_flows["Strokes"]=[] 
grid_flows["Length"]=[] 
grid_flows["Group"]=[] 
for k in grid_flows_dict.keys():
    grid_flows["Group"].append(k)
    grid_flows["Strokes"].append(len(grid_flows_dict[k]))
    grid_flows["Length"].append(grid_flows_lengths[k])
    

cluster_flows={}
cluster_flows["Strokes"]=[] 
cluster_flows["Length"]=[] 
cluster_flows["Group"]=[]     
for k in cluster_flows_dict.keys():
    cluster_flows["Group"].append(k)
    cluster_flows["Strokes"].append(len(cluster_flows_dict[k]))
    cluster_flows["Length"].append(cluster_flows_lengths[k])

cluster2_flows={}
cluster2_flows["Strokes"]=[] 
cluster2_flows["Length"]=[] 
cluster2_flows["Group"]=[]     
for k in cluster2_flows_dict.keys():
    cluster2_flows["Group"].append(k)
    cluster2_flows["Strokes"].append(len(cluster2_flows_dict[k]))
    cluster2_flows["Length"].append(cluster2_flows_lengths[k])

orig_flows={}
orig_flows["Strokes"]=[] 
orig_flows["Length"]=[] 
orig_flows["Group"]=[]       
for k in orig_flows_dict.keys():
    if k=="0":
        continue
    orig_flows["Group"].append(k)
    orig_flows["Strokes"].append(len(orig_flows_dict[k]))
    orig_flows["Length"].append(orig_flows_lengths[k])
    
    
grid_flows_dataframe = pd.DataFrame.from_dict(grid_flows)
grid_flows_dataframe["Flow"]="Grid"

print("Grid sectors has # flow grousp", grid_flows_dataframe.shape[0])

print("Grid sectors max leght", grid_flows_dataframe["Length"].max())
print("Grid sectors min leght", grid_flows_dataframe["Length"].min())
print("Grid sectors mean leght", grid_flows_dataframe["Length"].mean())

print("#################")

cluster_flows_dataframe = pd.DataFrame.from_dict(cluster_flows)
cluster_flows_dataframe["Flow"]="Clusters1"

print("Clustersectors has # flow grousp", cluster_flows_dataframe.shape[0])

print("Grid sectors max leght", cluster_flows_dataframe["Length"].max())
print("Grid sectors min leght", cluster_flows_dataframe["Length"].min())
print("Grid sectors mean leght", cluster_flows_dataframe["Length"].mean())
print("#################")

cluster2_flows_dataframe = pd.DataFrame.from_dict(cluster2_flows)
cluster2_flows_dataframe["Flow"]="Clusters2"

print("Cluster 2 sectors has # flow grousp", cluster2_flows_dataframe.shape[0])

print("Grid sectors max leght", cluster2_flows_dataframe["Length"].max())
print("Grid sectors min leght", cluster2_flows_dataframe["Length"].min())
print("Grid sectors mean leght", cluster2_flows_dataframe["Length"].mean())
print("#################")

orig_flows_dataframe = pd.DataFrame.from_dict(orig_flows)
orig_flows_dataframe["Flow"]="Original"

print("Orig sectors has # flow grousp", orig_flows_dataframe.shape[0])

print("Grid sectors max leght", orig_flows_dataframe["Length"].max())
print("Grid sectors min leght", orig_flows_dataframe["Length"].min())
print("Grid sectors mean leght", orig_flows_dataframe["Length"].mean())

frames=[orig_flows_dataframe,grid_flows_dataframe,cluster_flows_dataframe,cluster2_flows_dataframe]

flows_df=pd.concat(frames)


fig=plt.figure()
sns.boxplot(y="Length", x='Flow', data=flows_df).set(title="Length of flow groups",ylabel="Length (m)", xlabel=" Flow control method")

#plt.ylim(0, 40000)
plt.show()

fig=plt.figure()
sns.boxplot(y="Strokes", x='Flow', data=flows_df).set(title="Number of street edges in each flow group",ylabel="Number of street edges", xlabel=" Flow control method")

#plt.ylim(0, 40000)
plt.show()



