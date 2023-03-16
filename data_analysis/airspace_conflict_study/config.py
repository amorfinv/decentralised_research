import json

# general config
log_location = 'logs'

with open('ac_in_constrained.json') as f:
  ac_in_constrained_dict = json.load(f)

concepts_dict = {
    'm2'                    : 'Baseline',
    '1to1'                  : '1-to-1',
}

density_dict = {
    'very_low': 'very low',
    'low': 'low',
    'medium': 'medium',
    'high': 'high',
    'ultra': 'very high'
}

repetitions = range(0,9)

# CONFLOG data
conf_metrics = ['Total conflicts', 'Conflicts per flight']
conflict_columns = [
    'time',
    'ACID1',
    'ACID2',
    'LAT1',
    'LON1',
    'ALT1',
    'LAT2',
    'LON2',
    'ALT2',
    'CPALAT',
    'CPALON',
    'AIRSPACETYPE1',
    'AIRSPACETYPE2',
    'LAYERTYPE1',
    'LAYERTYPE2',
    'EDGEID1',
    'EDGEID2',
    ]

# LOSLOG data
los_metrics = ['Total intrusions']


FLST_cols = [
    'Deletion time', 
    'ACID', 
    'Spawn time',  
    'Flight time', 
    'Distance 2D', 
    'Distance 3D',
    'Distance ALT', 
    'Work Done', 
    'Latitude', 
    'Longitude', 
    'Altitude', 
    'TAS', 
    'Vertical Speed', 
    'Heading', 
    'ASAS Active', 
    'Pilot ALT', 
    'Pilot SPD', 
    'Pilot HDG', 
    'Pilot VS', 
    'AIRSPACEALLOC'
]

flst_metrics = [
    'Flight time', 
    'Distance 2D', 
    'Distance 3D',
    'Distance ALT',
    ]

flst_metrics = {
    'Flight time': 'Route duration', 
    'Distance 2D': 'Horizontal distance', 
    'Distance 3D': '3D distance',
    'Distance ALT': 'Vertical distance',
}
