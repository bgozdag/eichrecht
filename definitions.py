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

    def __init__(self, address, length, data_type):
        """Constructor"""
        self.address = address
        self.length = length
        self.data_type = data_type

class Device(ABC):
    """Device base class"""
    pass

class Bauer(Device):
    """Bauer device"""
    MAX_BAUD_RATE = 115200

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()
        self.manufacturer = Register(40004, 16, DataType.STRING)
        self.model = Register(40020, 16, DataType.STRING)
        self.options = Register(40036, 8, DataType.STRING)
        self.version = Register(40044, 8, DataType.STRING)
        self.serial_number = Register(40052, 16, DataType.STRING)
        self.baud_rate = Register(40082, 2, DataType.UINT32)
        self.epoch_time = Register(40260, 2, DataType.UINT32)
        self.voltageL1 = Register(40098, 1, DataType.UINT16)
        self.voltageL2 = Register(40099, 1, DataType.UINT16)
        self.voltageL3 = Register(40100, 1, DataType.UINT16)
        self.current = Register(40092, 1, DataType.UINT16)
        self.currentL1 = Register(40093, 1, DataType.UINT16)
        self.currentL2 = Register(40094, 1, DataType.UINT16)
        self.currentL3 = Register(40095, 1, DataType.UINT16)
        self.power = Register(40108, 1, DataType.UINT16)
        self.powerL1 = Register(40109, 1, DataType.UINT16)
        self.powerL2 = Register(40110, 1, DataType.UINT16)
        self.powerL3 = Register(40111, 1, DataType.UINT16)
        self.energy = Register(40136, 2, DataType.UINT32)
        self.snapshot_status = Register(40524, 1, DataType.UINT16)
        self.ocmf = Register(41795, 496, DataType.STRING)
        self.meta1 = Register(40279, 70, DataType.STRING)
        self.meta2 = Register(40349, 50, DataType.STRING)
        self.meta3 = Register(40399, 50, DataType.STRING)