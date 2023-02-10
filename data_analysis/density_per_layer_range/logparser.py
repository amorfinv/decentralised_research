import os
from rich import print
from rich.progress import track
import pandas as pd
from datetime import timedelta, datetime
from shapely.geometry import Point, MultiPoint
import osmnx as ox
import networkx as nx
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import defaultdict

from constrained import constrained_airspace_gdf

# ignore warnings with the way the gdf is created
import warnings
warnings.filterwarnings('ignore')
gpkgs_loc = '/Users/localadmin/Desktop/andresmorfin/decentralised_research/maps/gpkgs'
results_loc = 'results_airspace'

def logparse(args):

    densities = args['density']
    concepts = args['concept']
    repetitions = range(9)

    alt_bins = [0, 105, 195, 285, 375, 500]
    alt_labels = [f'{alt_bins[idx-1]}-{upper_alt} feet' for idx, upper_alt in enumerate(alt_bins[1:], start=1)]
    renaming_cols = {
        (0, '0-105 feet'): '0-105 ft',
        (0, '105-195 feet'): '105-195 ft',
        (0, '195-285 feet'): '195-285 ft',
        (0, '285-375 feet'): '285-375 ft',
        (0, '375-500 feet'): '375-500 ft'
        }

    G = ox.load_graphml('other_data/finalized_graph.graphml')
    edge_length = nx.get_edge_attributes(G, "length")

    # first loop through densities
    for i, density in enumerate(densities):
        
        # figure of layer concept
        fig, axs = plt.subplots(5, sharex=True, sharey=True)
        fig.set_size_inches(w=9, h=11)
        fig.suptitle(f'{density} scenario')
        fig.text(0.5, 0.04, 'seconds', ha='center')
        fig.text(0.04, 0.5, 'Aircraft density in constrained airspace (n_air/km)', va='center', rotation='vertical')
        # fig.text(0.04, 0.5, 'Number of aircraft in constrained airspace', va='center', rotation='vertical')

        # figure of layers for that concept
        con_data = defaultdict()

        # then loop through concepts
        for j, concept in enumerate(concepts):
            
            # get some information
            scn_comb = ('REGLOG', density, concept)
            gpkg_name = '_'.join(scn_comb)

            # get the log file names
            log_prefix = scn_comb[0] + '_Flight_intention_' + scn_comb[1] + '_40_'
            log_suffix = '_' + scn_comb[2] + '.log'
            scenario_list = [f'{log_prefix}{i}{log_suffix}' for i in repetitions]

            # filter out any non reglog files
            reglog_scenarios = [f[24:-4] for f in scenario_list if 'REGLOG' in f]

            # read the geopackage
            gdf = gpd.read_file(gpkgs_loc + '/' + gpkg_name + '.gpkg')
            gdf['ALT'] = gdf['ALT'].apply(pd.to_numeric, errors='ignore')
            gdf['seconds'] = gdf['seconds'].apply(pd.to_numeric, errors='ignore')
            gdf['alt_bin'] = pd.cut(gdf['ALT'], alt_bins, labels=alt_labels)
            # now only select points inside constrained airspace
            gdf_constrained = gdf.sjoin(constrained_airspace_gdf, how="inner", predicate="within")

            # loop through scenarios TODO: make it for all reps?
            scenario = reglog_scenarios[0]

            # scenarios specific gdf
            scen_gdf = gdf_constrained[gdf_constrained['scenario'] == scenario]

            # prep the data to plot
            time_df = scen_gdf.groupby(by=['seconds', 'alt_bin']).size()
            time_sorted_df = time_df.reset_index().sort_values('seconds').pivot('seconds','alt_bin')
            time_sorted_df.columns = [renaming_cols.get(x, x) for x in time_sorted_df.columns]

            new_cols = time_sorted_df.columns.to_list()[::-1]

            scale_dict = defaultdict()
            # scale with total airspace usage?
            for alt_range in gdf['alt_bin'].unique():
                
                # for some reason nan is a float
                if isinstance(alt_range, float):
                    continue
                unique_edges = scen_gdf[scen_gdf['alt_bin'] == alt_range].edge_id_str.unique()
                edgeids_float = [tuple(map(int, edge.split('-'))) + (0,) for edge in unique_edges]
                scen_edge_lengths = np.array(list(map(edge_length.get, edgeids_float)))

                scen_edge_lengths = np.where(scen_edge_lengths != None, scen_edge_lengths, 0)

                scaled_sum = np.sum(scen_edge_lengths)
                renamed_alt = renaming_cols[(0, alt_range)]
                scale_dict[renamed_alt] = scaled_sum

                #time_sorted_df[renamed_alt] = time_sorted_df[renamed_alt].div(scaled_sum/1000)
                
                time_sorted_df[renamed_alt] = time_sorted_df[renamed_alt]
        
            
            # loop to create the five imagee
            for idx, column_name in enumerate(new_cols):
        
                axs[idx].plot(time_sorted_df.index, time_sorted_df[column_name], label=concept)
                axs[idx].legend()
                axs[idx].yaxis.set_label_position("right")
                axs[idx].set_ylabel(ylabel=column_name, rotation=0)
                axs[idx].yaxis.set_label_coords(1.07,0.5)

            time_sorted_df['total'] = time_sorted_df[list(time_sorted_df.columns)].sum(axis=1)
            con_data[concept] = time_sorted_df

        plt.savefig(os.path.join(f'images/{density}/aircraft_count_rep0_scale.png'))
        plt.close()

        # figure of concept
        
        for concept in concepts:
            con_data[concept].plot(title=f'{concept} {density} scenario', xlabel='seconds',
                                    ylabel='Number of aircraft in constrained airspace',
                                    figsize=(10,10))
            plt.savefig(os.path.join(f'images/{density}/{concept}aircraft_count_rep0_scaled.png'))

        

        # if gpkg_args['logtype'] == 'CONFLOG':
        #     # check if the file exists
        #     if os.path.exists(os.path.join('gpkgs', gpkg_name + '.gpkg')):
        #         print(f'[bright_black]gpkgs/{gpkg_name}.gpkg already exists, skipping.')
        #         continue

        #     conflog(scenario_list, gpkg_name, gpkg_args)

        # if gpkg_args['logtype'] == 'LOSLOG':
        #     # check if the file exists
        #     if os.path.exists(os.path.join('gpkgs', gpkg_name + '.gpkg')):
        #         print(f'[bright_black]gpkgs/{gpkg_name}.gpkg already exists, skipping.')
        #         continue

        #     loslog(scenario_list, gpkg_name, gpkg_args)



