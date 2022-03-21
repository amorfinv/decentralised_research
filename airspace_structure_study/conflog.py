# %%
import os

import dask.dataframe as dd
import pandas as pd
pd.options.plotting.backend = "plotly"

import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

## STEP 1: Place all the conflog files in a dask dataframe

# get list of files in directory
list_files_l1 = os.listdir('sim_logs')

dask_divisions = sorted([x[8:-22] for x in list_files_l1])

# only get files with CONFLOG in name
list_files_l1 = ['sim_logs/' + x for x in list_files_l1 if 'CONFLOG' in x]

# only get files with CONFLOG in name
header_columns = ['time','ACID1','ACID2','LAT1','LON1','ALT1','LAT2','LON2','ALT2','CPALAT','CPALON']

# read all files and place in dataframe
ddf_conflog = dd.read_csv('sim_logs/*CONFLOG*.log', skiprows=9, header=None, names=header_columns, include_path_column=True)

# only use the file name in path and set as index and remove anything after the run date
ddf_conflog['path'] = ddf_conflog.path.str.split('/').str[-1]
ddf_conflog['path'] = ddf_conflog.path.str.split('_2022').str[0]

# set the path as the daks dataframe index
ddf_conflog = ddf_conflog.set_index('path')

## STEP 2: GET COUNT OF EACH CONFLOG FILE

# get conflict count of each log
df2 = pd.DataFrame(ddf_conflog.map_partitions(len).compute(), columns=['conflicts'])
df2['log'] = ddf_conflog.divisions[:-1]

# set the density based on log file
df2['density'] = df2.log.str.split('intention_').str[1].str[:-5]

# Get the repition of each log
df2['rep'] = df2.log.str.split('_').str[-2]

## STEP 3: REORGANIZE THE DATAFRAME FOR EASY PLOTTING

# reorganize the dataframe for plotting
df3 = df2.pivot(index='rep', columns="density", values='conflicts')

# ensure columns are in correct order
cols = ['very_low_40','low_40']
df3 = df3[cols]

# %%
## other conflog
# get list of files in directory
list_files_l1 = os.listdir('l1')

dask_divisions = sorted([x[8:-22] for x in list_files_l1])

# only get files with CONFLOG in name
list_files_l1 = ['l1/' + x for x in list_files_l1 if 'CONFLOG' in x]

# only get files with CONFLOG in name
header_columns = ['time','ACID1','ACID2','LAT1','LON1','ALT1','LAT2','LON2','ALT2','CPALAT','CPALON']

# read all files and place in dataframe
ddf_conflog = dd.read_csv('l1/*CONFLOG*.log', skiprows=9, header=None, names=header_columns, include_path_column=True)

# only use the file name in path and set as index and remove anything after the run date
ddf_conflog['path'] = ddf_conflog.path.str.split('/').str[-1]
ddf_conflog['path'] = ddf_conflog.path.str.split('_2022').str[0]

# set the path as the daks dataframe index
ddf_conflog = ddf_conflog.set_index('path')

## STEP 2: GET COUNT OF EACH CONFLOG FILE

# get conflict count of each log
df2 = pd.DataFrame(ddf_conflog.map_partitions(len).compute(), columns=['conflicts'])
df2['log'] = ddf_conflog.divisions[:-1]

# set the density based on log file
df2['density'] = df2.log.str.split('intention_').str[1].str[:-5]

# Get the repition of each log
df2['rep'] = df2.log.str.split('_').str[-1]

## STEP 3: REORGANIZE THE DATAFRAME FOR EASY PLOTTING

# reorganize the dataframe for plotting
df4 = df2.pivot(index='rep', columns="density", values='conflicts')

# ensure columns are in correct order
cols = ['very_low','low', 'medium']
df4 = df4[cols]

df5 = pd.concat([df4, df3], axis=1)

cols = ['very_low', 'very_low_40', 'low', 'low_40']
df5 = df5[cols]

# %%


fig = df5.boxplot()

# set the y axis label as conflicts
fig.update_yaxes(title_text='Conflicts')
fig.update_xaxes(title_text='Density')


# %%


app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter