import os
from rich import print
from rich.progress import track
import pandas as pd
from datetime import timedelta, datetime
from shapely.geometry import MultiPoint
import geopandas as gpd
import numpy as np

# ignore warnings with the way the gdf is created
import warnings
warnings.filterwarnings('ignore')


def logparse(args):
    
    conf_layer_dfs = {}
    conf_alt_dfs = {}

    for i in track(range(len(args['combinations'])), description="Processing..."):
        scn_comb = args['combinations'][i]
        
        # get global parameters for current combination
        logtype = scn_comb[0]
        density = scn_comb[1]
        concept = scn_comb[2]

        if density not in conf_layer_dfs:
            conf_layer_dfs[density] = {}
            conf_alt_dfs[density] = {}

        parse_args = {'logtype':logtype, 'density':density, 'concept':concept}

        # make the name of dataset entry
        dataset_name = '_'.join(scn_comb)

        # get the log file names
        log_prefix = scn_comb[0] + '_Flight_intention_' + scn_comb[1] + '_40_'
        log_suffix = '_' + scn_comb[2] + '.log'
        scenario_list = [f'{log_prefix}{i}{log_suffix}' for i in range(9)]
    
        if logtype == 'REGLOG':
            log_args = reglog(scenario_list, dataset_name, parse_args)

        if logtype == 'CONFLOG':
            layer_type_confs,altitude_confs = conflog(scenario_list, dataset_name, parse_args)            
            # add concept column and density column 
            conf_layer_dfs[density][concept] = layer_type_confs
            conf_alt_dfs[density][concept] = altitude_confs

        if logtype == 'LOSLOG':
            loslog(scenario_list, dataset_name, parse_args)

    
    plot_df = {}
    if 'CONFLOG' in args['logtype']:
        # merge the dataframes to a big one of conf_layer_dfs
        conf_df = pd.DataFrame(columns=['scenario', 'layertype', 'count', 'concept', 'density'])
        for density, conf_layer_df in conf_layer_dfs.items():
            for concept, unique_df in conf_layer_df.items():
                # append to the dataframe
                conf_df = conf_df.append(unique_df)

        # merge the dataframes to a big one of conf_alt_dfs
        alt_df = pd.DataFrame(columns=['scenario', 'altitudebins', 'count', 'concept', 'density'])
        for density, conf_alt_df in conf_alt_dfs.items():
            for concept, unique_df in conf_alt_df.items():
                # append to the dataframe
                alt_df = alt_df.append(unique_df)
        
        plot_df['CONFLOG'] = {'LAYERTYPES': conf_df, 'ALTITUDEBINS': alt_df}
    
    return plot_df



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

    print(f'[green]Parsing {gpkg_name}')
    try:

        for idx, filepath in enumerate(reglog_files):
            day = idx + 1
            date = datetime.strptime(f'2022-01-{day}',"%Y-%m-%d")

            with open(filepath) as f:
                for line_num, line in enumerate(f):
                    if line_num < 9:
                        continue
                    header_id = (line_num - 9) % 5

                    # get the time
                    sec_sim = float(line.split(',')[0])
                    time_stamp = str(date + timedelta(seconds=sec_sim))
                    if header_id == 0:
                        # make a dictionary wth values for each header_column
                        data[time_stamp] = {header_col:[] for header_col in header_2}            
                        data[time_stamp][header_columns[header_id]] = line.strip('\n').split(',')[1:]
                        data[time_stamp]['scenario'] = filepath[len('results')+1:] 
                    elif header_id == 4:
                        data[time_stamp][header_columns[header_id]] = [i for i in line.strip('\n').split(',')[1:]]
                    else:
                        data[time_stamp][header_columns[header_id]] = [float(i) for i in line.strip('\n').split(',')[1:]]

                    
                    # create a check to see if the data is complete.
                    time_stamp_entries[time_stamp] = time_stamp_entries.get(time_stamp, 0) + 1

        # get a dataframe of the entries
        df_time_entries = pd.DataFrame(time_stamp_entries, index=['count']).T

        # convert to pandas dataframe where the index is the data keys and the columns are the header columns
        df = pd.DataFrame(data).T

        # remove entries from df that have a value less than 4 in the df_time_entries
        df = df[df_time_entries['count'] >= 4]

        multi_point = np.array([MultiPoint(np.column_stack((x, y))) for x,y in zip(df['LONS'], df['LATS'])], dtype=MultiPoint)

        # remove ACID, LAT, LON, ALT columns
        df.drop(columns=['ACID','LATS', 'LONS', 'EDGE_ID', 'ALT'], inplace=True)
        # make a geodataframe from the pandas dataframe
        gdf = gpd.GeoDataFrame(df, geometry=multi_point, crs='epsg:4326')

        # set the index as a column
        gdf['date'] = gdf.index
        gdf['date']= pd.to_datetime(gdf['date'])

        # reset index
        gdf.reset_index(inplace=True)

        # convert to epsg 32633
        gdf = gdf.to_crs(epsg=32633)

        # convert to a geopackage
        gpkg_fpath = os.path.join('gpkgs', gpkg_name)
        gdf.to_file(gpkg_fpath + '.gpkg', driver='GPKG')

    except ValueError:
        print('[red]Problem with these files:')
        print(scenario_list)


