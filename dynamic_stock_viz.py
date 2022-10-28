# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:59:46 2017, updated Oct 26 2021

@author: romainb

Script building an interactive Bokeh visualization
for dynamic MFA models, where the user can:
    - choose between stock and inflow-driven models
    - choose different presets for the driver (inflow or stock)
    - change the lifetime distribution 
      (normal distribution defined by mean and standard deviation)
    - visualise the effet of decreasing or increasing lifetime
    
Based on the package dynamic_stock_model by Stefan Pauliuk:
https://github.com/stefanpauliuk/dynamic_stock_model/

The time and input data have to be specified in the file Sample_data.csv

To run the file on a server, it is necessary to open the Anaconda prompt
and type these two command lines 
(the first one should be mofidified to specifiy the actual path)
cd *path*
bokeh serve --show dynamic_stock_viz.py


dependencies:
    bokeh == 2.3.0
    numpy == 1.19.2
    pandas == 1.2.3
    scipy == 1.6.2
"""

import pandas as pd
import numpy as np
import stock_model_functions as smf

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc 
from bokeh.layouts import row, column
from bokeh.models.widgets import Slider, Select, Div
from bokeh.palettes import Category20 

# Initializing parameters for the model
data = smf.data
lifetime_start = 15
lifetime_end = 15
stdev=5
driver='Inflow-driven'
selected_input = 'Constant'

lifetime = smf.range_lifetime(lifetime_start, lifetime_end, stdev, len(data['Time']))
DSM = smf.compute_model(smf.data, lifetime)


def update_driver(attrname, old, new):
    """
    Callback function to dynamically update the value of 
    the driver type parameter
    each time the user changes the value in the corresponding widget
    It is necessary to update the value of each data source as well
    """
    global source, source_sc, source_bar, cohorts_matrix, driver 
    driver = new
    
    lifetime = smf.range_lifetime(lifetime_start, lifetime_end, stdev, len(smf.data['Time']))
    DSM = smf.compute_model(smf.data, lifetime, driver, input_type=selected_input)
    print("Driver:", new)
    plot_data = {'time': DSM.t,
             'stock': DSM.s,
             'inflows': DSM.i,
             'outflows': DSM.o,
             'stock change': DSM.i - DSM.o
             }
    source.data = plot_data
    source_sc.data = {'image': [np.flipud(DSM.s_c)]}
    cohorts_matrix = pd.DataFrame(
        data=DSM.s_c,  
        index=DSM.t.to_numpy(), 
        columns=[str(e) for e in plot_data["time"].to_numpy().tolist()]
        )
    cohorts_matrix.insert(
        0, "time",[str(e) for e in plot_data["time"].to_numpy().tolist()])
    source_bar.data=cohorts_matrix
    
def update_input(attrname, old, new):
    """
    Callback function to dynamically update the drver distribution  
    each time the user changes the value in the corresponding widget
    It is necessary to update the value of each data source as well
    """
    global source, source_sc, source_bar, cohorts_matrix, selected_input 
    selected_input = new
    
    lifetime = smf.range_lifetime(lifetime_start, lifetime_end, stdev, len(smf.data['Time']))
    DSM = smf.compute_model(smf.data, lifetime, driver, input_type=selected_input)
    print("Input distribution", new)
    plot_data = {'time': DSM.t,
             'stock': DSM.s,
             'inflows': DSM.i,
             'outflows': DSM.o,
             'stock change': DSM.i - DSM.o
             }
    source.data = plot_data
    source_sc.data = {'image': [np.flipud(DSM.s_c)]}
    cohorts_matrix = pd.DataFrame(
        data=DSM.s_c,  
        index=DSM.t.to_numpy(), 
        columns=[str(e) for e in plot_data["time"].to_numpy().tolist()]
        )
    cohorts_matrix.insert(
        0, "time",[str(e) for e in plot_data["time"].to_numpy().tolist()])
    #source_bar = ColumnDataSource(data=cohorts_matrix)
    source_bar.data = cohorts_matrix
    
def update_lifetime_start(attrname, old, new):
    """
    Callback function to dynamically update the value of 
    parameter defining the lifetime of the first cohort
    each time the user changes the value in the corresponding widget.
    It is necessary to update the value of each data source as well
    """
    global source, source_sc, source_bar, cohorts_matrix, lifetime_start
    lifetime_start = new
    print("Lifetime start", lifetime_start)
    lifetime = smf.range_lifetime(lifetime_start, lifetime_end, stdev, len(smf.data['Time']))
    
    DSM = smf.compute_model(smf.data, lifetime, driver, input_type=selected_input)

    plot_data = {'time': DSM.t,
             'stock': DSM.s,
             'inflows': DSM.i,
             'outflows': DSM.o,
             'stock change': DSM.i - DSM.o
             }
    source.data = plot_data
    lifetime_start = new
    source_sc.data = {'image': [np.flipud(DSM.s_c)]}
    cohorts_matrix = pd.DataFrame(
        data=DSM.s_c,  
        index=DSM.t.to_numpy(), 
        columns=[str(e) for e in plot_data["time"].to_numpy().tolist()]
        )
    cohorts_matrix.insert(
        0, "time",[str(e) for e in plot_data["time"].to_numpy().tolist()])
    source_bar.data=cohorts_matrix
    
def update_lifetime_end(attrname, old, new):
    """
    Callback function to dynamically update the value of 
    parameter defining the lifetime of the last cohort
    each time the user changes the value in the corresponding widget.
    It is necessary to update the value of each data source as well
    """
    global source, source_sc, source_bar, cohorts_matrix, lifetime_end 
    lifetime_end = new
    print("Lifetime end", lifetime_end)
    lifetime = smf.range_lifetime(lifetime_start, lifetime_end, stdev, len(smf.data['Time']))
    
    DSM = smf.compute_model(smf.data, lifetime, driver, input_type=selected_input)
    plot_data = {'time': DSM.t,
             'stock': DSM.s,
             'inflows': DSM.i,
             'outflows': DSM.o,
             'stock change': DSM.i - DSM.o
             }
    source.data = plot_data
    source_sc.data = {'image': [np.flipud(DSM.s_c)]}
    cohorts_matrix = pd.DataFrame(
        data=DSM.s_c,  
        index=DSM.t.to_numpy(), 
        columns=[str(e) for e in plot_data["time"].to_numpy().tolist()]
        )
    cohorts_matrix.insert(
        0, "time",[str(e) for e in plot_data["time"].to_numpy().tolist()])
    source_bar.data=cohorts_matrix
    
    
def update_stdev(attrname, old, new):
    """
    Callback function to dynamically update the value of 
    the standard deviation parameter 
    each time the user changes the value in the corresponding widget
    It is necessary to update the value of each data source as well
    """
    global source, source_sc, source_bar, cohorts_matrix, stdev
    stdev = new
    print("StDev", stdev)
    lifetime = smf.range_lifetime(lifetime_start, lifetime_end, stdev, len(smf.data['Time']))
    
    DSM = smf.compute_model(smf.data, lifetime, driver, input_type=selected_input)
    plot_data = {'time': DSM.t,
             'stock': DSM.s,
             'inflows': DSM.i,
             'outflows': DSM.o,
             'stock change': DSM.i - DSM.o
             }
    source.data = plot_data
    source_sc.data = {'image': [np.flipud(DSM.s_c)]}
    cohorts_matrix = pd.DataFrame(
        data=DSM.s_c,  
        index=DSM.t.to_numpy(), 
        columns=[str(e) for e in plot_data["time"].to_numpy().tolist()]
        )
    cohorts_matrix.insert(
        0, "time",[str(e) for e in plot_data["time"].to_numpy().tolist()])
    source_bar.data=cohorts_matrix
    
    
def make_line_plots(source):
    """
    Creates 3 line graphs of:
    1. Inflows and Outflows vs. Time
    2. Stock Change vs. Time
    3. Stock vs. Time
    one positionnal parameter: source, a column data source containing 
    the information in plot_data from the Dynamic Stock Model
    """

    options = dict(plot_width=400, plot_height=300,  toolbar_location=None)

    # Inflows and outflows
    p1 = figure(title="Inflows and outflows",  **options)
    p1.circle("time", "inflows", color="green", source=source)
    p1.circle("time", "outflows",  line_color="red", fill_color=None, source=source)
    
    # Stock change
    p2 = figure(title="Stock change", **options)
    p2.circle("time", "stock change",  line_color="black", fill_color=None, source=source)
    
    # Stock plot
    p3 = figure(title="Stock",  **options)
    p3.circle("time", "stock", color="blue", source=source)
    
    return [p1, p2, p3]
    

def make_bar_plots(source_sc, source_bar):
    """
    Creates 2 graphs:
    1. Time-cohorts matrix (heatmap image)
    2. Stock Size and column composition (bar chart stacked by cohort)
    two positionnal parameters: source_sc, and source_bar,
    customs columndata source containing 
    information about  the stock by time and cohort s_c 
    from the Dynamic Stock Model
    """
    # Image plot of the Stock by tie and cohort matrix
    p4 = figure(x_range=(DSM.t[0], DSM.t[len(DSM.t)-1]),
            y_range=(DSM.t[len(DSM.t)-1], DSM.t[0]),
            y_axis_label='Time', x_axis_label='Cohorts',
            title='Time-Cohorts Matrix',
            plot_width=410, plot_height=300,
            min_border_right = 20,
            toolbar_location=None)

    p4.image("image", x=DSM.t[0], y=DSM.t[len(DSM.t)-1], 
         dw=len(DSM.t), dh=len(DSM.t),
         source=source_sc, palette="Spectral11")
    
    stackers = [e for e in cohorts_matrix["time"].to_numpy().tolist()]
    palette = [Category20[20][i%19] for i in range(len(stackers))]
    
    p5 = figure(plot_width=790, plot_height=300, x_range=stackers,
            title = 'Stock size and cohort composition',
            y_axis_location="right", y_axis_label='Stock size',
            toolbar_location=None)
    p5.vbar_stack(stackers, x='time', width=0.9, color=palette,
                         source=source_bar)
    p5.xaxis.major_label_orientation = 3.14/2
    
    return [p4, p5]

# Defining sliders for lifetime and selection widget for the input distribution
driver_selection = Select(title="Driver", value="Inflow-driven", 
                         options=['Inflow-driven','Stock-driven'], width=400)
input_selection = Select(title="Driver distribution", value="Constant", 
                         options=smf.data.columns.tolist()[1:], width=400)
lifetime_param_start = Slider(start=2, end=50, value=15, step=1, 
                        title="Mean lifetime of 1st cohort", width=400)
lifetime_param_end = Slider(start=2, end=50, value=15, step=1, 
                        title="Mean lifetime of last cohort", width=400)
stdev_param = Slider(start=0.5, end=15, value=5, step=.1, 
                     title="Standard dev.", width=400)

# Launching the  calbacks every time the parameters are modified
driver_selection.on_change("value", update_driver)
input_selection.on_change("value", update_input)
lifetime_param_start.on_change('value_throttled', update_lifetime_start) 
lifetime_param_end.on_change('value_throttled', update_lifetime_end) 
stdev_param.on_change('value_throttled', update_stdev)


# Preparing data sources for the plots

# Source used for the line plots
plot_data = {'time': DSM.t,
         'stock': DSM.s,
         'inflows': DSM.i,
         'outflows': DSM.o,
         'stock change': DSM.i - DSM.o
         }
source = ColumnDataSource(data=plot_data)

# Source used for the matrix plot
source_sc = ColumnDataSource(data={'image': [np.flipud(DSM.s_c)]})

# Data preparation for the bar chart of cohorts vs time
cohorts_matrix = pd.DataFrame(
     data=DSM.s_c,  
     index=DSM.t.to_numpy(), 
     columns=[str(e) for e in plot_data["time"].to_numpy().tolist()]
     )
cohorts_matrix.insert(
     0, "time",[str(e) for e in plot_data["time"].to_numpy().tolist()])
# Source used for the bar plot 
source_bar = ColumnDataSource(data=cohorts_matrix)

# Putting the title and the widgets in a row container
widgets =column(row(Div(text="<h1> MFA Stock Dynamics Model</h1>", width=400,),
                    driver_selection, input_selection),
                row(lifetime_param_start, lifetime_param_end, stdev_param))

# Creating final layout and generating the plot
layout =column(
        widgets,
        row(make_line_plots(source)),
        row(make_bar_plots(source_sc, source_bar))
        )

curdoc().add_root(layout)
curdoc().title = " Dynamic MFA model"

