""" CSC111 Final Project: Bus Stop Creator
utility_unctions.py

================================================================================
This contains utility functions used in various calculations for other function
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu
"""
import math
import numpy as np


# ========================================================
# General mathematics
# ========================================================

def local_max(lst: list) -> list:
    """
    Preconditions:
          - all({type(i) == int or type(i) == float for i in lst})
    """
    maxes = []
    for i in range(len(lst)):
        if i not in (0, len(lst) - 1):
            if lst[i - 1] < lst[i] > lst[i + 1]:
                maxes.append(lst[i])

    return maxes


def projection(a: tuple, b: tuple, p: tuple) -> tuple[float, float]:
    """Return the coordinates of the projection of point p onto line ab
    """
    vec_a = np.asarray(a)
    vec_b = np.asarray(b)
    vec_p = np.asarray(p)

    ap = vec_p - vec_a
    ab = vec_b - vec_a

    t = np.dot(ap, ab) / np.dot(ab, ab)
    t = max(0, min(1, t))
    res = vec_a + t * ab

    return tuple(res)


def distance(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """Return the Euclidean distance between two coordinates
    """
    x_squared = (pos1[0] - pos2[0]) ** 2
    y_squared = (pos1[1] - pos2[1]) ** 2

    return math.sqrt(x_squared + y_squared)


def manhattan(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """Return the Manhattan distance between two coordinates
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def diagonal(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """Return the largest difference in coordinates
    """
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['math', 'numpy'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
