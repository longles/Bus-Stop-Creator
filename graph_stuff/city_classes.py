""" CSC111 Final Project: Bus Stop Creator
city_classes.py

================================================================================
This file contains the class definitions for the objects needed to represent
a city.
  - City
  - Place
  - _Intersection
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu

city = City.build_from_file("data/map.txt", "data/bus.txt")
city.export_to_file("data/map_save.txt", "data/bus_save.txt")
"""

from __future__ import annotations
from typing import Union

from pygame_stuff.drawing import *
from utility_functions import *
from sklearn.cluster import KMeans

import pygame
import random
import pandas as pd

import copy
import pygame
import pandas as pd



class _Place(Drawable):
    """A vertex in the City graph, used to represent a place in the city.

    Instance Attributes:
        - pos: The coordinates of the CENTRE of the place
        - neighbours: The vertices that are adjacent to this vertex and their respective distances
        - WIDTH: The width of this place in pixels, this place will be drawn as a square with
                 side length WIDTH

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - 0 <= self.pos[0] <= WIDTH and 0 <= self.pos[1] <= HEIGHT
    """
    pos: tuple[float, float]
    neighbours: dict[_Place, float]
    WIDTH: int = 20

    def __init__(self, pos: tuple[float, float]) -> None:
        self.pos = pos
        self.neighbours = dict()

    def __str__(self) -> str:
        """
        Convert this place to a string in the following format: 'place x y' where
        x and y are the coordinates of this place
        """
        x, y = self.pos
        return "place " + str(x) + " " + str(y)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws this vertex within the pygame window
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

    Representation Invariants:
        # TODO
    """
    traffic_light: int
    stop_time: float

    def __init__(self, pos: tuple[float, float],
                 traffic_light: int = 0, stop_time: int = 0) -> None:
        # TODO: adjust the default values later on
        super().__init__(pos)
        self.traffic_light = traffic_light
        self.stop_time = stop_time

    def __str__(self) -> str:
        """
        Convert this intersection to a string in the following format: 'intersection x y' where
        x and y are the coordinates of this place
        """
        x, y = self.pos
        return "intersection " + str(x) + " " + str(y)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws this vertex within the pygame window
        """
        x, y = self.pos
        pygame.draw.circle(screen, STREET, (x, y), City.STREET_WIDTH)


class _BusStop(_Place):
    """A vertex in the City graph, used to represent a bus stop in the city.

    Instance Attributes:
        - wait_time: Time the bus takes at the bus stop

    Representation Invariants:
        # TODO
    """
    wait_time: float
    neighbours: dict[_Place, float]
    WIDTH: int = 20

    def __init__(self, pos: tuple[float, float]) -> None:
        # TODO: adjust the default values later on
        super().__init__(pos)
        self.neighbours = dict()
        self.wait_time = random.randint(1, 5)

    def __str__(self) -> str:
        """
        Convert this place to a string in the following format: 'bus_stop x y' where
        x and y are the coordinates of this place
        """
        x, y = self.pos
        return "bus_stop " + str(x) + " " + str(y)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws this vertex within the pygame window
        """
        x, y = self.pos
        rect = pygame.Rect(x - self.WIDTH // 2, y - self.WIDTH // 2, self.WIDTH, self.WIDTH)
        pygame.draw.rect(screen, BUS_STOP, rect)

    def pos_on_bus_stop(self, m_pos: tuple[int, int]) -> bool:
        """Return whether the given mouse position <m_pos> is on this bus stop on the canvas.
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


