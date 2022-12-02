The height allocation grid for zones is based on the conflict cluster analysis made in the flow control study

the jsons and graphs for this were prepared with the flowcontrol code.

To create the grid we took the conflict cluster analysis clusters_1 and then performed a classification analysis. The areas of each sector were calculated and each sector was grouped into one of 5 groups using equal_count (quantile) from QGIS. The smallest group (areas < 373,698) were then merged to neighboring sectors. 