def reglog(scenario_list, gpkg_name, gpkg_args):

    # filter out any non reglog files
    reglog_scenarios = [f[24:-4] for f in scenario_list if 'REGLOG' in f]

    data = {}

    # frest reglog creates general log
    print(f'[green]Parsing {gpkg_name}')
    
    # for loop starts here
    alt_bins = [0, 105, 195, 285, 375, 500]
    alt_labels = [f'{alt_bins[idx-1]}-{upper_alt} feet' for idx, upper_alt in enumerate(alt_bins[1:], start=1)]

    # load the geopackage and prep data
    gdf = gpd.read_file(gpkgs_loc + '/' + gpkg_name + '.gpkg')
    gdf['ALT'] = gdf['ALT'].apply(pd.to_numeric, errors='ignore')
    gdf['seconds'] = gdf['seconds'].apply(pd.to_numeric, errors='ignore')
    gdf['alt_bin'] = pd.cut(gdf['ALT'], alt_bins, labels=alt_labels)

    # now only select points inside constrained airspace
    gdf_constrained = gdf.sjoin(constrained_airspace_gdf, how="inner", predicate="within")
    scenario = reglog_scenarios[0]
    density = ('_').join(scenario.split('_')[:-3])
    concept = scenario.split('_')[-1]

    # select the 0th repitition
    scen_gdf = gdf_constrained[gdf_constrained['scenario'] == scenario]

    # prep te data
    time_df = scen_gdf.groupby(by=['seconds', 'alt_bin']).size()

    fig, axs = plt.subplots(5)
    time_sorted_df = time_df.reset_index().sort_values('seconds').pivot('seconds','alt_bin')
    renaming_cols = {
        (0, '0-105 feet'): '0-105 feet',
        (0, '105-195 feet'): '105-195 feet',
        (0, '195-285 feet'): '195-285 feet',
        (0, '285-375 feet'): '285-375 feet',
        (0, '375-500 feet'): '375-500 feet'
        }

    time_sorted_df.columns = [renaming_cols.get(x, x) for x in time_sorted_df.columns]

    for idx, column_name in enumerate(time_sorted_df.columns):
        
        axs[idx].plot(time_sorted_df.index, time_sorted_df[column_name], label=concept)
        axs[idx].legend()
        axs[idx].set_title(column_name)

    # time_sorted_df.plot(ax=axs, subplots=True)

    plt.tight_layout()
    plt.show()

    time_sorted_df['total'] = time_sorted_df[list(time_sorted_df.columns)].sum(axis=1)

    time_sorted_df.plot()
    plt.show()






