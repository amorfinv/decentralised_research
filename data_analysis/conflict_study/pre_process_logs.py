# andrei code from m2

import numpy as np
from multiprocessing import Pool
import os
import copy
import traceback


# There are three folders
folders = ['PBpbp']
# folders = ['1to1']
# folders = ['m2']

# # Fix the files in these folders
# for folder in folders:
#     files = os.listdir(folder)
#     for file in files:
#         if len(file) > 50:
#             os.rename(folder + '/' + file, folder + '/' + file[:-22]+'.log')

# Get the files in each of these folders
# regs_m2 = [x for x in os.listdir(folders[0]) if 'REGLOG' in x]
regs_pbm2 = [x for x in os.listdir(folders[0]) if 'REGLOG' in x]
# regs_1to1 = [x for x in os.listdir(folders[0]) if 'REGLOG' in x]


# Create input array
input_arr = []
#for scen in centr_regs:
#    input_arr.append([folders[0], scen])
    
#for scen in decentr_regs:
#    input_arr.append([folders[1], scen])
    
for scen in regs_pbm2:
    input_arr.append([folders[0], scen])


# We only need to feed one log, and the rest will have the same name except for 
# the name of the actual log. So just filter out the REGLOGS and feed them to
# the pool.

# Make a function that accepts concept + log file as an input

CENTER_LAT = 48.20499787612939
CENTER_LON = 16.362249993868282

rogue_acids = [f'R{x}' for x in range(408)]

def kwikdist_matrix(lata, lona, latb, lonb):
    """
    Quick and dirty dist [nm]
    In:
        lat/lon, lat/lon vectors [deg]
    Out:
        dist vector [nm]
    """
    re      = 6371000.  # readius earth [m]
    dlat    = np.radians(latb - lata.T)
    dlon    = np.radians(((lonb - lona.T)+180)%360-180)
    cavelat = np.cos(np.radians(lata + latb.T) * 0.5)

    dangle  = np.sqrt(np.multiply(dlat, dlat) +
                      np.multiply(np.multiply(dlon, dlon),
                                  np.multiply(cavelat, cavelat)))
    dist    = re * dangle
    return dist

