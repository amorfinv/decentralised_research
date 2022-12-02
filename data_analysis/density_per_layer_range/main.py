# %%
import cmdargs
from rich import print

import logparser as logp

################## STEP 1: Parse command line arguments ######################
# filter the arguments
args = cmdargs.parse()

################## STEP 2: CREATE GEOPACKAGES #####################################

# send the information to the logparser
# parse the logs if creating geoapackages
if 'gpkgs' in args['create']:
    logp.logparse(args)


