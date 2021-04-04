""" CSC111 Final Project: Bus Stop Creator
city_classes.py

================================================================================
This file contains the class definitions for the objects needed to represent
a city.
  - City
  - _Place
  - _Intersection
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu
"""

from __future__ import annotations
from pygame_stuff.drawing import *
from typing import Union

import pygame
import math


class _Place(Drawable):
    """A vertex in the City graph, used to represent a place in the city.

    Instance Attributes:
        - pos: The coordinates of the CENTRE of the place
        - neighbours: The vertices that are adjacent to this vertex and their respective distances
        - WIDTH: The width of this place in pixels, this place will be drawn as a square with
                 side length WIDTH
    """
    pos:  tuple[float, float]
    neighbours: dict[_Place, float]
    WIDTH: int = 20

    def __init__(self, pos: tuple[float, float]) -> None:
        self.pos = pos
        self.neighbours = dict()

    def draw(self, screen: pygame.Surface) -> None:
        """Draws this item within the pygame window
        """
        x, y = self.pos
        rect = pygame.Rect(x - self.WIDTH // 2, y - self.WIDTH // 2, self.WIDTH, self.WIDTH)
        pygame.draw.rect(screen, PLACE, rect)

    def pos_on_place(self, m_pos: tuple[int, int]) -> bool:
        """
        Return whether the given mouse position <m_pos> is on this place on the canvas.
        """
        x, y = self.pos  # x and y coords of this place's centre on the canvas

        top_left_corner = (x - self.WIDTH // 2, y - self.WIDTH // 2)
        bottom_right_corner = (x + self.WIDTH // 2, y + self.WIDTH // 2)

        x1, y1 = top_left_corner
        x2, y2 = bottom_right_corner

        mx, my = m_pos

        # See if m_pos is within the box bounded by top left and bottom right corners
        if (x1 < mx < x2) and (y1 < my < y2):
            return True
        return False


class _Intersection(_Place):
    """A vertex in the City graph, used to represent a road intersection in the city.

    Instance Attributes:
        - traffic_light: 0 for a green light, 1 for a red light
        - stop_time: The average stop time (in seconds) for a red light
    """
    traffic_light: int
    stop_time: float

    def __init__(self, pos, traffic_light: int, stop_time: int) -> None:
        super().__init__(pos)
        self.traffic_light = traffic_light
        self.stop_time = stop_time

    def draw(self, screen: pygame.Surface) -> None:
        """Draws this item within the pygame window
        """
        # TODO


class City(Drawable):
    """A graph used to represent a city's road network

    Instance Attributes:
        - _places: Dictionary of coordinate: place pairs in the city
        - _streets: Set of coordinate pairs which define a street
                    For example, ((x, y), (a, b)) is a single street that connects (x, y)
                    to (a, b). This attribute is mainly used to facilitate drawing
        - _STREET_WIDTH: The width of a street in pixels on the pygame window
    """
    _places: dict[tuple, _Place]
    _streets: set[tuple[tuple, tuple]]
    _STREET_WIDTH: int = 10

    def __init__(self) -> None:
        self._places = dict()
        self._streets = set()

    def add_place(self, pos: tuple[float, float]) -> None:
        """Add a _Place to the dictionary with the same coordinates as the mouse click
        """
        if pos not in self._places:
            p = _Place(pos)
            self._places.update({pos: p})

    def add_street(self, pos1: tuple, pos2: tuple) -> None:
        """Connect two _Places together with a street
        Raise a ValueError if either positions do not correspond to places in the city.

        Preconditions:
          - pos1 != pos2
        """
        if (pos1 in self._places) and (pos2 in self._places):
            p1 = self._places[pos1]
            p2 = self._places[pos2]

            # Calculating distance between two points
            x_squared = (p1.pos[0] - p2.pos[0])**2
            y_squared = (p1.pos[1] - p2.pos[1])**2
            dist = math.sqrt(x_squared + y_squared)

            p1.neighbours.update({p2: dist})
            p2.neighbours.update({p1: dist})

            # Duplicate streets are fine, since self._streets is a set anyway
            self._streets.add((pos1, pos2))
        else:
            raise ValueError
            # maybe change to warning message in pygame

    def delete_place(self, pos: tuple[float, float]) -> None:
        """Remove a place from the city and remove all streets connecting to it"""
        if pos in self._places:
            p = self._places[pos]
            neighbours_copy = p.neighbours.copy()
            for neighbour in neighbours_copy:
                self.delete_street(p.pos, neighbour.pos)
            self._places.pop(pos)

    def delete_street(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> None:
        """Remove a street between two places"""
        if (pos1, pos2) in self._streets:
            p1 = self._places[pos1]
            p2 = self._places[pos2]
            p1.neighbours.pop(p2)
            p2.neighbours.pop(p1)
            self._streets.remove((pos1, pos2))
        elif (pos2, pos1) in self._streets:
            p1 = self._places[pos1]
            p2 = self._places[pos2]
            p1.neighbours.pop(p2)
            p2.neighbours.pop(p1)
            self._streets.remove((pos2, pos1))

    def get_neighbours(self, pos: tuple[float, float]) -> set:
        """Return a set of the neighbours (the names) of the at the given position.
        Raise a ValueError if name does not appear as a place in this city.
        """
        if pos in self._places:
            p = self._places[pos]
            return {neighbour.pos for neighbour in p.neighbours}
        else:
            raise ValueError

    def get_all_places(self) -> set:
        """Return set of all place coordinates in the city
        """
        return {p.pos for p in self._places.values()}

    def get_distance(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
        """Return the distance between two neighbours
        Return 0 if they are not neighbours
        """
        p1 = self._places[pos1]
        p2 = self._places[pos2]
        return p1.neighbours.get(p2, 0)

    def shortest_path(self, start: tuple[float, float], end: tuple[float, float]) \
            -> Union[tuple[list, float], None]:
        """Returns a list containing the shortest path between 'start' and 'end' and the total
        distance between the two places
        """
        if start not in self._places or end not in self._places:
            raise ValueError
        if start == end:
            return ([], 0)

        visited = set()
        unvisited = self.get_all_places()

        distances = {place: float('inf') for place in self.get_all_places()}
        distances[start] = 0

        predecessor = {place: None for place in self.get_all_places()}

        while end in unvisited:
            curr = min(unvisited, key=lambda place: distances[place])

            # if the smallest value is inf, then there is no path
            if distances[curr] == float('inf'):
                break

            for neighbour in self.get_neighbours(curr):
                if neighbour not in visited:
                    new_dist = distances[curr] + self.get_distance(curr, neighbour)
                    if new_dist < distances[neighbour]:
                        distances[neighbour] = new_dist
                        predecessor[neighbour] = curr

            visited.add(curr)
            unvisited.remove(curr)

        # prints the shortest path in the form of a list
        shortest_path = []
        curr = end
        if curr not in predecessor:
            predecessor[curr] = None

        while predecessor[curr] is not None:
            shortest_path.insert(0, curr)
            curr = predecessor[curr]

        if shortest_path != []:
            shortest_path.insert(0, curr)
        else:
            return None

        return (shortest_path, distances[end])

    def get_place_from_pos(self, m_pos: tuple[int, int]) -> Union[None, tuple[int, int]]:
        """
        Given the position of the mouse <pos>, return the POSITION of the place that the mouse
        is on.
        """
        for place_pos in self._places:
            place = self._places[place_pos]
            if place.pos_on_place(m_pos):
                return place_pos

    def draw(self, screen: pygame.Surface) -> None:
        """Draws this item within the pygame window
        """
        # Loop through the streets to draw them
        for street in self._streets:
            self._draw_street(street, screen)

        # Loop through the places to draw them
        for pos in self._places:
            place = self._places[pos]
            place.draw(screen)

    def _draw_street(self, street: tuple[tuple, tuple], screen: pygame.Surface) -> None:
        """
        A helper method to draw a street (a line) between two positions on a screen.
        """
        pygame.draw.line(screen, STREET, street[0], street[1], self._STREET_WIDTH)


if __name__ == '__main__':
    toronto = City()

    toronto.add_place((0, 0))
    toronto.add_place((3, 4))
    toronto.add_place((10, 15))
    toronto.add_place((9, 0))
    toronto.add_place((0, 7))

    toronto.add_street((0, 0), (9, 0))
    toronto.add_street((9, 0), (10, 15))
    toronto.add_street((10, 15), (3, 4))
    toronto.add_street((3, 4), (0, 7))
    toronto.add_street((0, 7), (0, 0))
    toronto.add_street((0, 0), (10, 15))

    print('(0, 0) -> (10, 15):', toronto.shortest_path((0, 0), (10, 15)))
    print('(3, 4) -> (9, 0):', toronto.shortest_path((3, 4), (9, 0)))
