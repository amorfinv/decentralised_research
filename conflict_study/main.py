# %%
import cmdargs

import logparser as logp
import plotter as plotp
################## STEP 1: Parse command line arguments ######################
# filter the arguments
args = cmdargs.parse()
dir_files = 'results'


# send the information to the logparser and plot
if 'plots' in args['create']:
    # parse the data
    plot_dict = logp.logparse(args)

    # now plot
    plotp.plotter(args, plot_dict)