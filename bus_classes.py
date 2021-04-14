""" CSC111 Final Project: Bus Stop Creator
bus_classes.py

================================================================================
This file contains the class definitions for a bus stop and the route
that a bus will take.
  - Route
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu
"""

from city_classes import _Place


class Route:
    """The route the bus took to pass through some bus stops
    """
    path: list[_Place]
    distance: float
    travel_time: float

    def __init__(self) -> None:
        self.path = []
        self.distance = 0
        self.travel_time = 0

    def simulate_route(self) -> dict:
        """Simulates a route (list of BusStops in order) a bus takes. Returns information
        about the trip the bus took.
        """
        ...
