"""This file contains the class and methods used to represent a city's road network
"""

from __future__ import annotations
from typing import Any
from pygame_stuff.drawing import Drawable

import pygame
import math


class _Place(Drawable):
    """A vertex in the City graph, used to represent a place in the city.

    Instance Attributes:
        - pos: The coordinates of this place
        - name: The name of this place
        - neighbours: The vertices that are adjacent to this vertex and their respective distances
    """
    name: str
    pos:  tuple[int, int]
    neighbours: dict[_Place, float]

    def __init__(self, name: str, x: int, y: int) -> None:
        self.name = name
        self.pos = (x, y)
        self.neighbours = dict()

    def draw(self, screen: pygame.screen) -> None:
        """Draws this item within the pygame window
        """
        # TODO


class _Intersection(_Place):
    """A vertex in the City graph, used to represent a road intersection in the city.

    Instance Attributes:
        - traffic_light: 0 for a green light, 1 for a red light
        - stop_time: The average stop time (in seconds) for a red light
    """
    traffic_light: int
    stop_time: float

    def __init__(self, name: str, x: int, y: int, traffic_light: int, stop_time: int) -> None:
        super().__init__(name, x, y)
        self.traffic_light = traffic_light
        self.stop_time = stop_time

    def draw(self, screen: pygame.screen) -> None:
        """Draws this item within the pygame window
        """
        # TODO


class City:
    """A graph used to represent a city's road network

    Instance Attributes:
        - traffic_light: 0 for a green light, 1 for a red light
        - stop_time: The average stop time (in seconds) for a red light
    """
    _places: dict[Any, _Place]
    # population: int

    def __init__(self) -> None:
        self._places = dict()

    def add_place(self, name: str, x: int, y: int) -> None:
        """Add a _Place to the dictionary with the same coordinates as the mouse click
        """
        if name not in self._places:
            self._places[name] = _Place(name, x, y)

    def add_street(self, name1: str, name2: str) -> None:
        """Connect two _Places together with a street

        Raise a ValueError if either name do not appear as places in the city.
        """
        if name1 in self._places and name2 in self._places:
            p1 = self._places[name1]
            p2 = self._places[name2]

            # Calculating distance between two points
            x_squared = (p1.pos[0] - p2.pos[0])**2
            y_squared = (p1.pos[1] - p2.pos[1])**2
            dist = math.sqrt(x_squared + y_squared)

            p1.neighbours.update({p2: dist})
            p2.neighbours.update({p1: dist})
        else:
            raise ValueError
            # maybe change to warning message in pygame

    def get_neighbours(self, name: str) -> set:
        """Return a set of the neighbours (the names) of the given name.

        Raise a ValueError if name does not appear as a place in this city.
        """
        if name in self._places:
            p = self._places[name]
            return {neighbour.name for neighbour in p.neighbours}
        else:
            raise ValueError

    def adjacent(self, name1: str, name2: str) -> bool:
        """Return if name1 and name2 are adjacent places in this city.

        Return False if name1 or name2 do not appear as places in this city.
        """
        if name1 in self._places and name2 in self._places:
            p1 = self._places[name1]
            return any(v2.name == name2 for v2 in p1.neighbours)
        else:
            return False
