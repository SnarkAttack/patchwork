from enum import IntEnum
import logging

PLAYER1 = 1
PLAYER2 = -1

class RotationDirection(IntEnum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3