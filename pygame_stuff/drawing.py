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
WIDTH, HEIGHT = 1000, 800


class Drawable:
    """An abstract class representing the drawable items in the pygame window"""

    def draw(self, screen: pygame.Surface) -> None:
        """Returns the drawn form of the drawable item within the pygame window"""
        raise NotImplementedError


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pygame'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