def conflog(scenario_list, gpkg_name, gpkg_args):

    # filter out any non reglog files
    conflog_files = [os.path.join(results_loc,f) for f in scenario_list if 'CONFLOG' in f]

    # read the files and skip the first 9 rows
    header_columns = ['time','ACID1','ACID2','LAT1','LON1','ALT1','LAT2','LON2','ALT2','CPALAT','CPALON', 'EDGEID1', 'EDGEID2']

    print(f'[green]Parsing {gpkg_name}...')
    try:

        # place all logs in a dataframe
        df = pd.concat((pd.read_csv(f, skiprows=9, header=None, names=header_columns).assign(scenario = f[8:-4]) for f in conflog_files))
        
        # convert time to datetime
        df['time'] = pd.to_datetime(df['time'], unit='s', errors='coerce')

        # convert coords to numpy array
        # convert to geodataframe
        gdf = gpd.GeoDataFrame(df, geometry=df.apply(lambda row: MultiPoint([(row['LON1'], row['LAT1']), (row['LON2'], row['LAT2'])]), axis=1), crs='epsg:4326')    

        # convert to epsg 32633
        gdf = gdf.to_crs(epsg=32633)

        # convert to a geopackage
        gpkg_fpath = os.path.join('gpkgs', gpkg_name)
        gdf.to_file(gpkg_fpath + '.gpkg', driver='GPKG')

    except ValueError:
        print('[red]Problem with these files:')
        print(scenario_list)


def loslog(scenario_list, gpkg_name, gpkg_args):

    # filter out any non reglog files
    loslog_files = [os.path.join(results_loc,f) for f in scenario_list if 'LOSLOG' in f]

    # read the files and skip the first 9 rows
    header_columns = ['exittime','starttime','timemindist','ACID1','ACID2','LAT1','LON1','ALT1','LAT2','LON2','ALT2','DIST']

    print(f'[green]Parsing {gpkg_name}...')
    try:

        # place all logs in a dataframe
        df = pd.concat((pd.read_csv(f, skiprows=9, header=None, names=header_columns).assign(scenario = f[8:-4]) for f in loslog_files))
        
        # convert time to datetime
        df['timemindist'] = pd.to_datetime(df['timemindist'], unit='s', errors='coerce')

        # convert coords to numpy array
        # convert to geodataframe
        gdf = gpd.GeoDataFrame(df, geometry=df.apply(lambda row: MultiPoint([(row['LON1'], row['LAT1']), (row['LON2'], row['LAT2'])]), axis=1), crs='epsg:4326')    

        # convert to epsg 32633
        gdf = gdf.to_crs(epsg=32633)

        # convert to a geopackage
        gpkg_fpath = os.path.join('gpkgs', gpkg_name)
        gdf.to_file(gpkg_fpath + '.gpkg', driver='GPKG')

    except ValueError:
        print('[red]Problem with these files:')
        print(scenario_list)