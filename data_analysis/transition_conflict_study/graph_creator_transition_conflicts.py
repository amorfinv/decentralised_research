import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import matplotlib
from rich import print

from graph_helpers import adjust_box_widths
import config as cfg

# some plot defaults
matplotlib.use('Agg')
concepts_colours=sns.color_palette("hls", len(cfg.concepts_dict.keys()))
            
# read as csv
new_conf_df = pd.read_csv('conflict_df.csv')
new_trans_df = pd.read_csv('inter_trans_df.csv')
percent_conf_df = pd.read_csv('percent_conflict.csv')

fig = plt.figure()

# make the transition types as percentage of totals conflict tansitions
for metric in cfg.transition_types:

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
    data=new_conf_df,
    palette=concepts_colours,
    hue='concept'
)

plt.ylabel(f'Conflicts in constrained airspace\nattributed to a transition [-]')
# plt.ylabel(f'Perent of conflicts in constrained airspace\nattributed to a transition [%]')
plt.legend(loc='upper left')
# plt.ylim(-5, 105)
adjust_box_widths(fig, 0.5)
# plt.savefig(f'images/percent_total_trans',bbox_inches='tight')
plt.savefig(f'images/total_trans',bbox_inches='tight')
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
for metric in cfg.transition_types[1:]:

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