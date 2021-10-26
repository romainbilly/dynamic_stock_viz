# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:59:46 2017, updated Oct 26 2021

@author: romainb

Useful functions to intereact with the dynamic_stock_model package
and data preparation for the stock dynamics visualisation
(main file dynamic_stock_viz.py)
"""

import pandas as pd
import numpy as np
from dynamic_stock_model import DynamicStockModel

# Importing data in a pandas dataframe
file = "Sample_Data.csv"
data = pd.read_csv(file,header=0 , sep=',')
data.fillna(0, inplace=True)


def range_lifetime(lifetime_start, lifetime_end, stdev, time):
    """
    Given the mean lifetime of the first cohort,
    the mean lifetime of the lastcohort,
    the standard deviation and a time vector,
    this function returns a lifetime distribution from linear regression
    """
    lt={'Type': 'Normal', 
        'Mean': np.linspace(lifetime_start, lifetime_end, time),
        'StdDev': np.linspace(stdev, stdev, time) }
    return lt



def compute_model(data, lifetime, driver='Inflow-driven', input_type='Constant'):
    """
    Given input data, a lifetime distribution, 
    a type of model  (stock or inflow-driven) and a driver distribution,
    this function returns a complete DSM, with all calculations done
    """
#   Initializing the Dynamic Stock Model with the input parameters
    DSM =  DynamicStockModel(t=data.loc[:,'Time'], lt=lifetime)
                             
#   Running the calculations, first for the stock by time and cohort matrix,
#   then the outflows by time and cohort matrix,
#   and finally giving the total stock and outflow by time vectors
    if driver == 'Stock-driven':
        DSM.s = data.loc[:,input_type]
        DSM.compute_stock_driven_model() 
    elif driver == 'Inflow-driven':
        DSM.i = data.loc[:,input_type]
        DSM.compute_s_c_inflow_driven()    
        DSM.compute_o_c_from_s_c()
    else:
        print('Wrong driver specified')
    DSM.compute_outflow_total()
    DSM.compute_stock_total()
        
    return DSM
