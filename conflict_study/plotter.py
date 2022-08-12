from rich import print, inspect, progress
from rich.progress import Progress
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import timedelta

def plotter(args, plot_dict):    

    if 'CONFLOG' in args['logtype']:
        # LAYERTYPES plotting
        layertypes_df = plot_dict['CONFLOG']['LAYERTYPES']

        # option 1 is to plot x-axis as density and give one plot per layer type
        densities = layertypes_df['density'].unique()

        # option 2 is to plot x-axis as layer type and give one plot per density
        layertypes = layertypes_df['layertype'].unique()

        # if option 1 loop through layer types
        for layertype in layertypes:
            # get the data for this layer type
            layertype_df = layertypes_df[layertypes_df['layertype'] == layertype]
            
            plot_title = f'confs/layertype_{layertype}'
            # plot the data
            sea_plotter(df=layertype_df, df_col='density', xlabels=densities, title=plot_title)

        
        for density in densities:
            #get the data for this density
            density_df = layertypes_df[layertypes_df['density'] == density]

            plot_title = f'confs/density_{density}_ltypes'
            
            # plot the data
            sea_plotter(df=density_df, df_col='layertype', xlabels=layertypes, title=plot_title)

        # ALTITUDE plotting
        alt_df = plot_dict['CONFLOG']['ALTITUDEBINS']

        # option 1 is to plot x-axis as density and give one plot per altitude bin
        densities = alt_df['density'].unique()

        # option 2 is to plot x-axis as altitude bin and give one plot per density
        altbins = alt_df['altitudebins'].unique()

        # if option 1 loop through layer types
        for altbin in altbins:
            # get the data for this layer type
            altbin_df = alt_df[alt_df['altitudebins'] == altbin]
            
            plot_title = f'confs/altitudebin_{altbin}'
            # plot the data
            sea_plotter(df=altbin_df, df_col='density', xlabels=densities, title=plot_title)
        
        for density in densities:
            #get the data for this density
            density_df = alt_df[alt_df['density'] == density]

            plot_title = f'confs/density_{density}_altbins'
            
            # plot the data
            sea_plotter(df=density_df, df_col='altitudebins', xlabels=altbins, title=plot_title)


    if 'LOSLOG' in args['logtype']:
        # LAYERTYPES plotting
        layertypes_df = plot_dict['LOSLOG']['LAYERTYPES']

        # option 1 is to plot x-axis as density and give one plot per layer type
        densities = layertypes_df['density'].unique()

        # option 2 is to plot x-axis as layer type and give one plot per density
        layertypes = layertypes_df['layertype'].unique()

        # if option 1 loop through layer types
        for layertype in layertypes:
            # get the data for this layer type
            layertype_df = layertypes_df[layertypes_df['layertype'] == layertype]
            
            plot_title = f'los/layertype_{layertype}'
            # plot the data
            sea_plotter(df=layertype_df, df_col='density', xlabels=densities, title=plot_title)

        
        for density in densities:
            #get the data for this density
            density_df = layertypes_df[layertypes_df['density'] == density]

            plot_title = f'los/density_{density}_ltypes'
            
            # plot the data
            sea_plotter(df=density_df, df_col='layertype', xlabels=layertypes, title=plot_title)

        # ALTITUDE plotting
        alt_df = plot_dict['LOSLOG']['ALTITUDEBINS']

        # option 1 is to plot x-axis as density and give one plot per altitude bin
        densities = alt_df['density'].unique()

        # option 2 is to plot x-axis as altitude bin and give one plot per density
        altbins = alt_df['altitudebins'].unique()

        # if option 1 loop through layer types
        for altbin in altbins:
            # get the data for this layer type
            altbin_df = alt_df[alt_df['altitudebins'] == altbin]
            
            plot_title = f'los/altitudebin_{altbin}'
            # plot the data
            sea_plotter(df=altbin_df, df_col='density', xlabels=densities, title=plot_title)

        
        for density in densities:
            #get the data for this density
            density_df = alt_df[alt_df['density'] == density]

            plot_title = f'los/density_{density}_altbins'
            
            # plot the data
            sea_plotter(df=density_df, df_col='altitudebins', xlabels=altbins, title=plot_title)