def process_logs(args):
    concept = args[0]
    reg_log_file = args[1]
    # Get the name of the file so we can load other logs from it as well
    log_file = reg_log_file.replace('REGLOG_', '')
    # Get the names of the other logs
    flst_log_file = 'FLSTLOG_' + log_file
    conf_log_file = 'CONFLOG_' + log_file
    los_log_file = 'LOSLOG_' + log_file
    geo_log_file = 'GEOLOG_' + log_file
    
    # Let's load this guy's flight intention file
    # split log file by underscores
    intention_file = '_'.join(log_file.split('_')[:-1]) + '.csv'
    intention_data = np.genfromtxt('Intentions/' + intention_file, dtype = str, delimiter = ',')
    
    # Create a new array of origin destination data for aircraft
    orig_dest_data = np.zeros((len(intention_data), 4))
    
    for i, ac_data in enumerate(intention_data):
        # The flight number is just the row index + 1, so we don't need that info
        #origin lat
        orig_dest_data[i,0] = float(ac_data[5].replace(')"', ''))
        #origin lon
        orig_dest_data[i,1] = float(ac_data[4].replace('"(', ''))
        #dest lat
        orig_dest_data[i,2] = float(ac_data[7].replace(')"', ''))
        #dest lon
        orig_dest_data[i,3] = float(ac_data[6].replace('"(', ''))
        
    # Delete the data
    #del intention_data
    
    # Load the reglog so we check for drifting aircraft or aircraft sitting on
    # top of destination
    with open(concept + '/' + reg_log_file, 'r') as f:
        # Read the lines
        reg_lines = f.readlines()
        
    # Ok so now we need to go time step by time step, check if aircraft are 
    # close to their destinations, and remember them
    bouncy_ac_dict = dict()
    far_ac_dict = dict()
    idx = 9
    time = 30
    for acid_line in reg_lines[9::5]:   
        if ',' not in acid_line:
            continue
        # Get the ACIDs, lats, lons as numpy arrays
        acids = np.array(acid_line.split(','))[1:]
        try:
            now_lats = np.array(reg_lines[idx+2].split(','), dtype = float)[1:]
            now_lons = np.array(reg_lines[idx+3].split(','), dtype = float)[1:]
        except:
            # Scenario is missing some lines, eh
            continue
                
        # Find if there are rogues, and delete em
        rogue_locations = np.where([(acid.replace('\n', '') in rogue_acids) for acid in acids])[0]

        if rogue_locations.size > 0:
            acids = np.delete(acids, rogue_locations)
            now_lats = np.delete(now_lats, rogue_locations)
            now_lons = np.delete(now_lons, rogue_locations)
                
        # Convert all those ACIDs into ACIDX
        acidx = np.char.replace(acids, 'D', '')
        # Convert these to int
        acidx = acidx.astype(np.int32)-1
        
        # Get the lats and lons of the destinations
        dest_lats = orig_dest_data[:,2][acidx]
        dest_lons = orig_dest_data[:,3][acidx]
        
        # Get the distances
        current_distances = kwikdist_matrix(now_lats, now_lons, dest_lats, dest_lons)
        
        # Get the index where current distances is smaller than 5m
        ac_strikes = np.where(current_distances < 20)[0]
        
        # Also get the indexes where aircraft are too far from the centre
        center_lats = CENTER_LAT + np.zeros(len(now_lats))
        center_lons = CENTER_LON + np.zeros(len(now_lats))
        dist_from_centre = kwikdist_matrix(now_lats, now_lons, center_lats, center_lons)
        
        # Get where aircraft are outside airspace
        far_away = np.where(dist_from_centre > 8500)[0]
        
        if ac_strikes.size>0:
            # Go through each entry, add number of strikes and times
            for num in ac_strikes:
                ac = acidx[num]
                if ac not in bouncy_ac_dict:
                    bouncy_ac_dict[f'D{ac+1}'] = [0]
                bouncy_ac_dict[f'D{ac+1}'][0] += 1
                bouncy_ac_dict[f'D{ac+1}'].append(time)
                
        if far_away.size>0:
            # Go through each entry, add time
            for num in far_away:
                ac = acidx[num]
                if f'D{ac+1}' not in far_ac_dict:
                    far_ac_dict[f'D{ac+1}'] = time
                
        idx += 4
        time += 30
        
    # Filter out aircraft in ac_dict that do not have more than 4 entries
    for acid in copy.copy(bouncy_ac_dict):
        if bouncy_ac_dict[acid][0] < 3:
            bouncy_ac_dict.pop(acid)
            
    # Aggregate both disctionaries
    ac_to_modify = dict()
    for acid in bouncy_ac_dict:
        # Set the time as the second time
        ac_to_modify[acid] = bouncy_ac_dict[acid][2]
        
    for acid in far_ac_dict:
        ac_to_modify[acid] = far_ac_dict[acid]
        
    # We need to delete the aircraft in the dicts in all the other logs after
    # the second time in their entries
    
    # ------------- FLSTLOG ---------------------
    # We want to find the entry for each aircraft, and modify the arrival time
    # and flight time
    with open(concept + '/' + flst_log_file, 'r') as f:
        flstlog = f.readlines()
        
    new_flstlog = copy.copy(flstlog)
        
    for line_idx, flst_line in enumerate(flstlog):
        if line_idx < 9:
            continue
        
        # Split the line
        split_line = flst_line.split(',')
        # Get the flight number
        acid = split_line[1]
        # If rogue, ignore
        if 'R' in acid:
            continue
        
        # Check if it's in the dictionary
        if acid in ac_to_modify:
            # We need to modify the landing time and the flight time
            # The first time is the deletion time
            new_deletion_time = ac_to_modify[acid]
            split_line[0] = f'{new_deletion_time}.00000000'
            
            # Change the flight time
            new_flight_time = new_deletion_time - float(split_line[2])
            
            split_line[3] = f'{new_flight_time}'
            new_flstlog[line_idx] = ','.join(split_line)
            
            # Change the distance metrics as they're meaningless for these aircraft
            split_line[4] = '-1'
            split_line[5] = '-1'
            split_line[6] = '-1'
            
            
    # Save the FLSTLOG
    with open(concept + '_processed/' + flst_log_file, 'w') as f:
        f.write(''.join(new_flstlog))
        
    # ------------- CONFLOG ------------------
    # Take line by line, check if acid in there, check if past time
    
    # Open it 
    with open(concept + '/' + conf_log_file, 'r') as f:
        conflog = f.readlines()
        
    new_conflog = copy.copy(conflog)
        
    for line_idx, conf_line in enumerate(conflog):
        if line_idx < 9:
            continue
        
        # get the split line
        split_line = conf_line.split(',')
        
        if split_line[1] in ac_to_modify:
            # Check if the time is past
            if ac_to_modify[split_line[1]] < float(split_line[0]):
                # We're past the time, delete this line
                new_conflog.pop(new_conflog.index(conf_line))
            
        elif split_line[2] in ac_to_modify:
            # Check if the time is past
            if ac_to_modify[split_line[2]] < float(split_line[0]):
                # We're past the time, delete this line
                new_conflog.pop(new_conflog.index(conf_line))
                
    # Write the new conflog
    with open(concept + '_processed/' + conf_log_file, 'w') as f:
        f.write(''.join(new_conflog))
        
    # ------------- LOSLOG ------------------
    # Same as conflog, but the two acids are in different locations
        
    # Open it 
    with open(concept + '/' + los_log_file, 'r') as f:
        loslog = f.readlines()
        
    new_loslog = copy.copy(loslog)
        
    for line_idx, los_line in enumerate(loslog):
        if line_idx < 9:
            continue
        
        # get the split line
        split_line = los_line.split(',')
        
        if split_line[3] in ac_to_modify:
            # Check if the time is past
            if ac_to_modify[split_line[3]] < float(split_line[0]):
                # We're past the time, delete this line
                new_loslog.pop(new_loslog.index(los_line))
            
        elif split_line[4] in ac_to_modify:
            # Check if the time is past
            if ac_to_modify[split_line[4]] < float(split_line[0]):
                # We're past the time, delete this line
                new_loslog.pop(new_loslog.index(los_line))
                
    # Write the new loslog
    with open(concept + '_processed/' + los_log_file, 'w') as f:
        f.write(''.join(new_loslog))

        
    # ------------- GEOLOG ------------------
    # Same as the los and conf logs, but we only check one acid, and the last
    # element in the line is the time
    
    # Open it 
    with open(concept + '/' + geo_log_file, 'r') as f:
        geolog = f.readlines()
        
    new_geolog = copy.copy(geolog)
        
    for line_idx, geo_line in enumerate(geolog):
        if line_idx < 9:
            continue
        
        # get the split line
        split_line = geo_line.split(',')
        
        if split_line[1] in ac_to_modify:
            # Check if the ac deletion time is in the past
            if ac_to_modify[split_line[1]] < float(split_line[-1].replace('\n', '')):
                # We're past the time, delete this line
                new_geolog.pop(new_geolog.index(geo_line))
                
    # Write the new geolog
    with open(concept + '_processed/' + geo_log_file, 'w') as f:
        f.write(''.join(new_geolog))
        
    # ------------- REGLOG ------------------
    # This one is different
    
    # Open it 
    with open(concept + '/' + reg_log_file, 'r') as f:
        reglog = f.readlines()
        
    new_reglog = copy.copy(reglog)
    
    idx = 9
    # Go once every fourth line
    for acid_line in reg_lines[9::4]:   
        if ',' not in acid_line:
            continue
        # Get the ACIDs, lats, lons as numpy arrays
        acids = acid_line.split(',')
        try:
            now_alts = reg_lines[idx+1].split(',')
            now_lats = reg_lines[idx+2].split(',')
            now_lons = reg_lines[idx+3].split(',')
        except:
            # Scenario is missing some lines, eh
            continue
        new_acids = copy.copy(acids)
        # Check if any of the acids is in the modify dict
        for acid in acids:
            if acid.replace('\n', '') in ac_to_modify:
                if time > ac_to_modify[acid.replace('\n', '')]:
                    # We need to delete this aircraft and its data
                    idx_acid = new_acids.index(acid)
                    new_acids.pop(idx_acid)
                    now_alts.pop(idx_acid)
                    now_lats.pop(idx_acid)
                    now_lons.pop(idx_acid)
                    
        # Replace these lines in the new reglog
        new_reglog[idx] = ','.join(new_acids)
        new_reglog[idx+1] = ','.join(now_alts)
        new_reglog[idx+2] = ','.join(now_lats)
        new_reglog[idx+3] = ','.join(now_lons)
        
        idx += 4
        
    # Add \n to the end of the lines of the reglog
    for i, regline in enumerate(new_reglog):
        if regline[-1:] != '\n':
            new_reglog[i] = regline + '\n'
    
    # Write the new reglog
    with open(concept + '_processed/' + reg_log_file, 'w') as f:
        f.write(''.join(new_reglog))
    return
    
                
def main():
    # process_logs(input_arr[326])
    # return
    # create_dill(input_arr[0])
    pool = Pool(1)
    try:
        _ = pool.map(process_logs, input_arr)
    except Exception as err:
        pool.close()
        print(traceback.format_exc())
        print(err)
    pool.close()
    
if __name__ == '__main__':
    main()
