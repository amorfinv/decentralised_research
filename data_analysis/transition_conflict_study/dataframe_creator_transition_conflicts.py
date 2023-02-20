import os
import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.patches import PathPatch
import matplotlib
import matplotlib.colors as mc
import colorsys

from rich import print

matplotlib.use('Agg')

# Log locations
log_location = 'logs'
concepts = ['noflow', 'noflowfulldenalloc','noflowrandomalloc', 'noflowdistalloc']
densities = ['very_low', 'low', 'medium', 'high', 'ultra']
repetitions = range(0,9)

density_dict = {
    'very_low': 'very low',
    'low': 'low',
    'medium': 'medium',
    'high': 'high',
    'ultra': 'ultra'
}


concepts_dict = {
    'noflow'                : 'Baseline',
    'noflowfulldenalloc'    : 'Density allocation',
    'noflowrandomalloc'     : 'Random allocation',
    'noflowdistalloc'       : 'Distance allocation',
}

concepts_colours=sns.color_palette("hls", len(concepts))


# STEP 1 read in the conflict log
conflict_columns = [
    'time',
    'ACID1',
    'ACID2',
    'LAT1',
    'LON1',
    'ALT1',
    'LAT2',
    'LON2',
    'ALT2',
    'CPALAT',
    'CPALON',
    'AIRSPACETYPE1',
    'AIRSPACETYPE2',
    'LAYERTYPE1',
    'LAYERTYPE2',
    'EDGEID1',
    'EDGEID2',
    'AIRSPACEALLOC1',
    'AIRSPACEALLOC2',
    ]

transition_columns = [
    'end_transition_time',
    'start_transition_time',
    'ACID',
    'transition_type',
    'intended_transition_type',
    'start_alt',
    'end_alt',
    'start_conf_search',
    'end_conf_search',
]

# LOG types
transition_types = [
    'Interrupted',
    'Recover',
    'CR1',
    'CR2',
    'Hopping up',
    'Hopping down',
    'Cruise to Turn',
    'Turn to Cruise',
    'Takeoff',
    'Free',
    'Missed'
]

cols = ['density', 'concept', 'repetition', 'Total Conflicts', 'Total Transitions', 'Unique transitions'] + transition_types
new_conf_df = pd.DataFrame(columns=cols)
percent_new_conf_df = pd.DataFrame(columns=cols)

new_trans_cols = ['density', 'concept', 'repetition'] + transition_types[1:]
new_trans_df = pd.DataFrame(columns=new_trans_cols)