def sea_plotter(df: pd.DataFrame, df_col: str, xlabels: np.array, title:str):
    '''
    Plotter the data using seaborn.

    The dataframe should be filtered to either include one density or one other variable.
    For example it can be the layer type or perhaps the altitude bins.

    The dataframe column is the data that will be plotted on the x-axis.
    For example if we filter the dataframe to include 'very_low' density and then set the df_col to 'layertype'
    the x-axis will be all of the layer types for the 'very_low' density.

    The xlabels are the lables of the x-axis. So these are the unique values seen in the dataframe column.

    The title is the title of the plot and will be whatever the dataframe has been filtered to.
    '''

    fig, axes = plt.subplots(ncols=1, sharey=True)

    ax = (
        df.pipe((sns.boxplot, 'data'), x=df_col, y='count', hue='concept', order=xlabels)  
    )
    sns.despine(trim=True)

    # save the plot
    plt.savefig(f'images/{title}.png')
    plt.close()


def conftime(args, plot_dict):
    '''
    Plot the time taken to run the configuration.
    '''

    # get the data
    conf_df = plot_dict['CONFLOG']['DF']
    los_df = plot_dict['LOSLOG']['DF']

    scn_comb = args['combinations']

    # loop through combinations and remove first entry of tuple and get unique combinations
    scn_comb = list({x[1:] for x in scn_comb})

    density = scn_comb[0][0]
    concept = scn_comb[0][1]

    # filter los_df and conf_df based on 'density' and 'concept' from scn_comb
    los_df = los_df[(los_df['density'] == density) & (los_df['concept'] == concept)]
    conf_df = conf_df[(conf_df['density'] == density) & (conf_df['concept'] == concept)]
    
    # now for each los_df 'ACID1' and 'ACID2' search for the corresponding 'ACID1' and 'ACID2' in conf_df
    # note that it may be the case that the 'ACID1' and 'ACID2' are in the opposite order in conf_df
    # so we need to check for both cases
    # However only check with a 20 second lookback time (2x lookahead time)
    warningtimes = []
    with Progress() as progress:
        
        task1 = progress.add_task("[red]Making time image...", total=len(los_df))


        for row in los_df.itertuples():
            
            acid1 = row.ACID1
            acid2 = row.ACID2

            endtime = row.starttime
            starttime = endtime - timedelta(seconds=60)


            # first thing to do is to only select the rows that match the repetition
            conf_df_clip = conf_df[(conf_df['repetition'] == row.repetition)]


            # now clip conf_df to this time period
            conf_df_clip = conf_df_clip[(conf_df_clip['time'] >= starttime) & (conf_df_clip['time'] <= endtime)] 

            # now search for the acid1 and acid2 in conf_df_clip and concatenate the two dataframes
            conf_df_clip = pd.concat([
                            conf_df_clip[(conf_df_clip['ACID1'] == acid1) & (conf_df_clip['ACID2'] == acid2)], 
                            conf_df_clip[(conf_df_clip['ACID1'] == acid2) & (conf_df_clip['ACID2'] == acid1)]]
                            )

            # check how many hits we have
            if len(conf_df_clip) == 0:
                warningtime = 0

            elif len(conf_df_clip) == 1:
                warningtime = (endtime - conf_df_clip['time'].values[0]).total_seconds()

            else:
                conf_df_clip = conf_df_clip[conf_df_clip['time'] == conf_df_clip['time'].min()]
                warningtime = (endtime - conf_df_clip['time'].values[0]).total_seconds()


            # save some stuff from conf_df_clip
            warningtimes.append(warningtime)
            progress.update(task1, advance=1)

    # make a bar plot of the warning time distribution
    fig, ax = plt.subplots()
    ax.hist(warningtimes, bins=20)
    ax.set_xlabel('Warning time (s)')
    ax.set_ylabel('Count')
    ax.set_title(f'Warning time distribution for {density} density and {concept} concept')
    
    # save the plot
    plt.show()
    los_df['warningtime'] = warningtimes
