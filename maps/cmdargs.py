''' BlueSky command-line argument parsing. '''
import argparse
from cmath import log
from itertools import combinations, product
from rich.pretty import pprint


def parse():
    parser = argparse.ArgumentParser(prog="heatmaps", description="Create heatmaps from BlueSky flight data.")


    # create arguments for --concept it can have multiple arguments (centralised, hybrid, decentralised)) 
    # if none are specified then the default value is used [all]
    parser.add_argument('--concept', nargs='+', default='all', 
                        help='Specify the concept of the heatmap to be created. Options are: m2, manualflow, noflow, projectedcd, ' 
                        '1to1, clustersectors1, clustersectors2, gridsectors, headalloc, headallocnoflow, headingcr. Default is all.')

    # create arguments for --logtype it can have multiple arguments (REGLOG, CONFLOG, LOSLOG, GEOLOG, FLSTLOG, all)
    parser.add_argument('--logtype', nargs='+', default='all', 
                        help='Specify the logtype of the heatmap to be created. Options are: REGLOG, CONFLOG, LOSLOG, GEOLOG ,FLSTLOG, all')

    # create arguments for --density it can have multiple arguments (very_low, low, medium, high, ultra, all)
    parser.add_argument('--density', nargs='+', default='all', 
                        help='Specify the density of the heatmap to be created. Options are: very_low, low, medium, high ,ultra, all')

    # create arguments for --create it can have multiple arguments (maps, files, all)
    parser.add_argument('--create', nargs='+', default='all', 
                        help='Specify if code should create gpkg files or just output heatmaps. Options are: gpkgs, geotifs, images, all')

    # parse arguments
    cmdargs, _ = parser.parse_known_args()

    # return the arguments
    args = vars(cmdargs)

    # now check if the user has specified all the arguments
    if args['create'] == 'all':
        args['create'] = ['gpkgs', 'geotifs', 'images']

    if args['concept'] == 'all':
        args['concept'] = [
                            "m2",
                            "manualflow",
                            "noflow",
                            "projectedcd",
                            "1to1",
                            "clustersectors1",
                            "clustersectors2",
                            "gridsectors",
                            "headalloc",
                            "headallocnoflow",
                            "headingcr",
                            ]
    
    if args['logtype'] == 'all':
        args['logtype'] = ['REGLOG', 'CONFLOG', 'LOSLOG', 'GEOLOG', 'FLSTLOG']

    if args['density'] == 'all':
        args['density'] = ['very_low', 'low', 'medium', 'high', 'ultra']
    
    # Uncertainty is a special case, do some stuff before creating combinations

    # make combinations
    args['combinations'] = list(product(args['logtype'], args['density'], args['concept']))
    
    return args