def conflog(scenario_list, dataset_name, parse_args):

    # filter out any non reglog files
    conflog_files = [os.path.join('results',f) for f in scenario_list if 'CONFLOG' in f]

    # read the files and skip the first 9 rows
    header_columns = ['time', 'ACID1', 'ACID2', 'LAT1', 'LON1', 'ALT1', 'LAT2', 'LON2', 'ALT2', 'CPALAT', 'CPALON', 'AIRSPACETYPE1', 'AIRSPACETYPE2', 'LAYERTYPE1', 'LAYERTYPE2', 'EDGEID1', 'EDGEID2']

    concept = parse_args['concept']
    density = parse_args['density']
    print(f'[green]Parsing {dataset_name}...')
    try:

        # place all logs in a dataframe
        df = pd.concat((pd.read_csv(f, skiprows=9, header=None, names=header_columns).assign(scenario = f[8:-4]) for f in conflog_files))
        
        # convert time to datetime
        df['time'] = pd.to_datetime(df['time'], unit='s', errors='coerce')

        # convert coords to numpy array
        # convert to geodataframe
        # df = gpd.GeoDataFrame(df, geometry=df.apply(lambda row: MultiPoint([(row['LON1'], row['LAT1']), (row['LON2'], row['LAT2'])]), axis=1), crs='epsg:4326')    

        # look at column "AIRSPACETYPE1" and "AIRSPACETYPE2". Only keep the rows if they are both "constrained"
        df = df[(df['AIRSPACETYPE1'] == 'constrained') & (df['AIRSPACETYPE2'] == 'constrained')]

        # go through layertype1 and layertype2 and check if one is a NAN, if so replace the value with 'S'
        df['LAYERTYPE1'] = df['LAYERTYPE1'].fillna('S')
        df['LAYERTYPE2'] = df['LAYERTYPE2'].fillna('S')

        # look at column "LAYERTYPE1" and "LAYERTYPE2" and sort them depending on the values
        # LAYERTYPE1 = "C" and LAYERTYPE2 = "C" -> "C-C"
        # LAYERTYPE1 = "S" and LAYERTYPE2 = "S" -> "S-S"
        # LAYERTYPE1 = "T" and LAYERTYPE2 = "T" -> "T-T"
        # LAYERTYPE1 = "F" and LAYERTYPE2 = "F" -> "F-F"
        # LAYERTYPE1 = "C" and LAYERTYPE2 = "T" -> "C-T"
        # LAYERTYPE1 = "T" and LAYERTYPE2 = "C" -> "C-T"
        # LAYERTYPE1 = "C" and LAYERTYPE2 = "F" -> "C-F"
        # LAYERTYPE1 = "F" and LAYERTYPE2 = "C" -> "C-F"
        # LAYERTYPE1 = "F" and LAYERTYPE2 = "T" -> "F-T"
        # LAYERTYPE1 = "T" and LAYERTYPE2 = "F" -> "F-T"
        # LAYERTYPE1 = "S" and LAYERTYPE2 = "C" -> "C-S"
        # LAYERTYPE1 = "C" and LAYERTYPE2 = "S" -> "C-S"
        # LAYERTYPE1 = "S" and LAYERTYPE2 = "T" -> "S-T"
        # LAYERTYPE1 = "T" and LAYERTYPE2 = "S" -> "S-T"
        # LAYERTYPE1 = "S" and LAYERTYPE2 = "F" -> "F-S"
        # LAYERTYPE1 = "F" and LAYERTYPE2 = "S" -> "F-S"
        df['layertype'] = df.apply(lambda row: row['LAYERTYPE1'] + '-' + row['LAYERTYPE2'] if row['LAYERTYPE1'] < row['LAYERTYPE2'] else row['LAYERTYPE2'] + '-' + row['LAYERTYPE1'], axis=1)

        # get the layer type conflict counts
        layer_type_confs = df.groupby(by=['scenario','layertype']).size()

        # make into a dataframe and make index into columns and name column count
        layer_type_confs = layer_type_confs.to_frame().reset_index().rename(columns={0:'count'})
        layer_type_confs['concept'] = concept
        layer_type_confs['density'] = density

        # check if any of these are missing per scenario and add it with a value of 0
        conflict_types = ['C-C', 'S-S', 'T-T', 'F-F', 'C-T', 'C-F', 'F-T', 'C-S', 'S-T', 'F-S']
        for scenario in df['scenario'].unique():
            for conflict_type in conflict_types:
                if conflict_type not in layer_type_confs[layer_type_confs['scenario'] == scenario]['layertype'].unique():
                    layer_type_confs = layer_type_confs.append({'scenario': scenario, 'layertype': conflict_type, 'count': 0, 'concept': concept, 'density': density}, ignore_index=True)

        # add a new column called 'repetition' that takes the 'scenario' string and splits it on the underscore and takes the last value
        layer_type_confs['repetition'] = layer_type_confs['scenario'].apply(lambda x: x.split('_')[-2])
        
        # another interesting study would be to look at the altitude differences between conflicts
        df['ALT_DIFF'] = df.apply(lambda row: abs(row['ALT1'] - row['ALT2']), axis=1)
        
        # create some altitude bins to place alt-diff values in 0-9.144, 9.144-18.288, 18.288-27.432, 27.432-36.576, 36.576-45.72, 45.72-150
        df['altitudebins'] = pd.cut(df['ALT_DIFF'], bins=[0, 9.144, 18.288, 27.432, 36.576, 45.72, 150], labels=['0L', '1L', '2L', '3L', '4L', '>4L'])
        
        altitude_confs = df.groupby(by=['scenario','altitudebins']).size()
        altitude_confs = altitude_confs.to_frame().reset_index().rename(columns={0:'count'})
        altitude_confs['concept'] = concept
        altitude_confs['density'] = density

        return layer_type_confs, altitude_confs

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