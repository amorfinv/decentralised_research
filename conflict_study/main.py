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
    plot_dict = logp.logparse(args)



# get unique layertypes from df for x-axis
layertypes_df = plot_dict['CONFLOG']['LAYERTYPES']

layertypes = layertypes_df['layertype'].unique()

fig, axes = plt.subplots(ncols=1, sharey=True)

ax = (
      layertypes_df.pipe((sns.boxplot, 'data'), x='layertype', y='count', hue='concept', order=layertypes)  
)
sns.despine(trim=True)
plt.show()


# get unique layertypes from df for x-axis
altbins_df = plot_dict['CONFLOG']['ALTITUDEBINS']

altitudebins= altbins_df['altitudebins'].unique()

fig, axes = plt.subplots(ncols=1, sharey=True)

ax = (
      altbins_df.pipe((sns.boxplot, 'data'), x='altitudebins', y='count', hue='concept', order=altitudebins)  
)
sns.despine(trim=True)
plt.show()