"""This file contains the class and methods used to represent a city's road network
"""

from __future__ import annotations
from typing import Any
from pygame_stuff.drawing import Drawable
import pygame


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

    def add_place(self, name: str) -> None:
        """Add a _Place to the dictionary with the same coordinates as the mouse click
        """
        # TODO

    def add_street(self, p1: str, p2: str) -> None:
        """Connect two _Places together with a street
        """
        # TODO
