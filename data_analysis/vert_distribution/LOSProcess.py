import numpy as np
import os
import matplotlib.pyplot as plt

data_folder = 'logs_new'
# The data dictionary
data_dict = dict()

# Get the los logs only
loslogs = [x for x in os.listdir(data_folder) if 'LOSLOG' in x]

# Loop through the logs
for log in loslogs:
    # Get some info about the loslog itself
    log_split = log.split('_')
    # Check for the very case
    if 'very' in log:
        density = 'verylow'
        iteration = int(log_split[6])
        case = log_split[7].replace('.log', '')
    else:
        density = log_split[3]
        iteration = int(log_split[5])
        case = log_split[6].replace('.log', '')
    
    # open the file
    with open(f'{data_folder}/{log}', 'r') as f:
        log_lines = f.readlines()
        
    # Initialise the data dict
    if case not in data_dict:
        data_dict[case] = dict()
    
    if density not in data_dict[case]:
        data_dict[case][density] = dict()
    
    #Initialise the 6 cases
    if 'C-C' not in data_dict[case][density]:
        data_dict[case][density]['C-C'] = np.zeros(9)
    if 'T-T' not in data_dict[case][density]:
        data_dict[case][density]['T-T'] = np.zeros(9)
    if 'U-U' not in data_dict[case][density]:
        data_dict[case][density]['U-U'] = np.zeros(9)
    if 'C-T' not in data_dict[case][density]:
        data_dict[case][density]['C-T'] = np.zeros(9)
    if 'C-U' not in data_dict[case][density]:
        data_dict[case][density]['C-U'] = np.zeros(9)
    if 'T-U' not in data_dict[case][density]:
        data_dict[case][density]['T-U'] = np.zeros(9)
    
    for line in log_lines:
        if 'constrained,constrained' in line:
            if 'C,C' in line:
                data_dict[case][density]['C-C'][iteration] += 1
            elif 'T,T' in line:
                data_dict[case][density]['T-T'][iteration] += 1
            elif 'F,F' in line:
                data_dict[case][density]['U-U'][iteration] += 1
            elif 'C,T' in line or 'T,C' in line:
                data_dict[case][density]['C-T'][iteration] += 1
            elif 'C,F' in line or 'F,C' in line:
                data_dict[case][density]['C-U'][iteration] += 1
            elif 'T,F' in line or 'F,T' in line:
                data_dict[case][density]['T-U'][iteration] += 1

print(data_dict.keys())
# Now we have a great dict, let's make a plot
cases = ['noflow', 'noflowfulldenalloc']
legend = ['Baseline', 'Density Allocation']
density = 'high'
offset = 0.1
barwidth = 0.2
color1 = (0.86, 0.3712, 0.33999999999999997)
color2 = (0.33999999999999997, 0.8287999999999999, 0.86)
data1 = data_dict[cases[0]][density]
data2 = data_dict[cases[1]][density]

plt.figure('niceplot')
for i, layerconf in enumerate(data1.keys()):
    avg_los_1 = np.average(data1[layerconf])
    avg_los_2 = np.average(data2[layerconf])
    std_1 = np.std(data1[layerconf])
    std_2 = np.std(data2[layerconf])
    if i == 0:
        plt.bar(i-offset, avg_los_1, color = color1, width = barwidth, label = legend[0])
        plt.bar(i+offset, avg_los_2, color = color2, width = barwidth, label = legend[1])
    else:
        plt.bar(i-offset, avg_los_1, color = color1, width = barwidth)
        plt.bar(i+offset, avg_los_2, color = color2, width = barwidth)
        
    plt.errorbar(i-offset,avg_los_1, yerr = std_1, capsize = 3, color = 'black')
    plt.errorbar(i+offset,avg_los_2, yerr = std_2, capsize = 3, color = 'black')

plt.xticks(range(6), list(data1.keys()))
plt.xlabel('Layers type')
plt.ylabel('Average number of intrusions [-]')
plt.legend()
plt.show()


