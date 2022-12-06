# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 17:05:15 2022

@author: nipat
"""


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

def adjust_box_widths(g, fac):
    """
    Adjust the withs of a seaborn-generated boxplot.
    """
    k=0

    # iterating through Axes instances
    for ax in g.axes:

        # iterating through axes artists:
        for c in ax.get_children():
            # searching for PathPatches
            if isinstance(c, PathPatch):
                # getting current width of box:
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]
                xmin = np.min(verts_sub[:, 0])
                xmax = np.max(verts_sub[:, 0])
                xmid = 0.5*(xmin+xmax)
                xhalf = 0.5*(xmax - xmin)

                # setting new width of box
                xmin_new = xmid-fac*xhalf
                xmax_new = xmid+fac*xhalf
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new
                
                # Set the linecolor on the artist to the facecolor, and set the facecolor to None
                col = lighten_color(c.get_facecolor(), 1.3)
                c.set_edgecolor(col) 

                for j in range((k)*6,(k)*6+6):
                   line = ax.lines[j]
                   line.set_color(col)
                   line.set_mfc(col)
                   line.set_mec(col)
                   line.set_linewidth(0.7)
                    
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])
                k+=1

def lighten_color(color, amount=0.5):  
    # --------------------- SOURCE: @IanHincks ---------------------
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

##Load teh result dictionaries and convert them to pandas datafarmes
# =============================================================================
# input_file=open("experiment_results/Path_plan_results_experiment1.dill", 'rb')
# exp1=dill.load(input_file) #original
# del exp1["geobreach"]
# exp1_dataframe = pd.DataFrame.from_dict(exp1)
# exp1_dataframe["Experiment"]="BB"
# 
# input_file=open("experiment_results/Path_plan_results_experiment2.dill", 'rb')
# exp2=dill.load(input_file) 
# del exp2["geobreach"]
# exp2_dataframe = pd.DataFrame.from_dict(exp2)
# exp2_dataframe["Experiment"]="MB"
# 
# input_file=open("experiment_results/Path_plan_results_experiment3.dill", 'rb')
# exp3=dill.load(input_file)
# del exp3["geobreach"]
# exp3_dataframe = pd.DataFrame.from_dict(exp3)
# exp3_dataframe["Experiment"]="EB"
# 
# input_file=open("experiment_results/Path_plan_results_experiment4.dill", 'rb')
# exp4=dill.load(input_file)
# del exp4["geobreach"]
# exp4_dataframe = pd.DataFrame.from_dict(exp4)
# exp4_dataframe["Experiment"]="BS"
# 
# input_file=open("experiment_results/Path_plan_results_experiment5.dill", 'rb')
# exp5=dill.load(input_file) 
# del exp5["geobreach"]
# exp5_dataframe = pd.DataFrame.from_dict(exp5)
# exp5_dataframe["Experiment"]="BL"
# 
# input_file=open("experiment_results/Path_plan_results_experiment6.dill", 'rb')
# exp6=dill.load(input_file) 
# del exp6["geobreach"]
# exp6_dataframe = pd.DataFrame.from_dict(exp6)
# exp6_dataframe["Experiment"]="EL"
# 
# 
# 
# 
# frames=[exp1_dataframe,exp2_dataframe,exp3_dataframe,exp4_dataframe,exp5_dataframe,exp6_dataframe]
# 
# df=pd.concat(frames)
# 
# 
# 
# mp20_df=df[df["aircraft_types"]==1]
# mp30_df=df[df["aircraft_types"]==2]
# 
# 
# 
# 
# mp20_df["time"]=mp20_df["lens"]/10.29+mp20_df["turn_numbers"]*0.96
# 
# mp30_df["time"]=mp30_df["lens"]/15.43+mp30_df["turn_numbers"]*2.75
# 
# ddf=pd.concat([mp20_df,mp30_df])
# df=ddf
# 
# bs_df=df[df["Experiment"]=="BB"]
# print("baseline time", bs_df["time"].mean())
# 
# dense_df=df[df["Experiment"]=="EB"]
# print("EB  time", dense_df["time"].mean())
# 
# geom_df=df[df["Experiment"]=="MB"]
# print("MB time", geom_df["time"].mean())
# 
# dense_df=df[df["Experiment"]=="BS"]
# print("BS  time", dense_df["time"].mean())
# 
# geom_df=df[df["Experiment"]=="BL"]
# print("BL time", geom_df["time"].mean())
# 
# 
# geom_df=df[df["Experiment"]=="EL"]
# print("EL time", geom_df["time"].mean())
# 
# constrained_df=df[df["airspace_type"]==0]
# 
# 
# df["lens"]=df["lens"]/1000
# #d* rep
# 
# fig=plt.figure()
# sns.boxplot(y="dstar_repetitions", x='Experiment', data=df).set(ylabel="D* repetitions")
# adjust_box_widths(fig, 0.9)
# plt.savefig("dstar_rep",bbox_inches='tight')
# 
# #dstar_rep_cons
# fig=plt.figure()
# sns.boxplot(y="dstar_repetitions", x='Experiment', data=constrained_df).set(ylabel="D* repetitions")
# adjust_box_widths(fig, 0.9)
# plt.savefig("dstar_rep_cons",bbox_inches='tight')
# 
# #route_length
# fig=plt.figure()
# sns.boxplot(y="lens", x='Experiment', data=df).set(ylabel="Route length (km)")
# adjust_box_widths(fig, 0.9)
# plt.savefig("route_length",bbox_inches='tight')
# 
# #turns
# fig=plt.figure()
# sns.boxplot(y="turn_numbers", x='Experiment', data=df).set(ylabel="Turns")
# adjust_box_widths(fig, 0.9)
# plt.savefig("turns",bbox_inches='tight')
# 
# #intersections
# fig=plt.figure()
# sns.boxplot(y="intersection_numbers", x='Experiment', data=df).set(ylabel="Intersection turns")
# adjust_box_widths(fig, 0.9)
# plt.savefig("intersections",bbox_inches='tight')
# 
# #flight_duration
# fig=plt.figure()
# sns.boxplot(y="time", x='Experiment', data=df).set(ylabel="Flight duration (sec)")
# adjust_box_widths(fig, 0.9)
# plt.savefig("flight_duration",bbox_inches='tight')
# 
# #flight_dur_cons
# fig=plt.figure()
# sns.boxplot(y="time", x='Experiment', data=constrained_df).set(ylabel="Flight duration (sec)")
# adjust_box_widths(fig, 0.9)
# plt.savefig("flight_dur_cons",bbox_inches='tight')
# =============================================================================


##For open airspace

input_file=open("experiment_results/Path_plan_results_experiment1.dill", 'rb')
exp1=dill.load(input_file) #original
del exp1["geobreach"]
exp1_dataframe = pd.DataFrame.from_dict(exp1)
exp1_dataframe["Experiment"]="Baseline"

input_file=open("experiment_results/Path_plan_results_smaller_cells.dill", 'rb')
exp7=dill.load(input_file) 
del exp7["geobreach"]
exp7_dataframe = pd.DataFrame.from_dict(exp7)
exp7_dataframe["Experiment"]="Denser \n open graph"


input_file=open("experiment_results/Path_plan_results_geom.dill", 'rb')
exp8=dill.load(input_file) 
del exp8["geobreach"]
exp8_dataframe = pd.DataFrame.from_dict(exp8)
exp8_dataframe["Experiment"]="Geometric \n approach"


frames=[exp1_dataframe,exp7_dataframe,exp8_dataframe]

df=pd.concat(frames)


mp20_df=df[df["aircraft_types"]==1]
mp30_df=df[df["aircraft_types"]==2]




mp20_df["time"]=mp20_df["lens"]/10.29+mp20_df["turn_numbers"]*0.96

mp30_df["time"]=mp30_df["lens"]/15.43+mp30_df["turn_numbers"]*2.75

ddf=pd.concat([mp20_df,mp30_df])
df=ddf




bs_df=df[df["Experiment"]=="Baseline"]
print("baseline time", bs_df["time"].mean())

dense_df=df[df["Experiment"]=="Denser \n open graph"]
print("dense  time", dense_df["time"].mean())

geom_df=df[df["Experiment"]=="Geometric \n approach"]
print("geom time", geom_df["time"].mean())


df["lens"]=df["lens"]/1000
open_df=df[df["airspace_type"]==1]
const_df=df[df["airspace_type"]==0]

bs_df=const_df[const_df["Experiment"]=="Baseline"]
print("consbaseline time", bs_df["time"].mean())

dense_df=const_df[const_df["Experiment"]=="Denser \n open graph"]
print(" cons dense  time", dense_df["time"].mean())

geom_df=const_df[const_df["Experiment"]=="Geometric \n approach"]
print("cons geom time", geom_df["time"].mean())

bs_df=open_df[open_df["Experiment"]=="Baseline"]
print("open baseline time", bs_df["time"].mean())

dense_df=open_df[open_df["Experiment"]=="Denser \n open graph"]
print("open dense  time", dense_df["time"].mean())

geom_df=open_df[open_df["Experiment"]=="Geometric \n approach"]
print("open geom time", geom_df["time"].mean())

#######################
 
bs_df=df[df["Experiment"]=="Baseline"]
print("baseline rep", bs_df["dstar_repetitions"].mean())

dense_df=df[df["Experiment"]=="Denser \n open graph"]
print("dense  rep", dense_df["dstar_repetitions"].mean())

geom_df=df[df["Experiment"]=="Geometric \n approach"]
print("geom rep", geom_df["dstar_repetitions"].mean())

bs_df=const_df[const_df["Experiment"]=="Baseline"]
print("consbaseline rep", bs_df["dstar_repetitions"].mean())

dense_df=const_df[const_df["Experiment"]=="Denser \n open graph"]
print(" cons dense  rep", dense_df["dstar_repetitions"].mean())

geom_df=const_df[const_df["Experiment"]=="Geometric \n approach"]
print("cons geom rep", geom_df["dstar_repetitions"].mean())

bs_df=open_df[open_df["Experiment"]=="Baseline"]
print("open baseline rep", bs_df["dstar_repetitions"].mean())

dense_df=open_df[open_df["Experiment"]=="Denser \n open graph"]
print("open dense  rep", dense_df["dstar_repetitions"].mean())

geom_df=open_df[open_df["Experiment"]=="Geometric \n approach"]
print("open geom rep", geom_df["dstar_repetitions"].mean())
#route_length

fig=plt.figure()
sns.boxplot(y="lens", x='Experiment', data=df).set(ylabel="Route length (km)")
adjust_box_widths(fig, 0.9)
plt.savefig("route_length",bbox_inches='tight')

#route_length_open

fig=plt.figure()
sns.boxplot(y="lens", x='Experiment', data=open_df).set(ylabel="Route length (km)")
adjust_box_widths(fig, 0.9)
plt.savefig("route_length_open",bbox_inches='tight')

#turns
fig=plt.figure()
sns.boxplot(y="turn_numbers", x='Experiment', data=df).set(ylabel="Turns")
adjust_box_widths(fig, 0.9)
plt.savefig("turns",bbox_inches='tight')

#turns_open
fig=plt.figure()
sns.boxplot(y="turn_numbers", x='Experiment', data=open_df).set(ylabel="Turns")
adjust_box_widths(fig, 0.9)
plt.savefig("turns_open",bbox_inches='tight')

#intersections
fig=plt.figure()
sns.boxplot(y="intersection_numbers", x='Experiment', data=df).set(ylabel="Intersection turns")
adjust_box_widths(fig, 0.9)
plt.savefig("intersections",bbox_inches='tight')

#flight_duration
fig=plt.figure()
sns.boxplot(y="time", x='Experiment', data=df).set(ylabel="Flight duration (sec)")
adjust_box_widths(fig, 0.9)
plt.savefig("flight_duration",bbox_inches='tight')


#flight_dur_open
fig=plt.figure()
sns.boxplot(y="time", x='Experiment', data=open_df).set(ylabel="Flight duration (sec)")
adjust_box_widths(fig, 0.9)
plt.savefig("flight_dur_open",bbox_inches='tight')
# =============================================================================


