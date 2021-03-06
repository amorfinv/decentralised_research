# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 19:25:26 2022

@author: labpc2
"""
import geopy.distance
import shapely.geometry
from pyproj import Transformer
import dill
transformer = Transformer.from_crs('epsg:4326', 'epsg:32633')
FEET_TO_METERS_SCALE=0.3048
def get_coordinates_distance(origin_latitude: float, origin_longitude: float,
                             destination_latitude: float, destination_longitude: float) -> float:
    """ Calculates the distance in meters between two world coordinates.

    :param origin_latitude: origin latitude point.
    :param origin_longitude: origin longitude point.
    :param destination_latitude: destination latitude point.
    :param destination_longitude: destination longitude point.
    :return: distance in meters.
    """
    origin_tuple = (origin_latitude, origin_longitude)
    destination_tuple = (destination_latitude, destination_longitude)
    return geopy.distance.distance(origin_tuple, destination_tuple).m

def convert_feet_to_meters(distance_in_feet):
    """ Converts a given column that contains the altitude in feets to meters.

    """
    return distance_in_feet* FEET_TO_METERS_SCALE


drone_vertical_speed=5 #5 m/s

mp20_cruisng_speed=  0.95*10.29 #m/s 0.9*10.29 #m/s
mp30_cruisng_speed=0.95*15.43 #m/s  0.9*15.43 #m/s


def compute_work_done(ascend_dist,flight_time):
    
    work_done=flight_time+ascend_dist/drone_vertical_speed
    return work_done


def compute_ascending_distance(vertical_distance,deletion_altitude):
    if vertical_distance==-1:
        return -1
    ascend_dist=deletion_altitude+(vertical_distance-deletion_altitude)/2
    return ascend_dist


def compute_baseline_vertical_distance(loitering):
    if loitering:
        baseline_vertical_distance=9.144 # 30 feet
    else:
        baseline_vertical_distance=2*9.144 # 60 feet
    return baseline_vertical_distance

def compute_baseline_ascending_distance():
    baseline_ascending_distance=9.144 # 30 feet
    return baseline_ascending_distance

def compute_baseline_flight_time(baseline_route_lentgh,aircraft_type):
    cruising_speed=mp20_cruisng_speed
    if aircraft_type=="MP30": 
        cruising_speed=mp30_cruisng_speed
        
    return baseline_route_lentgh/cruising_speed

loitering_violation_time_threshold=180 # 3 minutes

def is_in_area_when_applied(nfz_applied_time,violation_time):
 
    if violation_time-nfz_applied_time<loitering_violation_time_threshold:
        return True
    
    return False

def has_orig_dest_in_nfz(dataframe, nfz_area):
    nfz_area_list=nfz_area.split("-")

    lon1=float(nfz_area_list[0])
    lon2=float(nfz_area_list[1])
    lat1=float(nfz_area_list[2])
    lat2=float(nfz_area_list[3])
    
    p1=transformer.transform(lat1,lon1)
    p2=transformer.transform(lat2,lon2)
    
    nfz_poly=shapely.geometry.Polygon([(p1[0],p1[1]),(p1[0],p2[1]),(p2[0],p2[1]),(p2[0],p1[1])])
    
    origin_lat=dataframe["Origin_LAT"].values[0]
    origin_lon=dataframe["Origin_LON"].values[0]
    p_origin=transformer.transform(origin_lat,origin_lon)

    dest_lat=dataframe["Dest_LAT"].values[0]
    dest_lon=dataframe["Dest_LON"].values[0]
    p_dest=transformer.transform(dest_lat,dest_lon)    

    
    if nfz_poly.contains(shapely.geometry.Point(p_origin)) or nfz_poly.contains(shapely.geometry.Point(p_dest)):
        return True
    
    return False

class Constrained_airspace():

    def __init__(self):
        input_file = open("data/constrained_poly.dill", 'rb')
        constrained_poly = dill.load(input_file)
        self.constrained_poly = shapely.geometry.Polygon(constrained_poly)
        self.transformer = Transformer.from_crs('epsg:4326', 'epsg:32633')

    # Function to check if a point (lon,lat) is in constrained airspace
    # returns true if point is in contsrained
    # returns false if poitn is in open
    def inConstrained(self, point):
        p = self.transformer.transform(point[1], point[0])
        p = shapely.geometry.Point(p[0], p[1])
        return self.constrained_poly.contains(p)
    
class Airspace():

    def __init__(self):
        input_file = open("data/airspace_buffered_border.dill", 'rb')
        airspace_poly = dill.load(input_file)
        self.airspace_poly = shapely.geometry.Polygon(airspace_poly)
        self.transformer = Transformer.from_crs('epsg:4326', 'epsg:32633')

    # Function to check if a point (lon,lat) is in constrained airspace
    # returns true if point is in contsrained
    # returns false if poitn is in open
    def inAirspace(self, point):
        p = self.transformer.transform(point[1], point[0])
        p = shapely.geometry.Point(p[0], p[1])
        return self.airspace_poly.contains(p)