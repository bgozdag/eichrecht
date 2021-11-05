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

class Device(ABC):
    """Device base class"""
    pass

class Bauer(Device):
    """Bauer device"""
    MAX_BAUD_RATE = 115200

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()
        self.manufacturer = Register("Manufacturer", 40004, 16, DataType.STRING)
        self.model = Register("Model", 40020, 16, DataType.STRING)
        self.options = Register("Options", 40036, 8, DataType.STRING)
        self.version = Register("Version", 40044, 8, DataType.STRING)
        self.serial_number = Register("Serial Number", 40052, 16, DataType.STRING)
        self.baud_rate = Register("Baud Rate", 40082, 2, DataType.UINT32)
        self.epoch_time = Register("Epoch Time", 40260, 2, DataType.UINT32)
        self.voltageL1 = Register("VoltageL1", 40098, 1, DataType.UINT16)
        self.voltageL2 = Register("VoltageL2", 40099, 1, DataType.UINT16)
        self.voltageL3 = Register("VoltageL3", 40100, 1, DataType.UINT16)
        self.current = Register("Current", 40092, 1, DataType.UINT16)
        self.currentL1 = Register("CurrentL1", 40093, 1, DataType.UINT16)
        self.currentL2 = Register("CurrentL2", 40094, 1, DataType.UINT16)
        self.currentL3 = Register("CurrentL3", 40095, 1, DataType.UINT16)
        self.power = Register("Power", 40108, 1, DataType.UINT16)
        self.powerL1 = Register("PowerL1", 40109, 1, DataType.UINT16)
        self.powerL2 = Register("PowerL2", 40110, 1, DataType.UINT16)
        self.powerL3 = Register("PowerL3", 40111, 1, DataType.UINT16)
        self.energy = Register("Energy", 40136, 2, DataType.UINT32)
        self.current_snapshot_status = Register("Current Snapshot Status", 40524, 1, DataType.UINT16)
        self.start_snapshot_status = Register("Start Snapshot Status", 41286, 1, DataType.UINT16)
        self.end_snapshot_status = Register("End Snapshot Status", 41540, 1, DataType.UINT16)
        self.current_ocmf = Register("Current OCMF", 41795, 496, DataType.STRING)
        self.start_ocmf = Register("Start OCMF", 43295, 496, DataType.STRING)
        self.end_ocmf = Register("End OCMF", 43795, 496, DataType.STRING)
        self.meta1 = Register("Meta1", 40279, 70, DataType.STRING)
        self.meta2 = Register("Meta2", 40349, 50, DataType.STRING)
        self.meta3 = Register("Meta3", 40399, 50, DataType.STRING)