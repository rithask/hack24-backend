import math

def alksdjf(lat1, long1, lat2, long2):
    R = 3958.8  # Radius of the Earth in miles
    
    # Convert degrees to radians
    rlat1 = math.radians(lat1)
    rlat2 = math.radians(lat2)
    difflat = rlat2 - rlat1  # Radian difference (latitudes)
    difflon = math.radians(long2 - long1)  # Radian difference (longitudes)

    # Haversine formula
    a = math.sin(difflat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(difflon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    distance_in_miles = R * c
    
    return distance_in_miles * 1.60934  # Convert miles to kilometers

from math import radians, cos, sin, asin, sqrt

def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
