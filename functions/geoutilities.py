# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:39:49 2016

@author: Steven
"""
"""
import pandas as pd
import os



from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from time import sleep
geolocator = GoogleV3()
geolocator = Nominatim()

location = geolocator.geocode("175 5th Avenue NYC")


file_path =  os.path.join("_input_test", "location_data.csv")
location_data = pd.read_csv(file_path)
 
location_data["point"] = location_data["shipto_addr_zip"].map(lambda x: geolocator.geocode(x, timeout = 10))



i = 0
for x in location_data["shipto_addr_zip"]:
    print(str(i)+"/"+ str(location_data.shape[0]))
    i+=1
    try:
        #print(geolocator.geocode(x, timeout = 10))
        print(geolocator.geocode(x))
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s"%(x, e.message))
    sleep(1)
 """

#%% Haversine distance

from math import radians, cos, sin, asin, sqrt
import numpy as np

def computeHaversine(lat1, lon1, lat2, lon2, road_factor = 1.0, km = False):
    """ Compute great circle distance between two points
    
    Args:
        lat1,lon1,lat2,lon2 (float): lat and lon in decimal degrees
        km (boolean): if true, distance in km (default: False = distance in miles)
        road_factor (float): multiply distance to account for road (default = 1). Use 1.18 if want to take into account road
        
    Returns
        float: distance in km or miles between points
        
    """
    # set radius of earth
    if km:
        R = 6371
    else:
        R = 3959
    
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = [radians(x) for x in [lat1, lon1, lat2, lon2]]
  
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
  
    return R*c*road_factor   
  

computeHaversineVector = np.vectorize(computeHaversine, otypes=[np.float])
  