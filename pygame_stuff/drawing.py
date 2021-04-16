""" CSC111 Final Project: Bus Stop Creator
drawing.py

================================================================================
This file contains the class definitions and constants that will make drawing the city easier.
  - Drawable
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu
"""
import pygame

GRASS = (123, 168, 50)
STREET = (59, 59, 59)
PLACE = (117, 0, 0)
BUS_STOP = (255, 255, 0)
HIGHLIGHTED_STREET = (153, 0, 76)
COLOURS = [(153, 0, 76), (252, 186, 3), (3, 169, 252), (40, 3, 252), (252, 3, 45),
           (252, 3, 3), (3, 252, 140), (136, 3, 252)]


class Drawable:
    """An abstract class represting the drawable items in the pygame window"""

    def draw(self, screen: pygame.Surface) -> None:
        """Returns the drawn form of the drawable item within the pygame window"""
        raise NotImplementedError
