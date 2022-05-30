# -*- coding: utf-8 -*-
"""
Created on Sat May 28 11:18:31 2022

@author: nipat
"""

import dill
import pandas as pd


##Load teh result dictionaries and convert them to pandas datafarmes
input_file=open("experiment_results/experiment_results/Path_plan_results_experiment1.dill", 'rb')
exp1=dill.load(input_file) #original
exp1_dataframe = pd.DataFrame.from_dict(exp1)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment2.dill", 'rb')
exp2=dill.load(input_file) 
exp2_dataframe = pd.DataFrame.from_dict(exp2)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment3.dill", 'rb')
exp3=dill.load(input_file)
exp3_dataframe = pd.DataFrame.from_dict(exp3)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment4.dill", 'rb')
exp4=dill.load(input_file)
exp4_dataframe = pd.DataFrame.from_dict(exp4)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment5.dill", 'rb')
exp5=dill.load(input_file) 
del exp5["geobreach"]
exp5_dataframe = pd.DataFrame.from_dict(exp5)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment6.dill", 'rb')
exp6=dill.load(input_file) 
del exp6["geobreach"]
exp6_dataframe = pd.DataFrame.from_dict(exp6)

input_file=open("experiment_results/experiment_results/Path_plan_results_smaller_cells.dill", 'rb')
exp7=dill.load(input_file) 
del exp7["geobreach"]
exp7_dataframe = pd.DataFrame.from_dict(exp7)


input_file=open("experiment_results/experiment_results/Path_plan_results_geom.dill", 'rb')
exp8=dill.load(input_file) 
del exp8["geobreach"]
exp8_dataframe = pd.DataFrame.from_dict(exp8)



for i,df in enumerate([exp1_dataframe,exp2_dataframe,exp3_dataframe,exp4_dataframe,exp5_dataframe,exp6_dataframe,exp7_dataframe,exp8_dataframe]):
    unsuccefuly_plans=df[df["lens"]==-1].shape[0]
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
    
    print("For ",i+1,":", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers)
    
    ddf=mp20_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    
    print("For ",i+1," mp20:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers)
    
    ddf=mp30_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    
    print("For ",i+1," mp30:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers)
    
    ddf=constrained_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    
    print("For ",i+1," constrained:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers)
    
    ddf=open_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    
    print("For ",i+1," open:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers)
    
    ddf=mixed_df
    avg_computation_time=ddf["computation_time"].mean()
    avg_dstart_rep=ddf["dstar_repetitions"].mean() 
    avg_geom_rep=ddf["geom_repetitions"].mean() 
    avg_flight_time=ddf["flight_durations"].mean() 
    avg_lens=ddf["lens"].mean()  
    avg_turn_numbers=ddf["turn_numbers"].mean()  
    
    print("For ",i+1," mixed:", avg_computation_time,avg_dstart_rep,avg_geom_rep,avg_flight_time,avg_lens,avg_turn_numbers)
    
    print("#####################################")