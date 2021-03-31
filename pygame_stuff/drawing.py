"""This file contains the classes and functions used to draw the city with pygame"""

import pygame


class Drawable:
    """An abstract class represting the drawable items in the pygame window"""

    def draw(self, screen: pygame.Surface) -> None:
        """Returns the drawn form of the drawable item within the pygame window"""
        raise NotImplementedError
