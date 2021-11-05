from abc import ABC
from enum import Enum

class DataType(Enum):
    """Register data type"""

    INT16 = "int16"
    STRING = "string"
    UINT16 = "uint16"
    UINT32 = "uint32"

class SnapshotStatus(Enum):
    VALID = 0
    INVALID = 1
    UPDATE = 2
    FAILED_GENERAL_ERROR = 3
    FAILED_NO_CHARGE_RELEASE = 4
    FAILED_INCORRECT_FEEDBACK = 5

class SnapshotType(Enum):
    SIGNED_CURRENT_SNAPSHOT = 0
    SIGNED_TURN_ON_SNAPSHOT = 1
    SIGNED_TURN_OFF_SNAPSHOT = 2
    SIGNED_START_SNAPSHOT = 3

class Register:
    """Register base class"""

    def __init__(self, name, address, length, data_type):
        """Constructor"""
        self.name = name
        self.address = address
        self.length = length
        self.data_type = data_type
