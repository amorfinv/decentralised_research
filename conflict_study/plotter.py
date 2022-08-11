from rich import print
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plotter(args, plot_dict):    

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
        
        plot_title = f'layertype_{layertype}'
        # plot the data
        sea_plotter(df=layertype_df, df_col='density', xlabels=densities, title=plot_title)

    
    for density in densities:
        #get the data for this density
        density_df = layertypes_df[layertypes_df['density'] == density]

        plot_title = f'density_{density}_ltypes'
        
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
        
        plot_title = f'altitudebin_{altbin}'
        # plot the data
        sea_plotter(df=altbin_df, df_col='density', xlabels=densities, title=plot_title)

    
    for density in densities:
        #get the data for this density
        density_df = alt_df[alt_df['density'] == density]

        plot_title = f'density_{density}_ltypes'
        
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
