# %%
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:47:30 2021
@author: andub
"""
import numpy as np
import os
import geopandas as gpd


def kwikdist(origin, destination):
    """
    Quick and dirty dist [nm]
    In:
        lat/lon, lat/lon [deg]
    Out:
        dist [nm]
    """
    # We're getting these guys as strings
    lona = float(origin[0])
    lata = float(origin[1])

    lonb = float(destination[0])
    latb = float(destination[1])

    re      = 6371000.  # radius earth [m]
    dlat    = np.radians(latb - lata)
    dlon    = np.radians(((lonb - lona)+180)%360-180)
    cavelat = np.cos(np.radians(lata + latb) * 0.5)

    dangle  = np.sqrt(dlat * dlat + dlon * dlon * cavelat * cavelat)
    dist    = re * dangle
    return dist


def PreGeneratedPaths():
    """ Generates a set of pre-generated paths for the aircraft. It reads the origins and 
    destinations and creates the list of tuples with
    (origin_lon, origin_lat, destination_lon, destination_lat)

    """
    origins = gpd.read_file('whole_vienna/gis/Sending_nodes.gpkg').to_numpy()[:,0:2]
    destinations = gpd.read_file('whole_vienna/gis/Recieving_nodes.gpkg').to_numpy()[:,0:2]

    pairs = []
    round_int = 10
    for origin in origins:
        for destination in destinations:
            if kwikdist(origin, destination) >=800:
                lon1 = origin[0]
                lat1 = origin[1]
                lon2 = destination[0]
                lat2 = destination[1]
                pairs.append((round(lon1,round_int),round(lat1,round_int),round(lon2,round_int),round(lat2,round_int)))

    return pairs


def scenario_dills():
    dill_list = set()

    # read scenarios from M2_scenarios
    scenario_folder = '../M2_scenarios/'
    scenario_folder_files = os.listdir(scenario_folder)
    scenario_folder_files = [file for file in scenario_folder_files if not 'R1' in file and not 'R2' in file and not 'R3' in file and not 'W1' in file and not 'W2' in file and not 'W3' in file and not 'batch' in file]

    def check_scen_dills(scen):
        with open(scenario_folder + scen, 'r') as f:
            lines = f.readlines()
            lines = lines[11:]
        for line in lines:
            dill_name = line.split(',')[2].split('_')[0]
            dill_list.add(int(dill_name))


    for scenario in scenario_folder_files:
        check_scen_dills(scenario)


    return list(dill_list)


# Get Origin-Destination pairs list of all sending receiving nodes
# data is organized as (lon, lat, lon, lat)
pairs_list = PreGeneratedPaths()

# NOW JUST GET THE ONES THAT ARE IN THE SCENARIOS of Flight_intention_*_40*.scn
# THE ENTRIES INSIDE dill_list CORRESPOND TO AN INDEX IN pairs_list
dill_list = scenario_dills()

