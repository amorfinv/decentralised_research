# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:07:06 2022

@author: nipat
"""

import matplotlib.pyplot as plt 
import dill
import seaborn as sns
import pandas as pd
import numpy as np

import random ##imported for testing purposes
from matplotlib.patches import PathPatch
import matplotlib
import matplotlib.colors as mc
import colorsys

diagrams_path="output_graphs/"
dills_path="dills/"

matplotlib.use('Agg')
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




concepts=["1_","2_","3_"]
concept_names=["Centralised","Hybrid","Decentralised"]
concept_names_dict={}
for i in range(len(concepts)):
    concept_names_dict[concepts[i]]=concept_names[i]

densities=["very_low_","low_","medium_","high_","ultra_"]
density_names=["very_low","low","medium","high","very_high"]
density_names_dict={}
for i in range(len(densities)):
    density_names_dict[densities[i]]=density_names[i]

traffic_mix=["40_","50_","60_"]
traffic_mix_names=["40%","50%","60%"]
traffic_mix_names_dict={}
for i in range(len(traffic_mix)):
    traffic_mix_names_dict[traffic_mix[i]]=traffic_mix_names[i]

repetitions=["0_","1_","2_","3_","4_","5_","6_","7_","8_"]

uncertainties=["","R1","R2","R3","W1","W3","W5"]
rogue_uncertainties=["","R1","R2","R3"]
wind_uncertainties=["","W1","W3","W5"]
uncertainties_names=["No uncertainty","R1","R2","R3","W1","W3","W5"]
uncertainties_names_dict={}
for i in range(len(uncertainties)):
    uncertainties_names_dict[uncertainties[i]]=uncertainties_names[i]

concepts_colours=['r','g','b']

metrics_title=["AEQ1","AEQ1_1","AEQ2","AEQ2_1","AEQ3","AEQ4","AEQ5","AEQ5_1","CAP1","CAP2","EFF1","EFF2","EFF3","EFF4","EFF5","EFF6","ENV1",\
               "ENV2","ENV4","SAF1","SAF1_2","SAF2","SAF2_1","SAF3","SAF4","SAF5","SAF6","SAF6_1","SAF6_2","SAF6_3","SAF6_4","SAF6_5","SAF6_6",\
                   "SAF6_7","PRI1","PRI2","CAP3","CAP4","PRI3","PRI4","PRI5"]
    
metrics_title=["Number of cancelled demands","AEQ1_1","AEQ2","AEQ2_1","AEQ3","AEQ4","AEQ5","AEQ5_1","CAP1","CAP2","EFF1","EFF2","EFF3","EFF4","EFF5","EFF6","ENV1",\
               "ENV2","ENV4","SAF1","SAF1_2","SAF2","SAF2_1","SAF3","SAF4","SAF5","SAF6","SAF6_1","SAF6_2","SAF6_3","SAF6_4","SAF6_5","SAF6_6",\
                   "SAF6_7","PRI1","PRI2","CAP3","CAP4","PRI3","PRI4","PRI5"]    
boxplot_metrics=["AEQ1","AEQ1_1","AEQ2","AEQ2_1","AEQ3","AEQ4","AEQ5","AEQ5_1","CAP1","CAP2","EFF1","EFF2","EFF3","EFF4","EFF5","EFF6","ENV1","ENV2","ENV4","SAF1","SAF1_2","SAF2","SAF2_1","SAF3","SAF4","SAF5","SAF6","SAF6_1","SAF6_2","SAF6_3","SAF6_4","SAF6_5","SAF6_6","SAF6_7","PRI1","PRI2"]

boxplot_metrics_rogues=["CAP3","CAP4"]

boxplot_metrics_priority=["PRI3","PRI4","PRI5"]
metrics_titles_dict={}
i=0
for m in boxplot_metrics:
    metrics_titles_dict[m]=metrics_title[i]
    i+=1
for m in boxplot_metrics_rogues:
    metrics_titles_dict[m]=metrics_title[i]
    i+=1
for m in boxplot_metrics_priority:
    metrics_titles_dict[m]=metrics_title[i]
    i+=1

def metric_boxplots_baseline(metric,dataframe):
    vals=[]
    for density in densities:
        for t_mix in traffic_mix:
            for conc in concepts:
                for rep in repetitions:   
                    scenario_name=conc+density+t_mix+rep
                    try:
                        metric_value=dataframe[dataframe["Scenario_name"]==scenario_name][metric].values[0]
                        tmp=[concept_names_dict[conc],density_names_dict[density],traffic_mix_names_dict[t_mix],rep,metric_value]
                        vals.append(tmp)
                    except:
                        #metric_value=240+random.randint(-5,5)
                        print("No value for scenario baseline",scenario_name,metric)
                    
                    
    
    metric_pandas_df=pd.DataFrame(vals,columns=["Concept","Density","Traffic mix","repetition",metric])
    
    ##Create one graph for every traffic mix
    for t_mix in traffic_mix_names:
        df1=metric_pandas_df[metric_pandas_df["Traffic mix"]==t_mix]
        fig,ax=plt.subplot()
        sns.boxplot(y=metric, x='Density', data=df1, palette=concepts_colours,hue='Concept').set(title=metrics_titles_dict[metric]+" for "+t_mix+" traffic mix")
        sns.stripplot(y=metric, x='Density', data=df1, palette=concepts_colours,hue='Concept',dodge=True).set(title=metrics_titles_dict[metric]+" for "+t_mix+" traffic mix")

        handles, labels = ax.get_legend_handles_labels()
        plt.legend(handles,concept_names,loc='center left', bbox_to_anchor=(1, 0.5))
        adjust_box_widths(fig, 0.5)
        plt.savefig(diagrams_path+"boxplots/by_traffic_mix/"+metric+"_"+t_mix,bbox_inches='tight')
        plt.savefig(diagrams_path+"pdfs/boxplots/by_traffic_mix/"+metric+"_"+t_mix+".pdf",bbox_inches='tight')
        plt.clf()
        
    ##Create one graph for every density
    for dens in density_names:
         df1=metric_pandas_df[metric_pandas_df["Density"]==dens]
         fig=plt.figure()
         sns.boxplot(y=metric, x='Traffic mix', data=df1, palette=concepts_colours,hue='Concept',width=0.7).set(title=metrics_titles_dict[metric]+" for "+dens+" density")
         sns.stripplot(y=metric, x='Traffic mix', data=df1, palette=concepts_colours,hue='Concept',dodge=True).set(title=metrics_titles_dict[metric]+" for "+dens+" density")

         handles, labels = ax.get_legend_handles_labels()
         plt.legend(handles,concept_names,loc='center left', bbox_to_anchor=(1, 0.5))
         adjust_box_widths(fig, 0.5)
         plt.savefig(diagrams_path+"boxplots/by_density/"+metric+"_"+dens,bbox_inches='tight')
         plt.savefig(diagrams_path+"pdfs/boxplots/by_density/"+metric+"_"+dens+".pdf",bbox_inches='tight')
         plt.clf()




   
                    
                    


       

##Load the metrics
input_file=open(dills_path+"metrics_dataframe.dill", 'rb')
scenario_metrics_df=dill.load(input_file)
input_file.close()

input_file=open(dills_path+"prio_metrics_dataframe.dill", 'rb')
scenario_priority_metrics_df=dill.load(input_file)
input_file.close()

input_file=open(dills_path+"densitylog_dataframe.dill", 'rb')
density_metrics_dataframe=dill.load(input_file)
input_file.close()

input_file=open(dills_path+"density_constrained_dataframe.dill", 'rb')
density_constr_metrics_dataframe=dill.load(input_file)
input_file.close()
#scenario_metrics_df.to_csv("metrics.csv")
#scenario_priority_metrics_df.to_csv("scenario.csv")
#density_metrics_dataframe.to_csv("density.csv")



## Create the graphs
boxplot_metrics=["AEQ1","AEQ1_1","AEQ2","AEQ2_1","AEQ3","AEQ4","AEQ5","AEQ5_1","CAP1","CAP2","EFF1","EFF2","EFF3","EFF4","EFF5","EFF6","ENV1","ENV2","ENV4","SAF1","SAF1_2","SAF2","SAF2_1","SAF3","SAF4","SAF5","SAF6","SAF6_1","SAF6_2","SAF6_3","SAF6_4","SAF6_5","SAF6_6","SAF6_7","PRI1","PRI2"]

boxplot_metrics_rogues=["CAP3","CAP4"]

boxplot_metrics_priority=["PRI3","PRI4","PRI5"]


for metric in boxplot_metrics:
    metric_boxplots_baseline(metric,scenario_metrics_df)

    
