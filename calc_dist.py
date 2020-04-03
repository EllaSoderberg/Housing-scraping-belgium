import geopy.distance

def calc_distance(long, lat, loc_a, loc_b):
    """
    long, lat: The coordinates of a point of interest (for example an apartment)
    loc_a, loc_b: The coordinates of two other locations

    Returns the average distance as an int and center as a boolean
    """
    
    dist_a_to_b = geopy.distance.distance(loc_a, loc_b).km # Calculates the distance between point a and b

    dist_a = geopy.distance.distance(loc_a, (long, lat)).km # Calculates the distance between point a and the main point
    dist_b = geopy.distance.distance(loc_b, (long, lat)).km # Calculates the distance between point b and the main point

    avg_distance = (dist_a + dist_b) / 2 # Calculates the average distance between a and b

    center = True

    if dist_a > dist_a_to_b or dist_b > dist_a_to_b: # If the main point is not between point a and point b, center will return false. 
        center = False
    
    return avg_distance, center
