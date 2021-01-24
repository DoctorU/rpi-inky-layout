from enum import Enum, unique


@unique
class Rotation(Enum):
    """
        Rotation
        An enumeration to indicate the rotation of a Layout.
    """
    UP = 0  # Normal
    RIGHT = 1  # rotate left 90°
    DOWN = 2  # rotate 180°
    LEFT = 3  # rotate right 90°
