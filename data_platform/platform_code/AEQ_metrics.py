# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 16:44:11 2022

@author: labpc2
"""
import pandas as pd




def compute_aeq3(df):
    """ AEQ-3: The demand delay dispersion

    Measured as standard deviation of delay of all flight intentions,
    where delay for each flight intention is calculated as a difference between
    realized arrival time and ideal expected arrival time.

    Ideal expected arrival time is computed as arrival time of the fastest
    trajectory from origin to destination departing at the requested time as
    if a user were alone in the system, respecting all concept airspace rules.

    Realized arrival time comes directly from the simulations.
    The missions not completed are filtered from this metric.

    :param input_dataframes:filtered by scenario flst_datframe.
    :return: the computed AEQ3 metric.
    
    """
    df_filtered=df[(df['Spawned'])&(df['Mission_completed'])]
    aeq3=df_filtered["Arrival_delay"].std()
    
    return aeq3
