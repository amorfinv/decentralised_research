from rich import print, inspect, progress
from rich.progress import Progress
from matplotlib import pyplot as plt
from matplotlib.patches import PathPatch
import colorsys
import matplotlib.colors as mc

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

    concepts_colours=sns.color_palette("hls", 2)

    fig, axes = plt.subplots(ncols=1, sharey=True)

    ax = (
        df.pipe((sns.boxplot, 'data'), 
                x=df_col, 
                y='count',
                hue='concept', 
                order=xlabels, 
                palette=concepts_colours,
                # estimator=lambda x: sum(x==0)*100.0/len(x)
                )  
    )
    sns.despine(trim=True)
    plt.legend(loc='upper left')
    adjust_box_widths(fig, 0.5)
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

    with Progress() as progress:
        
        task1 = progress.add_task("[red]Making time image...", total=len(los_df))
        
        warningtimes = {density: {} for density, _ in scn_comb}

        # now loop through each concept and assign it as a key in the dictionary
        for density, concept in scn_comb:
            if concept not in warningtimes[density]:
                warningtimes[density][concept] = list()
    

        for density, concept in scn_comb:
            

            # filter los_df and conf_df based on 'density' and 'concept' from scn_comb
            los_df_trim = los_df[(los_df['density'] == density) & (los_df['concept'] == concept)]
            conf_df_trim = conf_df[(conf_df['density'] == density) & (conf_df['concept'] == concept)]
            
            # now for each los_df 'ACID1' and 'ACID2' search for the corresponding 'ACID1' and 'ACID2' in conf_df
            # note that it may be the case that the 'ACID1' and 'ACID2' are in the opposite order in conf_df
            # so we need to check for both cases
            # However only check with a 20 second lookback time (2x lookahead time)

            for row in los_df_trim.itertuples():
                
                acid1 = row.ACID1
                acid2 = row.ACID2

                endtime = row.starttime
                starttime = endtime - timedelta(seconds=60)


                # first thing to do is to only select the rows that match the repetition
                conf_df_clip = conf_df_trim[(conf_df_trim['repetition'] == row.repetition)]


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
                warningtimes[density][concept].append(warningtime)
                progress.update(task1, advance=1)


    fig, ax = plt.subplots()
    # set the hls colour palette for matplotlib
    concepts_colours=sns.color_palette("hls", 2)
    concept_list = ['m2', 'projectedcd']

    for concept in concept_list:

        if concept == 'm2':
            concept1 = 'baseline'
        elif concept == 'projectedcd':
            concept1 = 'projectedcd'
       
        ax.hist(warningtimes[density][concept], bins=20, label=concept1, histtype='step', ls='dashed', lw=1.5, color=concepts_colours[concept_list.index(concept)])
    
    ax.set_xlabel('Warning time (s)')
    ax.set_ylabel('Number of intrusions [-]')
    plt.legend(loc='upper right')
    # save the plot
    plt.savefig(f'images/{density}_los_time.png')


def adjust_box_widths(g, fac):
    """
    Adjust the withs of a seaborn-generated boxplot.
    """
    k=0

    # iterating through Axes instances
    for ax in g.axes:

        # iterating through axes artists:
        for c in ax.get_children():
            # searching for PathPatches
            if isinstance(c, PathPatch):
                # getting current width of box:
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]
                xmin = np.min(verts_sub[:, 0])
                xmax = np.max(verts_sub[:, 0])
                xmid = 0.5*(xmin+xmax)
                xhalf = 0.5*(xmax - xmin)

                # setting new width of box
                xmin_new = xmid-fac*xhalf
                xmax_new = xmid+fac*xhalf
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new
                
                # Set the linecolor on the artist to the facecolor, and set the facecolor to None
                col = lighten_color(c.get_facecolor(), 1.3)
                c.set_edgecolor(col) 

                for j in range((k)*6,(k)*6+6):
                   line = ax.lines[j]
                   line.set_color(col)
                   line.set_mfc(col)
                   line.set_mec(col)
                   line.set_linewidth(0.7)
                    
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])
                k+=1

def lighten_color(color, amount=0.5):  
    # --------------------- SOURCE: @IanHincks ---------------------
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])