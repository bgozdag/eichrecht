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


class Description(Enum):
    MANUFACTURER = "manufacturer"
    MODEL = "model"
    OPTIONS = "options"
    VERSION = "version"
    SERIAL_NUMBER = "serialNumber"
    BAUD_RATE = "baudRate"
    EPOCH_TIME = "epochTime"
    VOLTAGE_L1 = "voltageL1"
    VOLTAGE_L2 = "voltageL2"
    VOLTAGE_L3 = "voltageL3"
    VOLTAGE_EXP = "voltageExp"
    CURRENT = "current"
    CURRENT_L1 = "currentL1"
    CURRENT_L2 = "currentL2"
    CURRENT_L3 = "currentL3"
    CURRENT_EXP = "currentExp"
    POWER = "power"
    POWER_L1 = "powerL1"
    POWER_L2 = "powerL2"
    POWER_L3 = "powerL3"
    POWER_EXP = "powerExp"
    ENERGY = "energy"
    ENERGY_EXP = "energyExp"
    CURRENT_SNAPSHOT_STATUS = "currentSnapshotStatus"
    START_SNAPSHOT_STATUS = "startSnapshotStatus"
    END_SNAPSHOT_STATUS = "endSnapshotStatus"
    CURRENT_OCMF = "currentOCMF"
    START_OCMF = "startOCMF"
    END_OCMF = "endOCMF"
    META_1 = "meta1"
    META_2 = "meta2"
    META_3 = "meta3"

class Register:
    """Register base class"""

    def __init__(self, address, length, data_type):
        """Constructor"""
        self.address = address
        self.length = length
        self.data_type = data_type


class Current(Register):
    def __init__(self, address, length, data_type):
        super().__init__(address, length, data_type)


class Voltage(Register):
    def __init__(self, address, length, data_type):
        super().__init__(address, length, data_type)


class Power(Register):
    def __init__(self, address, length, data_type):
        super().__init__(address, length, data_type)


class Energy(Register):
    def __init__(self, address, length, data_type):
        super().__init__(address, length, data_type)


class Exponent(Register):
    def __init__(self, address, length, data_type):
        super().__init__(address, length, data_type)
