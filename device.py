from abc import ABC, abstractmethod
from definitions import Current, DataType, Description, Energy, Exponent, Power, Register, Voltage


class Device(ABC):

    @property
    @abstractmethod
    def PORT():
        raise NotImplementedError

    @property
    @abstractmethod
    def BYTESIZE():
        raise NotImplementedError

    @property
    @abstractmethod
    def UNIT_ID():
        raise NotImplementedError

    @property
    @abstractmethod
    def TIMEOUT():
        raise NotImplementedError

    @property
    @abstractmethod
    def PARITY():
        raise NotImplementedError

    @property
    @abstractmethod
    def STOPBITS():
        raise NotImplementedError

    @property
    @abstractmethod
    def DEFAULT_BAUD_RATE():
        raise NotImplementedError

    @property
    @abstractmethod
    def MAX_BAUD_RATE():
        raise NotImplementedError

    @property
    @abstractmethod
    def registers():
        raise NotImplementedError

    @abstractmethod
    def metrics_start(self):
        raise NotImplementedError

    @abstractmethod
    def metrics_end(self):
        raise NotImplementedError


class Bauer(Device):
    DEFAULT_BAUD_RATE = 19200
    MAX_BAUD_RATE = 115200
    PORT = "/dev/ttyO2"
    BYTESIZE = 8
    UNIT_ID = 44
    TIMEOUT = 15
    PARITY = 'E'
    STOPBITS = 1
    registers = {
        Description.MANUFACTURER: Register(40004, 16, DataType.STRING),
        Description.MODEL: Register(40020, 16, DataType.STRING),
        Description.OPTIONS: Register(40036, 8, DataType.STRING),
        Description.VERSION: Register(40044, 8, DataType.STRING),
        Description.SERIAL_NUMBER: Register(40052, 16, DataType.STRING),
        Description.BAUD_RATE: Register(40082, 2, DataType.UINT32),
        Description.EPOCH_TIME: Register(40260, 2, DataType.UINT32),
        Description.VOLTAGE_L1: Voltage(40098, 1, DataType.UINT16),
        Description.VOLTAGE_L2: Voltage(40099, 1, DataType.UINT16),
        Description.VOLTAGE_L3: Voltage(40100, 1, DataType.UINT16),
        Description.VOLTAGE_EXP: Exponent(40105, 1, DataType.UINT16),
        Description.CURRENT: Current(40092, 1, DataType.UINT16),
        Description.CURRENT_L1: Current(40093, 1, DataType.UINT16),
        Description.CURRENT_L2: Current(40094, 1, DataType.UINT16),
        Description.CURRENT_L3: Current(40095, 1, DataType.UINT16),
        Description.CURRENT_EXP: Exponent(40096, 1, DataType.UINT16),
        Description.POWER: Power(40108, 1, DataType.UINT16),
        Description.POWER_L1: Power(40109, 1, DataType.UINT16),
        Description.POWER_L2: Power(40110, 1, DataType.UINT16),
        Description.POWER_L3: Power(40111, 1, DataType.UINT16),
        Description.POWER_EXP: Exponent(40112, 1, DataType.UINT16),
        Description.ENERGY: Energy(40136, 2, DataType.UINT32),
        Description.ENERGY_EXP: Exponent(40144, 1, DataType.UINT16),
        Description.CURRENT_SNAPSHOT_STATUS: Register(40524, 1, DataType.UINT16),
        Description.START_SNAPSHOT_STATUS: Register(41286, 1, DataType.UINT16),
        Description.END_SNAPSHOT_STATUS: Register(41540, 1, DataType.UINT16),
        Description.CURRENT_OCMF: Register(41795, 496, DataType.STRING),
        Description.START_OCMF: Register(43295, 496, DataType.STRING),
        Description.END_OCMF: Register(43795, 496, DataType.STRING),
        Description.META_1: Register(40279, 70, DataType.STRING),
        Description.META_2: Register(40349, 50, DataType.STRING),
        Description.META_3: Register(40399, 50, DataType.STRING),
    }

    def metrics_start(self):
        return self.registers.get(Description.CURRENT)

    def metrics_end(self):
        return self.registers.get(Description.ENERGY_EXP)
