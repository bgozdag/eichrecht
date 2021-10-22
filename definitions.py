from abc import ABC, abstractmethod
from enum import Enum

class DataType(Enum):
    """Register data type"""

    INT16 = "int16"
    STRING = "string"
    UINT16 = "uint16"
    UINT32 = "uint32"

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