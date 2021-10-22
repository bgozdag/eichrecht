from abc import ABC
from enum import Enum

class DataType(Enum):
    INT16 = "int16"
    STRING = "string"
    UINT16 = "uint16"
    UINT32 = "uint32"

class Register:
    def __init__(self, address, length, data_type):
        self.address = address
        self.length = length
        self.data_type = data_type

class Device(ABC):
    pass

class Bauer(Device):
    def __init__(self) -> None:
        super().__init__()
        self.manufacturer = Register(40004, 16, DataType.STRING)
        self.model = Register(40020, 16, DataType.STRING)
        self.options = Register(40036, 8, DataType.STRING)
        self.baud_rate = Register(40082, 2, DataType.UINT32)