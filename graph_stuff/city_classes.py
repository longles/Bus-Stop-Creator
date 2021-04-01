"""This file contains the class and methods used to represent a city's road network
"""

from __future__ import annotations
from pygame_stuff.drawing import Drawable
from typing import Union

import pygame
import math



class _Place(Drawable):
    """A vertex in the City graph, used to represent a place in the city.

    Instance Attributes:
        - pos: The coordinates of the place
        - uid: The unique identifier of the place
        - neighbours: The vertices that are adjacent to this vertex and their respective distances
    """
    pos:  tuple[float, float]
    neighbours: dict[_Place, float]

    def __init__(self, pos: tuple[float, float]) -> None:
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

    def __init__(self, pos, traffic_light: int, stop_time: int) -> None:
        super().__init__(pos)
        self.traffic_light = traffic_light
        self.stop_time = stop_time

    def draw(self, screen: pygame.Surface) -> None:
        """Draws this item within the pygame window
        """
        # TODO


class City:
    """A graph used to represent a city's road network

    Instance Attributes:
        - _places: Dictionary of coordinate: place pairs in the city
    """
    _places: dict[tuple[float, float], _Place]

    def __init__(self) -> None:
        self._places = dict()

    def add_place(self, pos: tuple[float, float]) -> None:
        """Add a _Place to the dictionary with the same coordinates as the mouse click
        """
        if pos not in self._places:
            # generates a random string for the id
            p = _Place(pos)
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

    def adjacent(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> bool:
        """Return if places at pos1 and pos2 are adjacent in this city.

        Return False if name1 or name2 do not appear as places in this city.
        """
        if pos1 in self._places and pos2 in self._places:
            p1 = self._places[pos1]
            return any(p2.pos == pos2 for p2 in p1.neighbours)
        else:
            return False

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
            if distances[curr] == float('inf'):
                break

            for neighbour in self._places[curr].neighbours:
                if neighbour.pos not in visited:
                    new_dist = distances[curr] + self.get_distance(curr, neighbour.pos)

                    if new_dist < distances[neighbour.pos]:
                        distances[neighbour.pos] = new_dist
                        predecessor[neighbour.pos] = curr

            visited.add(curr)
            unvisited.remove(curr)

        # prints the shortest path in the form of a list
        shortest_path = []
        current = end
        if current not in predecessor:
            predecessor[current] = None

        while predecessor[current] is not None:
            shortest_path.insert(0, current)
            current = predecessor[current]
        if shortest_path != []:
            shortest_path.insert(0, current)
        else:
            return None

        return (shortest_path, distances[end])


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

    print('(0,0) -> (10, 15):', toronto.shortest_path((0, 0), (10, 15)))
    print('(3, 4) -> (9, 0):', toronto.shortest_path((3, 4), (9, 0)))
