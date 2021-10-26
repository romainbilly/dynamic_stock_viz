

To run, open the command prompt, go to this directory and run this command (python and bokeh should be installed with path well configured):

cd *current path for the local repository*

cd C:\Users\romainb\Documents\Dynamic MFA Viz Python Bokeh
bokeh serve --show dynamic_stock_viz.py

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

dependencies:
    bokeh == 2.3.0
    numpy == 1.19.2
    pandas == 1.2.3
    scipy == 1.6.2