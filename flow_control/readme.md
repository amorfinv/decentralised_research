# Directory organization.

## "airspace_design/"

This contains information about the original Metropolis 2 set up.

## "cluster_center_dills/"

This contains the cluster center dills that were created based on logs of a Metropolis 2 simulation without flow control.
These are created by running the "CreateClusterSectors.py" code with an accompanying log files.
There were six dills created. However, only 2 were selected for simulations

- Flow_control_clusters_centers1.dill
- Flow_control_clusters_centers5.dill

## "graph_data/"

This contains the json files needed for BlueSky simulations of each different case

- cluster_sectors_1
- cluster_sectors_2
- grid_sectors_large
- grid_sectors_small
- M2_baseline

Each of these folders contains:

- const_edges.json
- constrained_node_dict.json
- dummy.json
- edges.json
- Flow_control.dill
- flow_length.json
- flows.json
- nodes.json
- stroke_length.json
- strokes.json

The jsons are created by having a prepared graph from "Edges2FlowGroupsAssignment.py".
The dill is created with a prepared graph and "flow_control_dills_creator.py".

## "plugins/streets"

....

## "scenarios/"

Contains the scenarios of each different case

## "whole_vienna/"

This contains all the geogrpahical data, graphml files and QGIS files.

### "ConvertDill2GPKG.py"

This converts the cluster_center_dills into a geopackage file for analysis.

### "CreateClusterSectors.py"

This creates the cluster sectors based on a conflog file. The voronoi cells are then created via QGIS.
There is some manual modification at the borders to ensure that all edges are contained within one voronoi cell.

### "Edges2FlowGroupsAssignment.py"

This code takes "finalized_graph" (M2_baseline graph) and a sector grid to assign new flow groups to the graph based on the new grid.

### "flow_control_dills_creator.py"

Creates a flow control dill for each case.

### "flow_groups_graphs.py"

Creates a graph of flow groups.

### "prepare_jsons.py"

This code takes a graph and generates some jsons for BlueSky simulation.

### "flow_manage.cfg"

This is a settings file for generating the grid for grid_sectors_small and grid_sectors_large.
https://github.com/amorfinv/flowmanage
