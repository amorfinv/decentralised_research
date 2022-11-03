# Decentralised Research repository

This repository contains the code and data for modifying the Metropolis 2 scenarios for the decentralised sensitivity study. Refer to the [M2-sensitivity]([url](https://github.com/andubadea/bluesky/tree/M2-sensitivity)) ```BlueSky``` code for the relevant plugins needed to run these experiments.

Below is each directory and a summary of what it contains.

* ```M2_data/```.
  * Metropolis 2 scenarios.
  * Metropolis 2 decentralised layers structure json file.

* ```Output_graphics/```.
  * ...

* ```airspace_structure_study/```.
  * Scenarios of the 1to1 structure experiment.
  * The ```layers.json``` of the 1to1 structure.
  * The ```flow_manage.cfg``` settings file for creating this structure with [flowmanage]([url](https://github.com/amorfinv/flowmanage)) code.

* ```batch_scenarios```.
  * The batch scenarios for ```BlueSky```.

* ```conflict_study/```.
  * Code to analyze the conflict types in a log.

* ```data_platform/```.
  * This is a copy of the Metropolis 2 data analysis [platform]([url](https://github.com/Metropolis-2/M2_data_analysis_platform)) adapted for this sensitivity study.

* ```flow_control/```.
  * Experiments of different flow control implementation (large and small grid and voronoi cluster sectors)
  * See the ```flow_control/readme.md``` for more information.

* ```heading_based_cr/```.
  * Scenarios of experiment where heading
