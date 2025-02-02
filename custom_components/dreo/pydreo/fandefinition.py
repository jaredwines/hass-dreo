from enum import Enum

class OscillationSupport(Enum):
    NONE = 0
    HORIZONTAL = 1
    BOTH = 2

class PyDreoFanDefinition():

    def __init__(self, 
                 speed_range: range,
                 oscillation_support: OscillationSupport):
        self.speed_range = speed_range
        self.oscillation_support = oscillation_support
        