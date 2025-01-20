# -*- coding: utf-8 -*-
"""
Created on Tue May 05 09:53:14 2015

@author: lenovo
"""

# using google formula
import sys
import math
# import MySQLdb

EARTH_RADIUS = 6378.137  #km

def get_distance(lon1, lat1, lon2, lat2):
    #s = 2arcsin(sqrt(pow(sin(a/2),2) + cos(lat1)*cos(lat2)*pow(sin(b/2),2))) * radius
    
    radlon1 = math.radians(lon1)
    radlat1 = math.radians(lat1)
    radlon2 = math.radians(lon2)
    radlat2 = math.radians(lat2)
    
    a = radlat1 - radlat2
    b = radlon1 - radlon2
    
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radlat1) * math.cos(radlat2) * math.pow(math.sin(b/2), 2)))
    s = s * EARTH_RADIUS * 1000
    return s
    
def do(err):
    print("Getting distance between 2 points by calculating their gps using google formula")
    """    
    lon1 = float(raw_input("please input the longitude of the 1st point(float):")) 
    lat1 = float(raw_input("please input the latitude of the 1st point(float):"))  
    lon2 = float(raw_input("please input the longitude of the 2nd point(float):")) 
    lat2 = float(raw_input("please input the latitude of the 2nd point(float):"))
    """
    dis = get_distance(116.4590315,39.9539554, 116.4590315+err, 39.9539554)
    # dis = get_distance(116.277122,39.9539554, 116.277827, 39.960238 )

    print (dis)
    print("the distance between the 2 points is %.2f m" %(dis))
    return dis

if __name__=="__main__":
    do(9.327059835355894e-05)
    
    
