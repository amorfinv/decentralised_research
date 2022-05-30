# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 17:00:22 2021

@author: nipat
"""
import osmnx as ox
import numpy as np
from plugins.streets.flow_control_geom import street_graph,bbox
from plugins.streets.agent_path_planning_geometric import PathPlanning,Path
from plugins.streets.open_airspace_grid import Cell, open_airspace
import math
import dill
from pyproj import  Transformer

import matplotlib.pyplot as plt


import matplotlib.patches as patches

from matplotlib.patches import Polygon

import shapely.geometry

# Step 1: Import the graph we will be using

G = ox.io.load_graphml('whole_vienna/gis/finalized_graph.graphml')

edges = ox.graph_to_gdfs(G)[1]
gdf=ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
print('Graph loaded!')


#Load the open airspace grid
#input_file=open("smaller_cells_open_airspace_grid.dill", 'rb')
input_file=open("open_airspace_final.dill", 'rb')
grid=dill.load(input_file)



##Initialise the flow control entity
#input_file=open("Flow_control.dill", 'rb')
graph=street_graph(G,edges) 

fig, ax = ox.plot_graph(G,node_color="w",show=False,close=False)
ax.set_xlim([16.2,16.6])
ax.set_ylim([48.1,48.3])

#ax.scatter(16.3848463 ,48.1611501,c="g")#enrty


l=[(16.4025272687, 48.2489357246), (16.385040612869595, 48.24299456513938), (16.3848187, 48.2428926), (16.3848187, 48.2428926), (16.3838909, 48.2424695), (16.3830468, 48.24207619999999), (16.3829226, 48.2420223), (16.3817212, 48.2414753), (16.3795202, 48.24352059999998), (16.3794278, 48.2435838), (16.3791838, 48.2436044), (16.3790793, 48.2435919), (16.3784985, 48.242478), (16.3779055, 48.2413307), (16.3776637, 48.24139029999998), (16.3773682, 48.2416819), (16.3764433, 48.2412424), (16.3753281, 48.2407353), (16.3748448, 48.24144860000001), (16.3747542, 48.2416676), (16.3743505, 48.24226509999998), (16.3742447, 48.2423574), (16.3741647, 48.24242729999999), (16.3739293, 48.2425295), (16.3738329, 48.24254499999999), (16.3736457, 48.2425555), (16.3729895, 48.24255469999999), (16.3727268, 48.2425859), (16.3722957, 48.2426895), (16.3705134, 48.243415), (16.368465, 48.24423079999999), (16.3683463, 48.24430569999998), (16.3680185, 48.2444392), (16.3671775, 48.2447828), (16.3668603, 48.2448973), (16.366196, 48.24506079999998), (16.3652332, 48.2452216), (16.3649257, 48.2452418), (16.3632706, 48.24518359999999), (16.3628365, 48.24506229999999), (16.361834, 48.24471489999999), (16.361626, 48.2446818), (16.3616138, 48.24455859999999), (16.3615689, 48.2442322), (16.3611045, 48.24187349999998), (16.3609813, 48.24154189999998), (16.3579569, 48.2378988), (16.3570932, 48.2365876), (16.356806, 48.2361698), (16.3566763, 48.2358588), (16.3559791, 48.23315719999999), (16.3559885, 48.232958), (16.3560025, 48.2328023), (16.3556573, 48.23263439999999), (16.3550753, 48.23212999999998), (16.3543076, 48.2317555), (16.3527308, 48.2311253), (16.3515756, 48.2306766), (16.3510711, 48.23044779999999), (16.3510144, 48.23039549999999), (16.3509667, 48.23027889999999), (16.350864, 48.2297832), (16.3507009, 48.2291142), (16.3499329, 48.2291913), (16.349151, 48.2292683), (16.3474717, 48.2294453), (16.3457306, 48.2297782), (16.3454804, 48.22984089999999), (16.3447664, 48.2299932), (16.3447664, 48.2299932), (16.2904039177, 48.2155788659), (16.31831264812734, 48.23906237455595), (16.322811333732698, 48.23752032908), (16.32290685896084, 48.237493374368945), (16.322994524579915, 48.23746871215656), (16.322996809595423, 48.23746806102681), (16.323431310716522, 48.23734266061615), (16.32343328322492, 48.237342085070324), (16.323694842875618, 48.23726493289375), (16.324015200171115, 48.23717217682343), (16.324016023309103, 48.23717193740145), (16.324214090513472, 48.23711406382021), (16.324399557025373, 48.23706038923499), (16.324415149019735, 48.23705547511101), (16.32460974945976, 48.23698897490109), (16.32462812209721, 48.236982077704226), (16.324798215997742, 48.236912237087125), (16.324961996233636, 48.23684708139124), (16.324969922263723, 48.23684380276244), (16.325673923443585, 48.236541201866594), (16.325683430390548, 48.23653692159937), (16.326286131224773, 48.236252920784594), (16.32630890862833, 48.23624090954902), (16.32659950878115, 48.23606990910138), (16.32663171509021, 48.23604736008006), (16.326797014875016, 48.23590945978228), (16.326824446994767, 48.235881640584225), (16.327131445693055, 48.23549693996688), (16.32713288008471, 48.235495117466826), (16.327305227456137, 48.235273060779896), (16.327354499075746, 48.23521441287635), (16.32739215237408, 48.23516966812815), (16.327395115126244, 48.23516605096519), (16.327415824966366, 48.235140063946425), (16.32746054383139, 48.235084141972365), (16.327518466879802, 48.235071954139464), (16.327557931207355, 48.23506370340719), (16.327596012784092, 48.23505355718407), (16.32762411285012, 48.235044357154734), (16.327627362334006, 48.235043275056064), (16.327922063006, 48.23494347474031), (16.327968342552538, 48.23492359192401), (16.328007607171294, 48.23489784014237), (16.33050150444806, 48.232888435707615), (16.330524511003027, 48.232866838030645), (16.3311737913115, 48.23215095627107), (16.331840984116514, 48.23150065106492), (16.332076896688704, 48.23143159782075), (16.33220455021194, 48.231399208097564), (16.333151997897424, 48.231159121214674), (16.334291098412443, 48.230870454473205), (16.335921481737454, 48.230481854089206), (16.335922317966467, 48.23048165372785), (16.337338121982576, 48.23014065257515), (16.337342969925867, 48.230139449625376), (16.33885813446082, 48.229752367983195), (16.340333385088577, 48.22943137108373), (16.34034059302165, 48.22942972697916), (16.344541426666634, 48.23009224014183)]


for p in l:
   ax.scatter(p[0] ,p[1],c="y")

#ax.scatter(16.2957298193, 48.1804214091,c="b") #origin
#ax.scatter(16.3877307902, 48.2309296531,c="r")#destination
#ax.scatter(16.307706414966734 ,48.187894496892916 ,c="g")#enrty

#ax.scatter(16.4025272687, 48.2489357246,c="b") #origin
#ax.scatter(16.2904039177, 48.2155788659,c="r")#destination

transformer = Transformer.from_crs('epsg:32633','epsg:4326')
p=transformer.transform(602767.3942660292, 5344290.3636673421)
#ax.scatter(p[1], p[0],c="g")
p=transformer.transform(600014.3268148651, 5343006.1566248685)
#ax.scatter(p[1], p[0],c="g")
p=transformer.transform(599366.656770563, 5342704.041821347)
#ax.scatter(p[1], p[0],c="y")
p=transformer.transform(597096.9560151154, 5341645.307974044)
#ax.scatter(p[1], p[0],c="y")


plt.show()










   








