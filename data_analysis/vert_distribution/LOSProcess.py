import numpy as np
import os
import matplotlib.pyplot as plt

data_folder = 'logs'
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
            # check to see the altitude difference so you only include horizontal
            los = line.split(',')
            alt_1 = float(los[7])
            alt_2 = float(los[10])
            alt_diff = abs(alt_1 - alt_2)

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

# Now we have a great dict, let's make a plot
cases = ['noflow', 'noflowfulldenalloc', 'noflowrandomalloc', 'noflowdistalloc']
legend = ['Baseline', 'Density Allocation', 'Random Allocation', 'Distance Allocation']
density = 'high'
offset = 0.1
barwidth = 0.2
color1 = (0.86, 0.3712, 0.33999999999999997)
color2 = (0.5688000000000001, 0.86, 0.33999999999999997)
color3 =  (0.33999999999999997, 0.8287999999999999, 0.86)
color4 =  (0.6311999999999998, 0.33999999999999997, 0.86)
data1 = data_dict[cases[0]][density]
data2 = data_dict[cases[1]][density]
data3 = data_dict[cases[2]][density]
data4 = data_dict[cases[3]][density]

colors = [
    (0.86, 0.3712, 0.33999999999999997), 
    (0.5688000000000001, 0.86, 0.33999999999999997), 
    (0.33999999999999997, 0.8287999999999999, 0.86), 
    (0.6311999999999998, 0.33999999999999997, 0.86),
    ]

plt.figure('niceplot')
for i, layerconf in enumerate(data1.keys()):
    avg_los_1 = np.average(data1[layerconf])
    avg_los_2 = np.average(data2[layerconf])
    avg_los_3 = np.average(data3[layerconf])
    avg_los_4 = np.average(data4[layerconf])

    std_1 = np.std(data1[layerconf])
    std_2 = np.std(data2[layerconf])
    std_3 = np.std(data1[layerconf])
    std_4 = np.std(data2[layerconf])

    if i == 0:
        plt.bar(i-3*offset, avg_los_1, color = color1, width = barwidth, label = legend[0])
        plt.bar(i-1*offset, avg_los_2, color = color2, width = barwidth, label = legend[1])
        plt.bar(i+1*offset, avg_los_3, color = color3, width = barwidth, label = legend[2])
        plt.bar(i+3*offset, avg_los_4, color = color4, width = barwidth, label = legend[3])

    else:
        plt.bar(i-3*offset, avg_los_1, color = color1, width = barwidth)
        plt.bar(i-1*offset, avg_los_2, color = color2, width = barwidth)
        plt.bar(i+1*offset, avg_los_3, color = color3, width = barwidth)
        plt.bar(i+3*offset, avg_los_4, color = color4, width = barwidth)
    
    plt.errorbar(i-3*offset,avg_los_1, yerr = std_1, capsize = 3, color = 'black')
    plt.errorbar(i-1*offset,avg_los_2, yerr = std_2, capsize = 3, color = 'black')
    plt.errorbar(i+1*offset,avg_los_3, yerr = std_3, capsize = 3, color = 'black')
    plt.errorbar(i+3*offset,avg_los_4, yerr = std_4, capsize = 3, color = 'black')

plt.xticks(range(6), list(data1.keys()))
plt.xlabel('Layer pairs')
plt.ylabel('Average number intrusions [-]')
# plt.ylim(0, 700)
plt.legend()
plt.show()


