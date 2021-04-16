""" CSC111 Final Project: Bus Stop Creator
utility_unctions.py

================================================================================
This contains utility functions used in various calculations for other function
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu
"""
import math
import numpy as np
from pygame_stuff.drawing import WIDTH, HEIGHT


# ========================================================
# General mathematics
# ========================================================

def calc_inertia(place_coords: list, centers: list) -> float:
    """
    Inertia is the within-cluster sum-of-squares.
    It is a measure of how far 'every point in a cluster' is from the center (another point)

    Since the the centers of clusters calculated in _get_bus_stops() are being projected onto
    streets (forming the projected centers), a new inertia has to be calculated for
    the new projected centers

    - place_coords is a list of the coordinates of the places in self._places
    - centers is a list of the centers of the len(centers) clusters

    Read this for more info:
    https://scikit-learn.org/stable/modules/clustering.html#k-means

    Preconditions:
        - all(0 <= center[0] <= WIDTH for center in centers)
        - all(0 <= center[1] <= HEIGHT for center in centers)
    """
    inertia = 0.0
    for e in range(len(place_coords)):
        distances = []
        for i in range(len(centers)):
            distances.append(distance(tuple(place_coords[e]), centers[i]))
        inertia += min(distances) ** 2
    return inertia


def local_max(lst: list) -> list:
    """
    Preconditions:
          - all({type(i) == int or type(i) == float for i in lst})
    """
    maxes = []
    for i in range(len(lst)):
        if i not in (0, len(lst) - 1):
            if lst[i - 1] < lst[i] > lst[i + 1]:
                maxes.append(lst[i])

    return maxes


def projection(a: tuple, b: tuple, p: tuple) -> tuple[float, float]:
    """Return the coordinates of the projection of point p onto line ab
    """
    vec_a = np.asarray(a)
    vec_b = np.asarray(b)
    vec_p = np.asarray(p)

    ap = vec_p - vec_a
    ab = vec_b - vec_a

    t = np.dot(ap, ab) / np.dot(ab, ab)
    t = max(0, min(1, t))
    res = vec_a + t * ab

    return tuple(res)


def distance(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """Return the Euclidean distance between two coordinates
    """
    x_squared = (pos1[0] - pos2[0]) ** 2
    y_squared = (pos1[1] - pos2[1]) ** 2

    return math.sqrt(x_squared + y_squared)


def manhattan(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """Return the Manhattan distance between two coordinates
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def diagonal(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """Return the largest difference in coordinates
    """
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))


# ========================================================
# Maps and geography
# ========================================================

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


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['math', 'numpy'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
