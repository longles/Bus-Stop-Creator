"""This file contains the class and methods used to represent a city's road network
"""

from __future__ import annotations
from pygame_stuff.drawing import Drawable

import pygame
import math
import hashlib


class _Place(Drawable):
    """A vertex in the City graph, used to represent a place in the city.

    Instance Attributes:
        - pos: The coordinates of the place
        - name: The unique id of the place
        - neighbours: The vertices that are adjacent to this vertex and their respective distances
    """
    id: str
    pos:  tuple[float, float]
    neighbours: dict[_Place, float]

    def __init__(self, name: str, pos: tuple[float, float]) -> None:
        self.name = name
        self.pos = pos
        self.neighbours = dict()

    def draw(self, screen: pygame.Surface) -> None:
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

    def draw(self, screen: pygame.Surface) -> None:
        """Draws this item within the pygame window
        """
        # TODO


class City:
    """A graph used to represent a city's road network

    Instance Attributes:
        - _places: All the the places in the city
        - _positions: Dictionary of coordinate: _Place pairs in the city
    """
    _places: dict[tuple[float, float], _Place]

    def __init__(self) -> None:
        self._places = dict()

    def add_place(self, pos: tuple[float, float]) -> None:
        """Add a _Place to the dictionary with the same coordinates as the mouse click
        """
        if pos not in self._places:
            place_id = hashlib.md5(f'{pos}'.encode('utf-8')).hexdigest()
            p = _Place(place_id, pos)
            self._places.update({pos: p})

    def add_street(self, pos1: tuple, pos2: tuple) -> None:
        """Connect two _Places together with a street

        Raise a ValueError if either name do not appear as places in the city.
        """
        if pos1 in self._places and pos2 in self._places:
            p1 = self._places[pos1]
            p2 = self._places[pos2]

            # Calculating distance between two points
            x_squared = (p1.pos[0] - p2.pos[0])**2
            y_squared = (p1.pos[1] - p2.pos[1])**2
            dist = math.sqrt(x_squared + y_squared)

            p1.neighbours.update({p2: dist})
            p2.neighbours.update({p1: dist})
        else:
            raise ValueError
            # maybe change to warning message in pygame

    def get_neighbours(self, pos: tuple[float, float]) -> set:
        """Return a set of the neighbours (the names) of the at the given position.

        Raise a ValueError if name does not appear as a place in this city.
        """
        if pos in self._places:
            p = self._places[pos]
            return {neighbour.pos for neighbour in p.neighbours}
        else:
            raise ValueError

    def adjacent(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> bool:
        """Return if places at pos1 and pos2 are adjacent in this city.

        Return False if name1 or name2 do not appear as places in this city.
        """
        if pos1 in self._places and pos2 in self._places:
            p1 = self._places[pos1]
            return any(p2.pos == pos2 for p2 in p1.neighbours)
        else:
            return False
