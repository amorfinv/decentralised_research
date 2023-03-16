import os
import pandas as pd
import config as cfg

import matplotlib.pyplot as plt 
import seaborn as sns
import matplotlib

from graph_helpers import adjust_box_widths, lighten_color
from rich import print

matplotlib.use('Agg')

# read in config
log_location = cfg.log_location
repetitions = cfg.repetitions
concepts_dict = cfg.concepts_dict
concepts_colours=sns.color_palette("hls", len(concepts_dict.items()))

            
# read as csv
new_eff_df = pd.read_csv('efficiency_df.csv')

fig = plt.figure()

# make the transition types as percentage of totals conflict tansitions
for metric, metric_name in cfg.flst_metrics.items():

    sns.boxplot(
        y=metric,
        x='density',
        data=new_eff_df,
        palette=concepts_colours,
        hue='concept'
    )

    plt.ylabel(f'{metric_name} efficiency [%]')
    
    plt.legend(loc='upper right')

    if metric == 'Distance ALT':
        plt.ylim(-5, 105)
    elif metric == 'Flight time':
        plt.ylim(-10, 2)
    elif metric == 'Distance 3D':
        plt.ylim(-2, 10)


    adjust_box_widths(fig, 0.5)

    plt.savefig(f'images/{metric}_eff',bbox_inches='tight')
    plt.clf()                              
