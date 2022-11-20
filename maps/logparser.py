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
from itertools import islice
from copy import deepcopy

# ignore warnings with the way the gdf is created
import warnings
warnings.filterwarnings('ignore')


def logparse(args):
    
    for i in track(range(len(args['combinations'])), description="Processing..."):
        scn_comb = args['combinations'][i]
            
        # get global parameters for current combination
        gpkg_args = {'logtype':scn_comb[0], 'density':scn_comb[1], 'concept':scn_comb[2]}

        # make the name of gpkg
        gpkg_name = '_'.join(scn_comb)

        # get the log file names
        log_prefix = scn_comb[0] + '_Flight_intention_' + scn_comb[1] + '_40_'
        log_suffix = '_' + scn_comb[2] + '.log'
        scenario_list = [f'{log_prefix}{i}{log_suffix}' for i in range(9)]
    
        if gpkg_args['logtype'] == 'REGLOG':
            # check if the file exists
            if os.path.exists(os.path.join('gpkgs', gpkg_name + '.gpkg')):
                print(f'[bright_black]gpkgs/{gpkg_name}.gpkg already exists, skipping.')
                continue

            reglog(scenario_list, gpkg_name, gpkg_args)

        if gpkg_args['logtype'] == 'CONFLOG':
            # check if the file exists
            if os.path.exists(os.path.join('gpkgs', gpkg_name + '.gpkg')):
                print(f'[bright_black]gpkgs/{gpkg_name}.gpkg already exists, skipping.')
                continue

            conflog(scenario_list, gpkg_name, gpkg_args)

        if gpkg_args['logtype'] == 'LOSLOG':
            # check if the file exists
            if os.path.exists(os.path.join('gpkgs', gpkg_name + '.gpkg')):
                print(f'[bright_black]gpkgs/{gpkg_name}.gpkg already exists, skipping.')
                continue

            loslog(scenario_list, gpkg_name, gpkg_args)



def reglog(scenario_list, gpkg_name, gpkg_args):

    # filter out any non reglog files
    reglog_files = [os.path.join('results',f) for f in scenario_list if 'REGLOG' in f]

    # read the files and skip the first 9 rows
    header_columns = ['ACID','ALT','LATS','LONS','EDGE_ID']
    header_2 = ['ACID','ALT','LATS','LONS','EDGE_ID','scenario']

    # get the start date
    data = {}

    # each time stamp should have four entries
    time_stamp_entries = dict()

    # frest reglog creates general log
    print(f'[green]Parsing {gpkg_name}')

    # read the grahpml of streets
    G = ox.load_graphml('other_data/finalized_graph.graphml')
    edge_gdf = ox.graph_to_gdfs(G, nodes=False)
    edge_gdf['edge_id'] = edge_gdf.index
    edge_geometry = nx.get_edge_attributes(G, "geometry")

    try:
        for idx, filepath in enumerate(reglog_files):
            day = idx + 1
            date = datetime.strptime(f'2022-01-{day}',"%Y-%m-%d")
            
            with open(filepath, 'r') as infile:
                # skip first 9 lines of file
                lines_gen = islice(infile, 9, None)
                
                # loop through five lines at time
                slice_size = 5
                entry = 0
                for acids, alts, lats, lons, edgeids in zip(*[iter(lines_gen)]*slice_size):
                    
                    time = float(acids.split(',')[0])
                    time_stamp = str(date + timedelta(seconds=time))

                    acids = acids.strip().split(',')[1:]
                    alts = alts.strip().split(',')[1:]
                    lats = lats.strip().split(',')[1:]
                    lons = lons.strip().split(',')[1:]
                    edgeids = edgeids.strip().split(',')[1:]
                    edgeids_float = [tuple(map(int, edge.split('-'))) + (0,) for edge in edgeids]
                    edge_geom = list(map(edge_geometry.get, edgeids_float))
    

                    for acidx, acid in enumerate(acids):
                        data[entry] = {
                            'time_stamp': time_stamp,
                            'seconds': time,
                            'ACID': acid,
                            'ALT': float(alts[acidx]),
                            'geometry': Point(float(lons[acidx]), float(lats[acidx])),
                            'edge_id': edgeids_float[acidx],
                            'scenario': filepath[32:-4],
                            'edge_geometry': edge_geom[acidx]
                            }

                        entry += 1

        # convert to a geodataframe
        df = pd.DataFrame(data).T
        
        # save the geometry of the points
        gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
        gdf = gdf.to_crs(epsg=32633)
        gdf = gdf.drop(columns=['edge_id','edge_geometry'])
        gpkg_fpath = os.path.join('gpkgs', gpkg_name)
        gdf.to_file(gpkg_fpath + '.gpkg', driver='GPKG', layer=f'points_{gpkg_name}')

        # analyze heights if m2 or headallocnoflow in name
        if 'm2' in gpkg_name or 'headallocnoflow' in gpkg_name:
            # save a gdf for edges
            edge_df = df.dropna()
            edge_df['geometry'] = edge_df['edge_geometry']

            # first step is to remove time for now TODO: later maybe include for animation
            edge_df = edge_df[edge_df['seconds'] <= 5400]
            edge_df = edge_df.drop(columns=['time_stamp', 'seconds', 'ACID', 'edge_geometry', 'scenario'])

            # now slice the dataframe into altitude bins
            alt_bins = [0, 105, 195, 285, 375, 500]
            
            final_edge_gdf = deepcopy(edge_gdf)
            final_edge_gdf = final_edge_gdf.drop(columns=['oneway', 'length', 'bearing', 'stroke_group', 'edge_interior_angle',
            'layer_allocation', 'bearing_diff', 'height_allocation', 'edge_id', 'flow_group'])
            for idx, lower_alt in enumerate(alt_bins[:-1]):
                upper_alt = alt_bins[idx+1]
                sliced_df = edge_df[((edge_df['ALT'] >= lower_alt) & (edge_df['ALT'] < upper_alt))]
                edge_counts = sliced_df.groupby(by=['edge_id']).size()
                sliced_gdf = deepcopy(edge_gdf)
                sliced_gdf['count'] = sliced_gdf['edge_id'].map(edge_counts)
                sliced_gdf['count'] = sliced_gdf['count'].fillna(0)

                final_edge_gdf[f'count_bin_{idx}'] = sliced_gdf['count']

            gpkg_fpath = os.path.join('gpkgs', gpkg_name)
            final_edge_gdf.to_file(gpkg_fpath + '.gpkg', driver='GPKG', layer=f'edge_{gpkg_name}')
        

    except ValueError:
        print('[red]Problem with these files:')
        print(scenario_list)


def conflog(scenario_list, gpkg_name, gpkg_args):

    # filter out any non reglog files
    conflog_files = [os.path.join('results',f) for f in scenario_list if 'CONFLOG' in f]

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
    loslog_files = [os.path.join('results',f) for f in scenario_list if 'LOSLOG' in f]

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