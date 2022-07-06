# -*- coding: utf-8 -*-
"""
Created on Sat May 28 11:18:31 2022

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
input_file=open("experiment_results/experiment_results/Path_plan_results_experiment1.dill", 'rb')
exp1=dill.load(input_file) #original
#del exp1["geobreach"]
exp1_dataframe = pd.DataFrame.from_dict(exp1)
exp1_dataframe["Experiment"]="Original"

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment2.dill", 'rb')
exp2=dill.load(input_file) 
#del exp2["geobreach"]
exp2_dataframe = pd.DataFrame.from_dict(exp2)
exp2_dataframe["Experiment"]="Exp1"

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment3.dill", 'rb')
exp3=dill.load(input_file)
#del exp3["geobreach"]
exp3_dataframe = pd.DataFrame.from_dict(exp3)
exp3_dataframe["Experiment"]="Exp2"

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment4.dill", 'rb')
exp4=dill.load(input_file)
#del exp4["geobreach"]
exp4_dataframe = pd.DataFrame.from_dict(exp4)
exp4_dataframe["Experiment"]="Exp3"

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment5.dill", 'rb')
exp5=dill.load(input_file) 
#del exp5["geobreach"]
exp5_dataframe = pd.DataFrame.from_dict(exp5)
exp5_dataframe["Experiment"]="Exp4"

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment6.dill", 'rb')
exp6=dill.load(input_file) 
#del exp6["geobreach"]
exp6_dataframe = pd.DataFrame.from_dict(exp6)
exp6_dataframe["Experiment"]="Exp5"

input_file=open("experiment_results/experiment_results/Path_plan_results_smaller_cells.dill", 'rb')
exp7=dill.load(input_file) 
#del exp7["geobreach"]
exp7_dataframe = pd.DataFrame.from_dict(exp7)
exp7_dataframe["Experiment"]="Exp6"#"Denser \n open graph"


input_file=open("experiment_results/experiment_results/Path_plan_results_geom.dill", 'rb')
exp8=dill.load(input_file) 
#del exp8["geobreach"]
exp8_dataframe = pd.DataFrame.from_dict(exp8)
exp8_dataframe["Experiment"]="Exp7"#"Geometric \n approach"


frames=[exp1_dataframe,exp2_dataframe,exp3_dataframe,exp4_dataframe,exp5_dataframe,exp6_dataframe,exp7_dataframe,exp8_dataframe]

results_df=pd.concat(frames)


fig=plt.figure()
sns.boxplot(y="lens", x='Experiment', data=results_df).set(title="Route length",ylabel="Route length (m)")
adjust_box_widths(fig, 0.9)

#plt.ylim(0, 40000)
plt.show()

fig=plt.figure()
sns.boxplot(y="flight_durations", x='Experiment', data=results_df).set(title="Flight duration",ylabel="Flight duration (sec)")
adjust_box_widths(fig, 0.9)

plt.ylim(0, 5000)
plt.show()

fig=plt.figure()
sns.boxplot(y="computation_time", x='Experiment', data=results_df).set(title="Computation time",ylabel="Computation time (sec)")
adjust_box_widths(fig, 0.9)

plt.show()

fig=plt.figure()
sns.boxplot(y="memory_size", x='Experiment', data=results_df).set(title="Memory size",ylabel="Memory size")
adjust_box_widths(fig, 0.9)

plt.show()

fig=plt.figure()
sns.boxplot(y="memory_size", x='Experiment', data=results_df).set(title="Memory size",ylabel="Memory size")
adjust_box_widths(fig, 0.9)
plt.ylim(0, 2000000)

plt.show()



for i,df in enumerate([exp1_dataframe,exp2_dataframe,exp3_dataframe,exp4_dataframe,exp5_dataframe,exp6_dataframe,exp7_dataframe,exp8_dataframe]):
    unsuccefuly_plans=df[df["lens"]==-1].shape[0]
    unsuccefuly_plans=df[df["lens"]<200].shape[0]
    df=df[df["lens"]!=-1]
    print("Unsucceful paths for ",i+1,":",unsuccefuly_plans)
    mp20_df=df[df["aircraft_types"]==1]
    mp30_df=df[df["aircraft_types"]==2]
    constrained_df=df[df["airspace_type"]==0]
    open_df=df[df["airspace_type"]==1]
    mixed_df=df[df["airspace_type"]==2]
    print("For ",i+1,":",constrained_df.shape[0]," constrained paths,",open_df.shape[0]," open paths,",mixed_df.shape[0],"  mixed paths")
    ddf=df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    avg_size=ddf["memory_size"].mean()  
    geobreaches=ddf["geobreach"].sum()  
    
    print("For ",i+1,":", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers,avg_size,geobreaches)
    
    ddf=mp20_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    avg_size=ddf["memory_size"].mean()  
    geobreaches=ddf["geobreach"].sum()  
    
    print("For ",i+1," mp20:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers,avg_size,geobreaches)
    
    ddf=mp30_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    avg_size=ddf["memory_size"].mean()  
    geobreaches=ddf["geobreach"].sum()  
    
    print("For ",i+1," mp30:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers,avg_size,geobreaches)
    
    ddf=constrained_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean() 
    avg_size=ddf["memory_size"].mean()  
    geobreaches=ddf["geobreach"].sum()  
    
    print("For ",i+1," constrained:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers,avg_size,geobreaches)
    
    ddf=open_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    avg_size=ddf["memory_size"].mean()  
    geobreaches=ddf["geobreach"].sum()  
    
    print("For ",i+1," open:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers,avg_size,geobreaches)
    
    ddf=mixed_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    avg_size=ddf["memory_size"].mean()  
    geobreaches=ddf["geobreach"].sum()  
    
    print("For ",i+1," mixed:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers,avg_size,geobreaches)
    
    print("#####################################")