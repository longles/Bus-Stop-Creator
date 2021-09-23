""" CSC111 Final Project: Bus Stop Creator
place.py

================================================================================
This file contains the class definitions for the objects needed to represent
a city.
  - Place
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu
"""

from __future__ import annotations

from visual.drawing import *


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
    STREET_WIDTH = 10

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
    """A vertex in the City graph, used to represent a road intersection in the city. Functionally
     the same as _Place but it is drawn as a grey circle on the canvas.
    """

    def __init__(self, pos: tuple[float, float]) -> None:
        super().__init__(pos)

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
        pygame.draw.circle(screen, STREET, (x, y), self.STREET_WIDTH)


class _BusStop(_Place):
    """A vertex in the City graph, used to represent a bus stop in the city.

    Instance Attributes:
        - wait_time: Time the bus takes at the bus stop
        - neighbours: The bus stop's neighbours
    """
    neighbours: dict[_Place, float]
    WIDTH: int = 20

    def __init__(self, pos: tuple[float, float]) -> None:
        super().__init__(pos)
        self.neighbours = dict()

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
