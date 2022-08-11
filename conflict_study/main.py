# %%
import cmdargs
from rich import print
from matplotlib import pyplot as plt
import numpy as np
import numpy
import pandas as pd
import seaborn as sns

import logparser as logp

################## STEP 1: Parse command line arguments ######################
# filter the arguments
args = cmdargs.parse()
dir_files = 'results'

################## STEP 2: CREATE GEOPACKAGES #####################################

# send the information to the logparser
# parse the logs if creating geoapackages
if 'plots' in args['create']:
    plot_df = logp.logparse(args)
    # plot_df.groupby(['concept']).mean()
    # plot_df.boxplot(by ='LAYERTYPE', column =['count'], grid = False)
    # plt.show()

# get unique layertypes from df for x-axis
layertypes = plot_df['layertype'].unique()

fig, axes = plt.subplots(ncols=1, sharey=True)

ax = (
      plot_df.pipe((sns.boxplot, 'data'), x='layertype', y='count', hue='concept', order=layertypes)  
)
sns.despine(trim=True)
plt.show()