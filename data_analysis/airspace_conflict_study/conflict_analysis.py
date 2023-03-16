import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
from pyproj import Transformer
import matplotlib
from shapely.geometry import Point

from graph_helpers import adjust_box_widths
from constrained import constrained_airspace
import config as cfg

# set matplotlib and seaborn default
matplotlib.use('Agg')
concepts_colours=sns.color_palette("hls", len(cfg.concepts_dict.keys()))

# set the transformer from lat lon to utm
transformer = Transformer.from_crs(4326, 32633)

# create a LOS and CONF dataframe to populate
conf_cols = ['density', 'concept', 'repetition'] + cfg.conf_metrics
los_cols = ['density', 'concept', 'repetition'] + cfg.los_metrics

conf_df = pd.DataFrame(columns=conf_cols)
los_df = pd.DataFrame(columns=los_cols)

for density, density_name in cfg.density_dict.items():

    for concept, concept_name in cfg.concepts_dict.items():

        for repetition in cfg.repetitions:
            
            # first get the number of aircraft in the air
            n_air = cfg.ac_in_constrained_dict[density][str(repetition)]['num_ac_constrained']

            # CONFLOG

            # get the scenario name and open the file
            scenario = f'Flight_intention_{density}_40_{repetition}_{concept}.log'
            with open(f'{cfg.log_location}/CONFLOG_{scenario}') as f:
                confs = f.readlines()[9:]

            # initialize some variables for conflicts and process the logs
            total_confs = 0

            for conf in confs:

                # split log based on comma
                conf = conf.split(',')

                # only process constrained airspace conflicts
                airspace_type_1 = conf[11]
                airspace_type_2 = conf[12]

                if airspace_type_1 == 'open' or airspace_type_2 == 'open':
                    continue
                
                # sum total number of conflicts
                total_confs += 1

            # get conflict data in dataframe
            df_conf_scn = pd.DataFrame(
                [
                    [
                        density_name,
                        concept_name,
                        repetition,
                        total_confs,
                        total_confs/n_air

                    ]
                ],
                columns=conf_cols
            )

            # concat dataframes
            conf_df = pd.concat([conf_df, df_conf_scn])

            # LOSLOG
            with open(f'{cfg.log_location}/LOSLOG_{scenario}') as f:
                losses = f.readlines()[9:]
            
            # initialize some data for conflicts and process them
            total_los = 0

            for los in losses:
                # split log based on comma

                los = los.split(',')

                lat_1 = float(los[5])
                lon_1 = float(los[6])

                lat_2 = float(los[8])
                lon_2 = float(los[9])

                p_1 = Point(transformer.transform(lat_1, lon_1))
                p_2 = Point(transformer.transform(lat_2, lon_2))

                if not constrained_airspace.contains(p_1) and not constrained_airspace.contains(p_2):
                    continue

                total_los += 1


            # get los data in dataframe
            df_los_scn = pd.DataFrame(
                [
                    [
                        density_name,
                        concept_name,
                        repetition,
                        total_los,
                    ]
                ],
                columns=los_cols
            )
            los_df = pd.concat([los_df, df_los_scn])



fig = plt.figure()

for metric in cfg.conf_metrics:
    
    sns.boxplot(
        y=metric,
        x='density',
        data=conf_df,
        palette=concepts_colours,
        hue='concept'
    )

    plt.ylabel(f'{metric} in constrained airspace [-]')
    plt.legend(loc='upper left')
    adjust_box_widths(fig, 0.5)

    plt.savefig(f'images/{metric}',bbox_inches='tight')
    plt.clf()

for metric in cfg.los_metrics:

    sns.boxplot(
        y=metric,
        x='density',
        data=los_df,
        palette=concepts_colours,
        hue='concept'
    )

    plt.ylabel(f'{metric} in constrained airspace [-]')
    plt.legend(loc='upper left')
    adjust_box_widths(fig, 0.5)

    plt.savefig(f'images/{metric}',bbox_inches='tight')
    plt.clf()
