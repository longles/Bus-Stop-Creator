"""
utility functions
"""
import math


### functions related to general mathematics ###
def local_max(lst: list) -> list:
    """
    Preconditions:
          - all({type(i) == int or type(i) == float for i in lst})
    """
    l_maxs = []
    for i in range(len(lst)):
        if i != 0 and i != len(lst) - 1:
            if lst[i - 1] < lst[i] > lst[i + 1]:
                l_maxs.append(lst[i])
    return l_maxs


### functions related to maps and geography ###
def lat_long_to_coord(latitude: float, longtitude: float, central_meridian: float) -> tuple:
    """
    Use Mercator projection to transform longitude latitude to coordinates
    read https://en.wikipedia.org/wiki/Mercator_projection#Derivation_of_the_Mercator_projection
    for more info
    "the Mercator projection inflates the size of objects away from the equator."

    Preconditions:
          - central meridian is the closest meridian to the center of the map

    Notice that difference is returned because values are lost through performing math.tan()
    If you want to perform coord_to_long_lat(), you must return difference, otherwise you don't
    need to.

    testing
    coord = lat_long_to_coord(43.786370, -79.463070, 0.0)
    x = coord[0]
    y = coord[1]
    difference = coord[2]
    """
    earth_radius = 6371000  # meters
    x = earth_radius * (longtitude - central_meridian)
    y = earth_radius * math.log(math.tan(math.pi / 4 + latitude / 2), math.e)
    difference = int((math.pi / 4 + latitude / 2) / math.pi)
    return int(x), int(y), difference


def coord_to_long_lat(x: int, y: int, central_meridian: float, difference: int) -> tuple:
    """
    Transform Mercator projected coordinates back to longitude latitude
    read https://en.wikipedia.org/wiki/Mercator_projection#Derivation_of_the_Mercator_projection
    for more info
    "the Mercator projection inflates the size of objects away from the equator."

    testing
    coord_to_long_lat(x, y, 0.0, difference)
    """
    earth_radius = 6371000  # meters
    longitude = x / earth_radius + central_meridian
    latitude = 2 * (math.atan(math.e ** (y / earth_radius)) + difference * math.pi - math.pi / 4)
    return (latitude, longitude)
