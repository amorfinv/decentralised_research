# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:59:47 2022

@author: labpc2
"""

def compute_saf1(df):
    """ SAF-1: Number of conflicts

    Number of aircraft pairs that will experience a loss of separation
    within the look-ahead time.

    :param input_dataframes: the filtered by scenario conflog_datframe.
    :return: the computed SAF1 metric.
    """

    saf1=df[df['in_time']].shape[0]
    return saf1
def compute_saf1_3(df):
    """ SAF-1_3: Number of conflicts in constarined

    Number of aircraft pairs that will experience a loss of separation
    within the look-ahead time.

    :param input_dataframes: the filtered by scenario conflog_datframe.
    :return: the computed SAF1 metric.
    """

    saf1_3=df[(df['in_time'])&(df["constrained"])].shape[0]
    return saf1_3

def compute_saf1_4(df):
    """ SAF-1_4: Number of conflicts in open

    Number of aircraft pairs that will experience a loss of separation
    within the look-ahead time.

    :param input_dataframes: the filtered by scenario conflog_datframe.
    :return: the computed SAF1 metric.
    """

    saf1_4=df[(df['in_time'])&(df["constrained"]==False)].shape[0]
    return saf1_4

def compute_saf2(df):
    """ SAF-2: Number of intrusions

    Number of aircraft pairs that experience loss of separation.
    
    :param input_dataframes: the filtered by scenario loslog_datframe.
    :return: the computed SAF2 metric.
    """
    saf2=df[df['in_time']].shape[0]
    return saf2
def compute_saf2_2(df):
    """ SAF-2_2: Number of intrusions in constrained

    Number of aircraft pairs that experience loss of separation.
    
    :param input_dataframes: the filtered by scenario loslog_datframe.
    :return: the computed SAF2 metric.
    """
    saf2_2=df[(df['in_time'])&(df["constrained"])].shape[0]
    return saf2_2

def compute_saf2_3(df):
    """ SAF-2_3: Number of intrusions in open

    Number of aircraft pairs that experience loss of separation.
    
    :param input_dataframes: the filtered by scenario loslog_datframe.
    :return: the computed SAF2 metric.
    """
    saf2_3=df[(df['in_time'])&(df["constrained"]==False)].shape[0]
    return saf2_3

def compute_saf2_1(df):
    """ SAF-2-1: Count of crashes

    Count of crashes for each scenario (each aircraft logged in the FLSTlog has a boolean flag called crash)
    if that is true ir counts as a crash and the number of the times crash is true is the result of this metric.

    :param input_dataframes: the filtered by scenario loslog_datframe.
    :return: the computed SAF2-1 metric.
    """
    saf2=df[(df['in_time'])&(df['crash'])].shape[0]
    return saf2

def compute_saf4(df):
    """ SAF-4: Minimum separation

    The minimum separation between aircraft during conflicts.

    :param input_dataframes: the filtered by scenario loslog_datframe.
    :return: the computed SAF4 metric.
    """
    saf4=df[df['in_time']]['DIST'].min()
    return saf4

def compute_saf5(df):
    """ SAF-5: Time spent in LOS

    Total time spent in a state of intrusion.

    :param input_dataframes: the filtered by scenario loslog_datframe.
    :return: the computed SAF5 metric.
    """
    saf5=df[df['in_time']]['LOS_duration_time'].sum()
    return saf5

def compute_saf5_1(df):
    """ SAF-5_1: Average Time spent in LOS

    Total time spent in a state of intrusion.

    :param input_dataframes: the filtered by scenario loslog_datframe.
    :return: the computed SAF5 metric.
    """
    saf5_1=df[df['in_time']]['LOS_duration_time'].sum()
    saf5_1/=df[df['in_time']]['LOS_duration_time'].shape[0]
    return saf5_1
