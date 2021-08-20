from enum import Enum, unique


@unique
class SidePanelSide(Enum):
    LEFT = 0
    RIGHT = 1


@unique
class WidePanelPosition(Enum):
    TOP = 0
    BOTTOM = 1


@unique
class ChangeMetricType(Enum):
    ABSOLUTE = 0
    RELATIVE = 1


@unique
class StorageType(Enum):
    LOCAL = 0
    MEMORY = 1
    SESSION = 2


@unique
class LabelPosition(Enum):
    LEFT = 0
    TOP = 1
