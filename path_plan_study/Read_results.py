# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:15:22 2022

@author: nipat
"""

import dill
import pandas as pd




input_file=open("experiment_results/experiment_results/Path_plan_results_experiment1.dill", 'rb')
exp1=dill.load(input_file) #original

avg_computation_time=sum(exp1["computation_time"])/len(exp1["computation_time"])
avg_dstart_rep=sum(exp1["dstar_repetitions"])/len(exp1["dstar_repetitions"])
avg_flight_time=sum(exp1["flight_durations"])/len(exp1["flight_durations"])
avg_lens=sum(exp1["lens"])/len(exp1["lens"])
avg_turn_numbers=sum(exp1["turn_numbers"])/len(exp1["turn_numbers"])
print("1:", avg_computation_time,avg_dstart_rep,avg_flight_time,avg_lens,avg_turn_numbers)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment2.dill", 'rb')
exp2=dill.load(input_file) 

avg_computation_time=sum(exp2["computation_time"])/len(exp2["computation_time"])
avg_dstart_rep=sum(exp2["dstar_repetitions"])/len(exp2["dstar_repetitions"])
avg_flight_time=sum(exp2["flight_durations"])/len(exp2["flight_durations"])
avg_lens=sum(exp2["lens"])/len(exp2["lens"])
avg_turn_numbers=sum(exp2["turn_numbers"])/len(exp2["turn_numbers"])
print("2:",avg_computation_time,avg_dstart_rep,avg_flight_time,avg_lens,avg_turn_numbers)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment3.dill", 'rb')
exp3=dill.load(input_file) 

avg_computation_time=sum(exp3["computation_time"])/len(exp3["computation_time"])
avg_dstart_rep=sum(exp3["dstar_repetitions"])/len(exp3["dstar_repetitions"])
avg_flight_time=sum(exp3["flight_durations"])/len(exp3["flight_durations"])
avg_lens=sum(exp3["lens"])/len(exp3["lens"])
avg_turn_numbers=sum(exp3["turn_numbers"])/len(exp3["turn_numbers"])
print("3:",avg_computation_time,avg_dstart_rep,avg_flight_time,avg_lens,avg_turn_numbers)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment4.dill", 'rb')
exp4=dill.load(input_file)

avg_computation_time=sum(exp4["computation_time"])/len(exp4["computation_time"])
avg_dstart_rep=sum(exp4["dstar_repetitions"])/len(exp4["dstar_repetitions"])
avg_flight_time=sum(exp4["flight_durations"])/len(exp4["flight_durations"])
avg_lens=sum(exp4["lens"])/len(exp4["lens"])
avg_turn_numbers=sum(exp4["turn_numbers"])/len(exp4["turn_numbers"])
print("4:",avg_computation_time,avg_dstart_rep,avg_flight_time,avg_lens,avg_turn_numbers)

input_file=open("experiment_results/experiment_results/Path_plan_results_experiment5.dill", 'rb')
exp5=dill.load(input_file) 

avg_computation_time=sum(exp5["computation_time"])/len(exp5["computation_time"])
avg_dstart_rep=sum(exp5["dstar_repetitions"])/len(exp5["dstar_repetitions"])
avg_flight_time=sum(exp5["flight_durations"])/len(exp5["flight_durations"])
avg_lens=sum(exp5["lens"])/len(exp5["lens"])
avg_turn_numbers=sum(exp5["turn_numbers"])/len(exp5["turn_numbers"])
print("5:",avg_computation_time,avg_dstart_rep,avg_flight_time,avg_lens,avg_turn_numbers)