# %%
import cmdargs

import logparser as logp
import plotter as plotp
################## STEP 1: Parse command line arguments ######################
# filter the arguments
args = cmdargs.parse()
dir_files = 'results_filtered'


# send the information to the logparser and plot
if 'dfs' in args['create']:
    # parse the data
    plot_dict = logp.logparse(args)

    if 'plots' in args['create']:
        # now plot
        plotp.plotter(args, plot_dict)

    if 'conftime':
        # now plot
        plotp.conftime(args, plot_dict)