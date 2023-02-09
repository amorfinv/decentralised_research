import os
import numpy as np

log_location = 'logs'

concept = 'noflow'

log_type = 'CONFLOG'

def convert_angle(angle):
    if angle > 180:
        angle -= 360
    return angle

def kwikqdrdist(lata, lona, latb, lonb):
    """Gives quick and dirty qdr[deg] and dist [nm]
       from lat/lon. (note: does not work well close to poles)"""

    re      = 6371000.  # radius earth [m]
    dlat    = np.radians(latb - lata)
    dlon    = np.radians(((lonb - lona)+180)%360-180)
    cavelat = np.cos(np.radians(lata + latb) * 0.5)

    dangle  = np.sqrt(dlat * dlat + dlon * dlon * cavelat * cavelat)
    dist    = re * dangle 

    qdr     = np.degrees(np.arctan2(dlon * cavelat, dlat)) % 360.

    return qdr, dist

files = os.listdir(log_location)

files = [file for file in files if f'_{concept}.log' in file]
files = [file for file in files if log_type in file]


file = 'CONFLOG_Flight_intention_high_40_7_noflow.log'
print(file)
with open(f'{log_location}/{file}') as f:
    confs = f.readlines()[9:]


count = 0

for conf in confs:
    conf = conf.split(',')

    lat_1 = float(conf[3])
    lon_1 = float(conf[4])
    alt_1 = float(conf[5])

    lat_2 = float(conf[6])
    lon_2 = float(conf[7])
    alt_2 = float(conf[8])

    cpalat = float(conf[9])
    cpalon = float(conf[10])
    
    qdr_1, dist_1 = kwikqdrdist(lat_1, lon_1, cpalat, cpalon)
    qdr_2, dist_2 = kwikqdrdist(lat_2, lon_2, cpalat, cpalon)
    
    # get angle difference
    angle_diff = abs(convert_angle(qdr_1)-convert_angle(qdr_2))
    
    # if alt within 20 feet
    alt_diff = abs(alt_1 - alt_2)

    if alt_diff < 6 and angle_diff < 20:
        count += 1

print(count/len(confs))
print(count)
print(len(confs))
