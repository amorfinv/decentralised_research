import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd

from matplotlib.patches import PathPatch
import matplotlib
import matplotlib.colors as mc
import colorsys

matplotlib.use('Agg')

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

conf_dict = {density: {concept: {repetition: 0 for repetition in repetitions} for concept in concepts}for density in densities}
los_dict = {density: {concept: {repetition: 0 for repetition in repetitions} for concept in concepts}for density in densities}

metrics = ['Total', 'Percentage of horizontal', 'Percentage of vertical', 'Percentage of back-to-back']
cols = ['density', 'concept', 'repetition'] + metrics

conf_df = pd.DataFrame(columns=cols)
los_df = pd.DataFrame(columns=cols)


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

def convert_angle(angle):
    if angle > 180:
        angle -= 360
    return angle

def kwikqdrdist(lata, lona, latb, lonb):
    """Gives quick and dirty qdr[deg] and dist [nm]
       from lat/lon. (note: does not work well close to poles)"""

    re      = 6371000.  # radius earth [m]
    dlat    = np.radians(latb - lata)
    dlon    = np.radians(((lonb - lona)+180)%360-180)
    cavelat = np.cos(np.radians(lata + latb) * 0.5)

    dangle  = np.sqrt(dlat * dlat + dlon * dlon * cavelat * cavelat)
    dist    = re * dangle 

    qdr     = np.degrees(np.arctan2(dlon * cavelat, dlat)) % 360.

    return qdr, dist

for density in densities:

    for concept in concepts:

        for repetition in repetitions:

            # CONFLOG

            # get the scenario name and open the file
            scenario = f'Flight_intention_{density}_40_{repetition}_{concept}.log'
            with open(f'{log_location}/CONFLOG_{scenario}') as f:
                confs = f.readlines()[9:]

            # initialize some variables for conflicts and process the logs
            vertical_confs = 0
            horizontal_confs = 0
            back_to_back_confs = 0
            total_confs = 0

            for conf in confs:

                # split log based on comma
                conf = conf.split(',')

                # only process constrained airspace conflicts
                airspace_type_1 = conf[11]
                airspace_type_2 = conf[12]

                airspace_types = [airspace_type_1, airspace_type_2]

                if airspace_type_1 == 'open' or airspace_type_2 == 'open':
                    continue
                
                # sum total number of conflicts
                total_confs += 1

                # get some data from the log
                lat_1 = float(conf[3])
                lon_1 = float(conf[4])
                alt_1 = float(conf[5])

                lat_2 = float(conf[6])
                lon_2 = float(conf[7])
                alt_2 = float(conf[8])

                cpalat = float(conf[9])
                cpalon = float(conf[10])

                # get the distance of current conflict aircraft to cpa                
                qdr_1, dist_1 = kwikqdrdist(lat_1, lon_1, cpalat, cpalon)
                qdr_2, dist_2 = kwikqdrdist(lat_2, lon_2, cpalat, cpalon)
                
                # get angle difference
                angle_diff = abs(convert_angle(qdr_1)-convert_angle(qdr_2))
                
                # if alt within 20 feet
                alt_diff = abs(alt_1 - alt_2)

                # label as vertical or horizontal conflict
                if alt_diff >= 6:
                    vertical_confs += 1
                else:
                    horizontal_confs += 1

                if alt_diff < 6 and angle_diff < 20:
                    back_to_back_confs += 1


            # get conflict data in dataframe
            df_conf_scn = pd.DataFrame(
                [
                    [
                        density,
                        concepts_dict[concept],
                        repetition,
                        total_confs,
                        horizontal_confs/total_confs*100,
                        vertical_confs/total_confs*100,
                        back_to_back_confs/total_confs*100,
                    ]
                ],
                columns=cols
            )

            # concat dataframes
            conf_df = pd.concat([conf_df, df_conf_scn])

            # LOSLOG
            with open(f'{log_location}/LOSLOG_{scenario}') as f:
                losses = f.readlines()[9:]
            
            # initialize some data for conflicts and process them
            vertical_los = 0
            horizontal_los = 0
            back_to_back_los = 0
            total_los = 0

            for los in losses:
                # split log based on comma

                los = los.split(',')

                airspace_type_1 = los[12]
                airspace_type_2 = los[13]

                if airspace_type_1 == 'open' or airspace_type_2 == 'open':
                    continue


                lat_1 = float(los[5])
                lon_1 = float(los[6])
                alt_1 = float(los[7])

                lat_2 = float(los[8])
                lon_2 = float(los[9])
                alt_2 = float(los[10])
                
                qdr_1 = float(los[18])
                qdr_2 = float(los[19])

                total_los += 1

                # get angle difference
                angle_diff = abs(convert_angle(qdr_1)-convert_angle(qdr_2))
                
                # check if alt within 20 feet
                alt_diff = abs(alt_1 - alt_2)

                # label as vertical or horizontal conflict
                if alt_diff >= 6:
                    vertical_los += 1
                else:
                    horizontal_los += 1

                if alt_diff < 6 and angle_diff < 20:
                    back_to_back_los += 1


            # get los data in dataframe
            df_los_scn = pd.DataFrame(
                [
                    [
                        density,
                        concepts_dict[concept],
                        repetition,
                        total_los,
                        horizontal_los/total_los*100,
                        vertical_los/total_los*100,
                        back_to_back_los/total_los*100,
                    ]
                ],
                columns=cols
            )
            los_df = pd.concat([los_df, df_los_scn])



fig = plt.figure()

for metric in metrics:
    
    sns.boxplot(
        y=metric,
        x='density',
        data=conf_df,
        palette=concepts_colours,
        hue='concept'
    )

    plt.ylabel(f'{metric} conflicts in constrained airspace [-]')
    plt.legend(loc='upper left')
    adjust_box_widths(fig, 0.5)

    if metric != 'Total':
        plt.ylim(-5, 105)

    plt.savefig(f'images/{metric}_confs',bbox_inches='tight')
    plt.clf()

    sns.boxplot(
        y=metric,
        x='density',
        data=los_df,
        palette=concepts_colours,
        hue='concept'
    )

    plt.ylabel(f'{metric} intrusions in constrained airspace [-]')
    plt.legend(loc='upper left')
    adjust_box_widths(fig, 0.5)

    if metric != 'Total':
        plt.ylim(-5, 105)

    plt.savefig(f'images/{metric}_los',bbox_inches='tight')
    plt.clf()