for density in densities:

    for concept in concepts:

        for repetition in repetitions:
            
            # read in conflict log and get dataframe
            conf_log = f'{log_location}/CONFLOG_Flight_intention_{density}_40_{repetition}_{concept}.log'
            conf_df = pd.read_csv(conf_log, skiprows=9, header=None, names=conflict_columns)
            conf_df['time'] = pd.to_datetime(conf_df['time'], unit='s', errors='coerce')
            
            # only select dataframes where conflicts are in constrained
            conf_df = conf_df[(conf_df['AIRSPACETYPE1']=='constrained') & (conf_df['AIRSPACETYPE2'] == 'constrained')]
            conf_df = conf_df[['time', 'ACID1', 'ACID2']]

            # This last section of CONFLOG removes duplicate conflicts
            # first rearrange ACID1 and ACID2 so smallest value is ACID1
            conf_df['ACID1'], conf_df['ACID2'] = np.where(conf_df['ACID1'] > conf_df['ACID2'], (conf_df['ACID2'], conf_df['ACID1']), (conf_df['ACID1'], conf_df['ACID2']))
            conf_df = conf_df.sort_values(by=['time', 'ACID1', 'ACID2'])

            conf_df['duplicate_conf'] = False

            for i, row in conf_df.iterrows():
                acid_1 = row['ACID1']
                acid_2 = row['ACID2']

                # create temporary dataframe with data up to current value
                temp_df = conf_df.loc[:i]

                # remove anything with time greater than 10 seconds
                temp_df = temp_df[np.abs(temp_df['time'] - row['time']) <= pd.Timedelta(seconds=10)]

                
                # check if there is a duplicate ACIDs
                temp_df = temp_df.duplicated(subset=['ACID1', 'ACID2'])

                # print(time_diff)
                if temp_df.loc[i]:
                    conf_df.at[i,'duplicate_conf'] = True

            conf_df = conf_df[~conf_df['duplicate_conf']]


            # read in transition log and get dataframe
            trans_log = f'{log_location}/TRANSLOG_Flight_intention_{density}_40_{repetition}_{concept}.log'

            trans_df = pd.read_csv(trans_log, skiprows=9, header=None, names=transition_columns)
            trans_df['start_transition_time'] = pd.to_datetime(trans_df['start_transition_time'], unit='s', errors='coerce')
            trans_df['end_transition_time'] = pd.to_datetime(trans_df['end_transition_time'], unit='s', errors='coerce')
            trans_df['start_conf_search'] = pd.to_datetime(trans_df['start_conf_search'], unit='s', errors='coerce')
            trans_df['end_conf_search'] = pd.to_datetime(trans_df['end_conf_search'], unit='s', errors='coerce')

            # for each transition see if there is a conflict within a certain time
            search_start_time = 'start_conf_search'
            search_end_time = 'end_conf_search'
            
            # Now merge daframes so that time can be compares
            merged_df = pd.merge(trans_df, conf_df, left_on='ACID', right_on='ACID1', how='outer')
            merged_df = pd.merge(merged_df, conf_df, left_on='ACID', right_on='ACID2', how='outer')

            # now we combine rows of the merge
            merged_df['conf_time'] = merged_df['time_x'].fillna(merged_df['time_y'])
            merged_df['ACID1'] = merged_df['ACID1_x'].fillna(merged_df['ACID1_y'])
            merged_df['ACID2'] = merged_df['ACID2_x'].fillna(merged_df['ACID2_y'])

            # compare the time
            merged_df = merged_df[merged_df['conf_time'].between(merged_df[search_start_time], merged_df[search_end_time])]

            # rename to only keep the original format
            filled_df = merged_df[
                                    [
                                        search_start_time, 
                                        search_end_time, 
                                        'ACID',
                                        'transition_type',                        
                                        'intended_transition_type',
                                        'conf_time',
                                        'ACID1',
                                        'ACID2',                                        
                                        ]
                                ]

            # total conflicts attributed to transitions
            # Note that two transitions may lead to one a conflict
            # this count gets a total count of how one transitions to one conflict
            unique_trans_confs = filled_df.drop_duplicates(subset=['conf_time', 'ACID1', 'ACID2']).shape[0]

            # Drop duplicates with complete row
            # Here you may get two transitions getting the same conflict
            # so here we get more data but we get importance of transition
            filled_df.drop_duplicates(inplace=True)
            
            # Now start counting
            total_trans_confs = filled_df.shape[0]
            total_confs = conf_df.shape[0]


            # get conflict data in dataframe (percentages)
            percent_df_conf_scn = pd.DataFrame(
                [
                    [
                        density_dict[density],
                        concepts_dict[concept],
                        repetition,
                        total_confs,
                        total_trans_confs/trans_df.shape[0],
                        unique_trans_confs/total_confs*100,
                        *[filled_df[filled_df['transition_type'] == i].shape[0]/total_trans_confs*100 for i in range(1,12)]
                    ]
                ],
                columns=cols
            )
            percent_new_conf_df = pd.concat([percent_new_conf_df, percent_df_conf_scn])

            # get conflict data in dataframe (no percentages)
            df_conf_scn = pd.DataFrame(
                [
                    [
                        density_dict[density],
                        concepts_dict[concept],
                        repetition,
                        total_confs,
                        total_trans_confs/trans_df.shape[0],
                        unique_trans_confs,
                        *[filled_df[filled_df['transition_type'] == i].shape[0] for i in range(1,12)]
                    ]
                ],
                columns=cols
            )

            # concat dataframes
            new_conf_df = pd.concat([new_conf_df, df_conf_scn])

            # now get the percentages of transitions that lead to conflitcts
            interrupted_transition_df = filled_df[filled_df['transition_type'] == 1]
            num_interrupted = interrupted_transition_df.shape[0]
            interrupted_trans_data = []
            for i in range(2,12):
                num_intented = interrupted_transition_df[interrupted_transition_df['intended_transition_type'] == i].shape[0]
                interrupted_trans_data.append(num_intented/num_interrupted*100)

            df_trans_scn = pd.DataFrame([
                [
                        density_dict[density],
                        concepts_dict[concept],
                        repetition,
                        *interrupted_trans_data

                ]
            ],
            columns=new_trans_cols
            )
            # print(df_trans_scn)
            new_trans_df = pd.concat([new_trans_df, df_trans_scn])
            

# save new_conf_df as csv
new_conf_df.to_csv('conflict_df.csv', index=False)
percent_new_conf_df.to_csv('percent_conflict.csv', index=False)
new_trans_df.to_csv('inter_trans_df.csv', index=False)
