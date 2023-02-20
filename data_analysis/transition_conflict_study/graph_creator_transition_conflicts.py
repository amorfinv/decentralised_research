import os
import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt 
import seaborn as sns
import matplotlib

from graph_helpers import adjust_box_widths, lighten_color
from rich import print

matplotlib.use('Agg')

# Log locations
log_location = 'logs'
concepts = ['noflow', 'noflowfulldenalloc','noflowrandomalloc', 'noflowdistalloc']
densities = ['very_low', 'low', 'medium', 'high', 'ultra']
repetitions = range(0,9)

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
new_trans_cols = ['density', 'concept', 'repetition'] + transition_types[1:]

            
# read as csv
new_conf_df = pd.read_csv('conflict_df.csv')
new_trans_df = pd.read_csv('inter_trans_df.csv')

percent_conf_df = pd.read_csv('percent_conflict.csv')

fig = plt.figure()

# make the transition types as percentage of totals conflict tansitions
for metric in transition_types:

    if metric == 'CR1':

        new_conf_df['CR'] = new_conf_df['CR1'] + new_conf_df['CR2']

        sns.boxplot(
            y='CR',
            x='density',
            data=new_conf_df,
            palette=concepts_colours,
            hue='concept'
        )
        plt.ylabel(f'CR transitions as a percentage\n of total conflict causing transitions ')

    elif metric == 'CR2':
        continue
    else:
    
        sns.boxplot(
            y=metric,
            x='density',
            data=new_conf_df,
            palette=concepts_colours,
            hue='concept'
        )

        plt.ylabel(f'{metric} transitions as a percentage\n of total conflict causing transitions ')
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    adjust_box_widths(fig, 0.5)

    # if metric != 'Total':
    plt.ylim(-5, 105)

    plt.savefig(f'images/{metric}_confs',bbox_inches='tight')
    plt.clf()                              

# make image of number of conflicts attributed to transitions
conflict_transition_plot = sns.boxplot(
    y='Unique transitions',
    x='density',
    data=percent_conf_df,
    palette=concepts_colours,
    hue='concept'
)

# plt.ylabel(f'Conflicts in constrained airspace\nattributed to a transition [-]')
plt.ylabel(f'Perent of conflicts in constrained airspace\nattributed to a transition [%]')
plt.legend(loc='upper right')
plt.ylim(-5, 105)
adjust_box_widths(fig, 0.5)
plt.savefig(f'images/percent_total_trans',bbox_inches='tight')
# plt.savefig(f'images/total_trans',bbox_inches='tight')
plt.clf()    

# make image of percentage of transitions that cause conflicts
sns.boxplot(
    y='Total Transitions',
    x='density',
    data=new_conf_df,
    palette=concepts_colours,
    hue='concept'
)
plt.ylabel(f'Percent of transitions that cause conflicts')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
adjust_box_widths(fig, 0.5)
# plt.ylim(-5, 105)
plt.savefig(f'images/unique_confs',bbox_inches='tight')
plt.clf()   

# make interrupted transitions
# make the transition types as percentage of totals conflict tansitions
for metric in transition_types[1:]:

    if metric == 'CR1':

        new_trans_df['CR'] = new_trans_df['CR1'] + new_trans_df['CR2']

        sns.boxplot(
            y='CR',
            x='density',
            data=new_trans_df,
            palette=concepts_colours,
            hue='concept'
        )
        plt.ylabel(f'Interrupted CR transitions percentage')

    elif metric == 'CR2':
        continue
    else:
    
        sns.boxplot(
            y=metric,
            x='density',
            data=new_trans_df,
            palette=concepts_colours,
            hue='concept'
        )

        plt.ylabel(f'Interrupted {metric} transitions percentage')
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    adjust_box_widths(fig, 0.5)

    # if metric != 'Total':
    # plt.ylim(-5, 105)

    plt.savefig(f'images/{metric}_interupted',bbox_inches='tight')
    plt.clf()    