class City(Drawable):
    """A graph used to represent a city's road network

   Instance Attributes:
        - STREET_WIDTH: The width of a street in pixels on the pygame window

    Private Instance Attributes:
        - _places: Dictionary of coordinate: place pairs in the city
        - _streets: Set of coordinate pairs which define a street
                    For example, ((x, y), (a, b)) is a single street that connects (x, y)
                    to (a, b). This attribute is mainly used to facilitate drawing
        - _bus_stops: a list of 1. dictionary of coordinate to bus stop pairs 2. inertia
                    (basically measures how good a bus stop system is, the less the better)
        - _bus_routes: # TODO

    Representation Invariants:
        # TODO
    """
    _places: dict[tuple, _Place]
    _streets: set[tuple[tuple, tuple]]
    _bus_stops: list[dict[tuple: _BusStop], float]
    _bus_routes: list[list[tuple]]
    STREET_WIDTH: int = 10

    def __init__(self) -> None:
        self._places = dict()
        self._streets = set()
        self._bus_stops = [dict(), -1.0]
        self._bus_routes = []

    # ========================================================
    # File I/O
    # ========================================================

    @staticmethod
    def build_from_file(map_file: str, bus_file: str) -> City:
        """
        Build a city from the given .txt files.

        Preconditions:
          - The input file is in the same format described in export_to_file
        """
        city = City()
        calculate_inertia = False


        with open(bus_file, 'r') as f:
            for line in f:
                parsed_line = line.split()
          
                # Read bus stops from txt file
                if parsed_line[0] == "bus_stop":
                    x, y = int(parsed_line[1]), int(parsed_line[2])
                    city.add_bus_stop((x, y))

                # Read the inertia for this set of bus stops
                elif parsed_line[0] == "inertia":
                    # If its -1.0 it means the inertia hasn't been calculated yet
                    if float(parsed_line[1]) == -1.0:
                        # Calculate the inertia
                        calculate_inertia = True
                    # Otherwise save the inertia
                    else:
                        city.change_inertia(float(parsed_line[1]))

                # Read bus routes from txt file
                else:
                    # Notice len(parsed_line) is always even
                    route = []
                    for i in range(int(len(parsed_line) / 2)):
                        x1, y1 = int(parsed_line[2 * i]), int(parsed_line[2 * i + 1])
                        route.append((x1, y1))
                    city.add_bus_route(route)

        with open(map_file, 'r') as f:
            for line in f:
                parsed_line = line.split()

                if parsed_line[0] in {"place", "intersection"}:
                    # The line encodes a place
                    kind = parsed_line[0]
                    x, y = int(parsed_line[1]), int(parsed_line[2])
                    city.add_place((x, y), kind)
                else:
                    # The line encodes a street
                    x1, y1 = int(parsed_line[0]), int(parsed_line[1])
                    x2, y2 = int(parsed_line[2]), int(parsed_line[3])
                    city.add_street((x1, y1), (x2, y2))

        places = city.get_all_places()
        centers = list(city._bus_stops[0].keys())
        if calculate_inertia and len(places) != 0 and len(centers) != 0:
            city.change_inertia(calc_inertia(list(places), centers))

        return city

    def export_to_file(self, output_map: str, output_bus: str) -> None:
        """
        Export the city to a .txt file in the following format:

        For every place/bus stop:
            <place type> <x coord> <y coord>

        For every street:
            <x coord 1> <y coord 1> <x coord 2> <y coord 2>

        For every bus route:
            <x coord 1> <y coord 1> <x coord 2> <y coord 2> <x coord 3> <y coord 3> ...

        Preconditions:
            - output_map is a valid file
            - output_bus is a valid file
        """
        with open(output_map, 'w') as f:
            # First, write all the place information
            for pos in self._places:
                place = self._places[pos]

                f.write(str(place) + '\n')

            # Next, write all the street information
            for street in self._streets:
                p1, p2 = street
                x1, y1 = p1
                x2, y2 = p2
                f.write(str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + '\n')

        with open(output_bus, 'w') as f:
            # First, write down the inertia
            f.write("inertia " + str(self._bus_stops[1]) + '\n')

            # Second, write all the bus stop information
            for pos in self._bus_stops[0]:
                place = self._bus_stops[0][pos]
                f.write(str(place) + '\n')

            # Next, write all the bus routes information
            for route in self._bus_routes:
                route_string = ""
                for place in route:
                    x1, y1 = place
                    route_string += str(x1) + " " + str(y1) + " "
                f.write(route_string + '\n')

    # ========================================================
    # Mutating instance attributes
    # ========================================================

    def add_place(self, pos: tuple[float, float], kind: str = 'place') -> None:
        """
        Add a Place to the dictionary with the same coordinates as the mouse click

        Preconditions:
            - 0 <= pos[0] <= WIDTH and 0 <= pos[1] <= HEIGHT
        """
        if pos not in self._places:
            if kind == 'intersection':
                p = _Intersection(pos)
            else:
                p = _Place(pos)
            self._places.update({pos: p})

    def delete_place(self, pos: tuple[float, float]) -> None:
        """
        Remove a place from the city and remove all streets connecting to it

        Preconditions:
            - 0 <= pos[0] <= WIDTH and 0 <= pos[1] <= HEIGHT
        """
        if pos in self._places:
            p = self._places[pos]
            neighbours_copy = p.neighbours.copy()
            for neighbour in neighbours_copy:
                self.delete_street(p.pos, neighbour.pos)
            self._places.pop(pos)

    def add_street(self, pos1: tuple, pos2: tuple) -> None:
        """
        Connect two _Places together with a street
        Raise a ValueError if either positions do not correspond to places in the city.

        Preconditions:
          - pos1 != pos2
        """
        if (pos1 in self._places or pos1 in self._bus_stops[0]) and \
                (pos2 in self._places or pos2 in self._bus_stops[0]):
            if pos1 in self._places:
                p1 = self._places[pos1]
            else:
                p1 = self._bus_stops[0][pos1]

            if pos2 in self._places:
                p2 = self._places[pos2]
            else:
                p2 = self._bus_stops[0][pos2]

            dist = distance(pos1, pos2)
            p1.neighbours.update({p2: dist})
            p2.neighbours.update({p1: dist})

            # Prevent duplicate streets: (a, b) = (b, a)
            if (pos2, pos1) not in self._streets:
                self._streets.add((pos1, pos2))
        else:
            raise ValueError

    def delete_street(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> None:
        """
        Remove a street between two places

        Preconditions:
            - 0 <= pos[0] <= WIDTH and 0 <= pos[1] <= HEIGHT
        """
        if (pos1, pos2) in self._streets:
            if pos1 in self._places:
                p1 = self._places[pos1]
            else:
                p1 = self._bus_stops[0][pos1]

            if pos2 in self._places:
                p2 = self._places[pos2]
            else:
                p2 = self._bus_stops[0][pos2]
            p1.neighbours.pop(p2, None)
            p2.neighbours.pop(p1, None)
            self._streets.remove((pos1, pos2))
        elif (pos2, pos1) in self._streets:
            if pos1 in self._places:
                p1 = self._places[pos1]
            else:
                p1 = self._bus_stops[0][pos1]

            if pos2 in self._places:
                p2 = self._places[pos2]
            else:
                p2 = self._bus_stops[0][pos2]
            p1.neighbours.pop(p2, None)
            p2.neighbours.pop(p1, None)
            self._streets.remove((pos2, pos1))

    def add_bus_stop(self, pos: tuple[float, float]) -> None:
        """
        Add a _BusStop to the dictionary self._bus_stops[0]

        Preconditions:
            - 0 <= pos[0] <= WIDTH and 0 <= pos[1] <= HEIGHT
        """
        if pos not in self._bus_stops[0]:
            p = _BusStop(pos)
            self._bus_stops[0].update({pos: p})

    def clear_bus_stops(self) -> None:
        """Clear all bus stops and reconnect the "disconnected" streets

                    A----BUS_STOP---B becomes A--------B
        """
        # Reconnect the "disconnected" streets caused by _bus_stop_projected()
        changed_streets = copy.copy(self._streets)
        for street in changed_streets:
            p1 = street[0]
            p2 = street[1]
            if (p1 in self._places and p1 in self._bus_stops[0]) or (
                    p2 in self._places and p2 in self._bus_stops[0]):
                pass
            elif p1 in self._bus_stops[0]:
                streets2 = copy.copy(changed_streets)
                streets2.remove(street)
                for street2 in streets2:
                    p3 = street2[0]
                    p4 = street2[1]
                    if p3 == p1:
                        self.delete_street(p1, p2)
                        self.delete_street(p3, p4)
                        self.add_street(p2, p4)
                        break
                    elif p4 == p1:
                        self.delete_street(p1, p2)
                        self.delete_street(p3, p4)
                        self.add_street(p2, p3)
                        break
            elif p2 in self._bus_stops[0]:
                streets2 = copy.copy(changed_streets)
                streets2.remove(street)
                for street2 in streets2:
                    p3 = street2[0]
                    p4 = street2[1]
                    if p3 == p2:
                        self.delete_street(p1, p2)
                        self.delete_street(p3, p4)
                        self.add_street(p1, p4)
                        break
                    elif p4 == p2:
                        self.delete_street(p1, p2)
                        self.delete_street(p3, p4)
                        self.add_street(p1, p3)
                        break

        # Clear all bus stops
        self._bus_stops[0].clear()

    def add_bus_route(self, route: list[tuple]):
        """Add a bus route to the list self._bus_routes

        Preconditions:
            # TODO
        """
        if route not in self._bus_routes:
            self._bus_routes.append(route)

    def clear_bus_routes(self) -> None:
        """Clear all bus routes
        """
        self._bus_routes = []

    def change_inertia(self, inertia: float) -> None:
        """Change the inertia of the current bus system
        """
        self._bus_stops[1] = inertia

    # ========================================================
    # Accessing instance attributes
    # ========================================================

    def get_neighbours(self, pos: tuple[float, float]) -> set:
        """
        Return a set of the neighbours (the names) of the at the given position.
        Raise a ValueError if name does not appear as a place in this city.

        Preconditions:
            - 0 <= pos[0] <= WIDTH and 0 <= pos[1] <= HEIGHT
        """
        if pos in self._places:
            p = self._places[pos]
            return {neighbour.pos for neighbour in p.neighbours}
        elif pos in self._bus_stops[0]:
            p = self._bus_stops[0][pos]
            return {neighbour.pos for neighbour in p.neighbours}
        else:
            raise ValueError

    def get_all_places(self) -> set:
        """Return set of all place coordinates in the city that is not a bus stop
        """
        return set(pos for pos in self._places)

    def get_all_bus_stops(self) -> set:
        """Return set of all coordinates in the city that is a bus stop
        """
        return set(pos for pos in self._bus_stops[0])

    def get_distance(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
        """
        Return the distance between two neighbours
        Return 0 if they are not neighbours

        Preconditions:
            - 0 <= pos1[0] <= WIDTH and 0 <= pos1[1] <= HEIGHT
            - 0 <= pos2[0] <= WIDTH and 0 <= pos2[1] <= HEIGHT
        """
        if pos1 in self._places:
            p1 = self._places[pos1]
        else:
            p1 = self._bus_stops[0][pos1]
        if pos2 in self._places:
            p2 = self._places[pos2]
        else:
            p2 = self._bus_stops[0][pos2]
        return p1.neighbours.get(p2, 0)

    def get_inertia(self) -> float:
        """
         Return the inertia of the current bus system
        """
        return self._bus_stops[1]

    # ========================================================
    # Pathfinding algorithms
    # ========================================================

    def dijkstra_path(self, start: tuple[float, float], end: tuple[float, float]) \
            -> tuple:
        """
        Returns a list containing the shortest path between 'start' and 'end' and the total
        distance between the two places

        Based on the Dijkstra’s Shortest Path Algorithm

        Preconditions:
            - 0 <= start[0] <= WIDTH and 0 <= start[1] <= HEIGHT
            - 0 <= end[0] <= WIDTH and 0 <= end[1] <= HEIGHT
        """
        if (start not in self._places and start not in self._bus_stops[0]) or \
                (end not in self._places and end not in self._bus_stops[0]):
            raise ValueError
        if start == end:
            return ([], 0)

        visited = set()
        unvisited = self.get_all_places().union(self.get_all_bus_stops())

        distances = {place: float('inf') for place in unvisited}
        distances[start] = 0

        predecessor = {place: None for place in unvisited}

        while end not in visited:
            curr = min(unvisited, key=lambda place: distances[place])

            # If the shortest distance is inf, then there is no path
            if distances[curr] == float('inf'):
                break

            for neighbour in self.get_neighbours(curr):
                new_dist = distances[curr] + self.get_distance(curr, neighbour)
                if neighbour not in visited and new_dist < distances[neighbour]:
                    distances[neighbour] = new_dist
                    predecessor[neighbour] = curr

            visited.add(curr)
            unvisited.remove(curr)

        # Printing the shortest path in the form of a list
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
            return ([], "No path exists!")

        return (shortest_path, round(distances[end], 2))

    def a_star_path(self, start: tuple[float, float], end: tuple[float, float],
                    heuristic: callable) -> tuple:
        """
        Returns a list containing the shortest path (may not be the case; read below for more info)
        between 'start' and 'end' and the total distance between the two places

        Based on the A* Shortest Path Algorithm which is a 'smart' version of Dijkstra. It uses a
        heuristic function to determine which nodes are better instead of traversing over every
        node.

        For A* to find the shortest path, the heuristic must not overestimate the
        remaining distance to the end. With a city graph, there is no particular rule to how
        streets and places must be placed (compared to a grid-based graph). As a such, basic
        heuristic functions like 'distance','diagonal' or 'manhattan' in utility_functions.py may
        overestimate the remaining distance. There are certainly custom heuristic functions out
        there that provide far better estimates but they are way beyond the scope of this
        project and course.

        As such, this implementation of A* will not always give you the shortest path.

        Preconditions:
            - 0 <= start[0] <= WIDTH and 0 <= start[1] <= HEIGHT
            - 0 <= end[0] <= WIDTH and 0 <= end[1] <= HEIGHT
        """
        if (start not in self._places and start not in self._bus_stops[0]) or \
                (end not in self._places and end not in self._bus_stops[0]):
            raise ValueError
        if start == end:
            return ([], 0)

        visited = set()
        unvisited = self.get_all_places().union(self.get_all_bus_stops())

        costs = {place: float('inf') for place in unvisited}
        costs[start] = 0

        distances = {place: 0 for place in unvisited}
        predecessor = {place: None for place in unvisited}

        while end not in visited:
            curr = min(unvisited, key=lambda place: costs[place])

            # If the smallest cost is inf, then there is no path
            if costs[curr] == float('inf'):
                break

            for neighbour in self.get_neighbours(curr):
                new_cost = costs[curr] + self.get_distance(curr, neighbour) + heuristic(curr, end)
                if neighbour not in visited and new_cost < costs[neighbour]:
                    costs[neighbour] = new_cost
                    distances[neighbour] = distances[curr] + self.get_distance(curr, neighbour)

                    predecessor[neighbour] = curr

            visited.add(curr)
            unvisited.remove(curr)

        # Printing the shortest path in the form of a list
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
            return ([], "No path exists!")

        return (shortest_path, round(distances[end], 2))

    # ========================================================
    # Bus stop algorithms
    # ========================================================

    def _bus_stop_projections(self, bus_stops: list) -> list[tuple]:
        """
        Given a bus_stop position, add a bus stop on the closest street. This will mutate the
        two endpoints of the street.
                    Theoretical bus stop position
                      C
                      |
                      |
                A-----C----------B
                    Bus stop on street

        Preconditions:
            - all(0 <= bus_stop[0] <= WIDTH for bus_stop in bus_stops)
            - all(0 <= bus_stop[1] <= HEIGHT for bus_stop in bus_stops)
        """
        bus_stops_so_far = []
        projections = []

        for bus_stop in bus_stops:
            min_dist = float('inf')
            bus_stop_proj = None
            target_street = None

            # Calculating closest street
            for street in self._streets:
                proj = projection(street[0], street[1], bus_stop)
                dist = distance(bus_stop, proj)
                if dist < min_dist:
                    min_dist = dist
                    bus_stop_proj = proj
                    target_street = street

            bus_stops_so_far.append((bus_stop_proj, target_street))

        for bus_stop_proj, target_street in bus_stops_so_far:
            if bus_stop_proj is not None and target_street is not None:
                p1 = target_street[0]
                p2 = target_street[1]

                if target_street[0] == bus_stop_proj or target_street[1] == bus_stop_proj:

                    bus_stop_proj = (int(bus_stop_proj[0]), int(bus_stop_proj[1]))
                    self.add_bus_stop(bus_stop_proj)
                    projections.append(bus_stop_proj)

                # Currently by pressing b1 in visualisation to
                # "override existing bus stops and generate new ones"
                # the "if p1 in self._places and p2 in self._places" will be satisfied every time
                elif p1 in self._places and p2 in self._places:
                    # Round bus_stop_proj's coords for pygame
                    bus_stop_proj = (int(bus_stop_proj[0]), int(bus_stop_proj[1]))
                    self.add_bus_stop(bus_stop_proj)
                    self.delete_street(p1, p2)
                    self.add_street(p1, bus_stop_proj)
                    self.add_street(p2, bus_stop_proj)
                    projections.append(bus_stop_proj)
                else:
                    projections.append(None)
            else:
                projections.append(None)

        return projections

    def get_bus_stops_num(self) -> int:
        """
        Find the k value in which an "elbow" appears (where a large increase in the variation
        of inertia is seen)
        For more info, please look at https://www.youtube.com/watch?v=4b5d3muPQmA
        """
        k = 2
        inertias = []
        variation = []
        change_in_variation = []  # We want to find the largest change in variation

        while True:
            inertias.append(self.add_bus_stops(k))
            if len(inertias) >= 2:
                variation.append(inertias[k - 2] - inertias[k - 3])
            if len(variation) >= 2:
                change_in_variation.append(variation[k - 3] - variation[k - 4])
            l_max = local_max(change_in_variation)
            if len(l_max) == 1:
                # So now a local max is found; this must be the element in
                # change_in_variation[len(change_in_variation) - 2].
                # Naturally this change in variation corresponds to the
                # difference in "variation of inertia of k = len(inertias) and inertia of
                # k = len(inertias) - 1" and "variation of inertia of k = len(inertias) - 1
                # and inertia of k = len(inertias) - 2", and so we return k = len(inertias) - 1
                return len(inertias) - 1
            elif k == 30:
                # If no local max exist, return a default value
                return 3
            k += 1

    def _get_bus_stops(self, n_clusters: int) -> list[list[tuple], list]:
        """Return a set of bus stop coordinates calculated using KMeans clustering algorithm
        """

        temp = [list(x) for x in self.get_all_places()]
        df = pd.DataFrame(temp)

        km = KMeans(n_clusters=n_clusters, init='k-means++')
        km.fit_predict(df)
        centers = km.cluster_centers_

        # km.inertia_ is the original inertia with the auto generated centroid
        return [list(map(tuple, centers)), temp]

    def calculate_inertia(self, place_coords: list, centers: list) -> float:
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
            - all(place in self._places for place in place_coords)
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

    def add_bus_stops(self, num: int) -> float:
        """Return the inertia of the bus system
        """
        km_parameters = self._get_bus_stops(num)
        bus_stops = km_parameters[0]
        self.clear_bus_stops()
        projected_centers = self._bus_stop_projections(bus_stops)

        if None not in projected_centers:
            return self.calculate_inertia(km_parameters[1], projected_centers)
        else:
            return -1.0

    # ========================================================
    # Pygame interaction
    # ========================================================

    def get_element_from_pos(self, m_pos: tuple[int, int]) -> Union[None, tuple]:
        """
        Return a tuple of (place, type).

        Given the position of the mouse <pos>, the first item returned is
        the POSITION of the place that the mouse is on, OR the street that the mouse is on
        (as a tuple of two coordinates).

        Return the type of the element (place or street) as a second item. This is None
        if there is also no element to be found.

        Preconditions:
            - 0 <= m_pos[0] <= WIDTH
            - 0 <= m_pos[1] <= HEIGHT
        """
        # First see if the mouse is on a place
        for place_pos in self._places:
            place = self._places[place_pos]
            if place.pos_on_place(m_pos):
                return place_pos, "Place"

        # Second see if the mouse is on a bus stop
        for bus_pos in self._bus_stops[0]:
            bus_stop = self._bus_stops[0][bus_pos]
            if bus_stop.pos_on_place(m_pos):
                return bus_pos, "Bus Stop"

        # If not a place, then check if it's on a street
        for street in self._streets:
            if self.pos_on_street(street, m_pos):
                return street, "Street"

        return None, None  # The mouse is on nothing

    def pos_on_street(self, street: tuple[tuple, tuple], m_pos: tuple[int, int]) -> bool:
        """
        Given a street (pair of coordinates) and mouse position <m_pos>, determine if the mouse
        is on the street.

        Preconditions:
            - street in self._streets
            - 0 <= m_pos[0] <= WIDTH
            - 0 <= m_pos[1] <= HEIGHT
        """
        # Since the street is usually drawn thicker than one pixel, I want some leeway
        threshold = self.STREET_WIDTH // 2
        a, b = street

        # A simple to way to check if the mouse pos is near a street is to compare
        # distance between a, m_pos and b, m_pos, and see if the added distance is close to
        # the distance between a, b
        street_length = self.get_distance(a, b)  # Summed distances will be compared to this

        summed = distance(a, m_pos) + distance(b, m_pos)

        return abs(summed - street_length) <= threshold

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

        # Loop through the bus stops to draw them
        for pos in self._bus_stops[0]:
            place = self._bus_stops[0][pos]
            place.draw(screen)

    def _draw_street(self, street: tuple[tuple, tuple], screen: pygame.Surface) -> None:
        """
        A helper method to draw a street (a line) between two positions on a screen.

        Preconditions:
            - street in self._streets
        """
        pygame.draw.line(screen, STREET, street[0], street[1], self.STREET_WIDTH)


    def draw_highlighted_street(self, street: tuple[tuple, tuple], screen: pygame.Surface,
                                Colour: tuple) -> None:
        """
        A helper method to draw a highlighted street (a line) between two positions on a screen.

        Preconditions:
            - street in self._streets
        """
        pygame.draw.line(screen, Colour, street[0], street[1], self.STREET_WIDTH)

