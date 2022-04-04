
# %%
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:47:30 2021
@author: andub
"""
import os

# set the location of the vanilla scenarios
scenario_folders = ['M2_scenarios/', 
                    'airspace_structure_study/1_to_1_scenarios/',
                    'heading_layer_allocation_study/head_alloc_scenarios/',
                    'heading_layer_allocation_study/heading_alloc_scenarios_no_flow/',
                    'heading_based_cr/hdg_cr_scenarios/',
                    'baseline_scenarios/']


# set location of places that bluesky should search for all the blueksy scenarios
# plus the location of the batch file
scenario_path_bluesky = 'M2sensitivity/'
batch_scenario_folder = 'batch_scenarios/'
# get scenario files in main scenario folder and remove anything that doesnt start with 'Flight_'
scenario_files = []
for scenario_folder in scenario_folders:

    scenario_folder_files = os.listdir(scenario_folder)
    scenario_files += [x for x in scenario_folder_files if x.startswith('Flight_')]

# split the scenarios
very_low_scenarios = [file for file in scenario_files if 'very_low' in file]
low_scenarios = [file for file in scenario_files if 'low' in file and 'very' not in file]
medium_scenarios = [file for file in scenario_files if 'medium' in file]
high_scenarios = [file for file in scenario_files if 'high' in file]
ultra_scenarios = [file for file in scenario_files if 'ultra' in file]

# assemble scenarios into two batches
batch_1 = very_low_scenarios + low_scenarios + medium_scenarios
batch_2 = high_scenarios + ultra_scenarios

# create the first batch scenatio

batch_1_scenario = []
for scenario in batch_1:

    # remove last 4 characters
    line1 = f'00:00:00>SCEN {scenario[:-4]}\n'
    line2 = f'00:00:00>PCALL {scenario_path_bluesky}{scenario}\n'
    line3 = '00:00:00>FF\n'
    line4 = '00:00:00>SCHEDULE 03:00:00 HOLD\n'
    line5 = '00:00:00>SCHEDULE 03:00:00 DELETEALL\n\n'

    batch_1_scenario.append(line1)
    batch_1_scenario.append(line2)
    batch_1_scenario.append(line3)
    batch_1_scenario.append(line4)
    batch_1_scenario.append(line5)

# write to a file
with open(f'{batch_scenario_folder}struct_batch_1.scn', 'w') as file:
    file.writelines(batch_1_scenario)

# now do batch scenario 2
batch_2_scenario = []
for scenario in batch_2:
    # remove last 4 characters
    line1 = f'00:00:00>SCEN {scenario[:-4]}\n'
    line2 = f'00:00:00>PCALL {scenario_path_bluesky}{scenario}\n'
    line3 = '00:00:00>FF\n'
    line4 = '00:00:00>SCHEDULE 03:00:00 HOLD\n'
    line5 = '00:00:00>SCHEDULE 03:00:00 DELETEALL\n\n'

    batch_2_scenario.append(line1)
    batch_2_scenario.append(line2)
    batch_2_scenario.append(line3)
    batch_2_scenario.append(line4)
    batch_2_scenario.append(line5)

# write to a file
with open(f'{batch_scenario_folder}struct_batch_2.scn', 'w') as file:
    file.writelines(batch_2_scenario)

# %%
