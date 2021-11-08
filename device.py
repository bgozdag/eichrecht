from abc import ABC
from definitions import DataType, Register


class Device(ABC):

    @property
    def PORT(self):
        raise NotImplementedError

    @property
    def BYTESIZE(self):
        raise NotImplementedError

    @property
    def UNIT_ID(self):
        raise NotImplementedError

    @property
    def TIMEOUT(self):
        raise NotImplementedError

    @property
    def PARITY(self):
        raise NotImplementedError

    @property
    def STOPBITS(self):
        raise NotImplementedError

    @property
    def DEFAULT_BAUD_RATE(self):
        raise NotImplementedError

    @property
    def MAX_BAUD_RATE(self):
        raise NotImplementedError

    @property
    def manufacturer(self):
        raise NotImplementedError

    @property
    def model(self):
        raise NotImplementedError

    @property
    def options(self):
        raise NotImplementedError

    @property
    def version(self):
        raise NotImplementedError

    @property
    def serial_number(self):
        raise NotImplementedError

    @property
    def baud_rate(self):
        raise NotImplementedError

    @property
    def epoch_time(self):
        raise NotImplementedError

    @property
    def voltageL1(self):
        raise NotImplementedError

    @property
    def voltageL2(self):
        raise NotImplementedError

    @property
    def voltageL3(self):
        raise NotImplementedError

    @property
    def current(self):
        raise NotImplementedError

    @property
    def currentL1(self):
        raise NotImplementedError

    @property
    def currentL2(self):
        raise NotImplementedError

    @property
    def currentL3(self):
        raise NotImplementedError

    @property
    def power(self):
        raise NotImplementedError

    @property
    def powerL1(self):
        raise NotImplementedError

    @property
    def powerL2(self):
        raise NotImplementedError

    @property
    def powerL3(self):
        raise NotImplementedError

    @property
    def energy(self):
        raise NotImplementedError

    @property
    def current_snapshot_status(self):
        raise NotImplementedError

    @property
    def start_snapshot_status(self):
        raise NotImplementedError

    @property
    def end_snapshot_status(self):
        raise NotImplementedError

    @property
    def current_ocmf(self):
        raise NotImplementedError

    @property
    def start_ocmf(self):
        raise NotImplementedError

    @property
    def end_ocmf(self):
        raise NotImplementedError

    @property
    def meta1(self):
        raise NotImplementedError

    @property
    def meta2(self):
        raise NotImplementedError

    @property
    def meta3(self):
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
    manufacturer = Register("Manufacturer", 40004, 16, DataType.STRING)
    model = Register("Model", 40020, 16, DataType.STRING)
    options = Register("Options", 40036, 8, DataType.STRING)
    version = Register("Version", 40044, 8, DataType.STRING)
    serial_number = Register("Serial Number", 40052, 16, DataType.STRING)
    baud_rate = Register("Baud Rate", 40082, 2, DataType.UINT32)
    epoch_time = Register("Epoch Time", 40260, 2, DataType.UINT32)
    voltageL1 = Register("VoltageL1", 40098, 1, DataType.UINT16)
    voltageL2 = Register("VoltageL2", 40099, 1, DataType.UINT16)
    voltageL3 = Register("VoltageL3", 40100, 1, DataType.UINT16)
    current = Register("Current", 40092, 1, DataType.UINT16)
    currentL1 = Register("CurrentL1", 40093, 1, DataType.UINT16)
    currentL2 = Register("CurrentL2", 40094, 1, DataType.UINT16)
    currentL3 = Register("CurrentL3", 40095, 1, DataType.UINT16)
    power = Register("Power", 40108, 1, DataType.UINT16)
    powerL1 = Register("PowerL1", 40109, 1, DataType.UINT16)
    powerL2 = Register("PowerL2", 40110, 1, DataType.UINT16)
    powerL3 = Register("PowerL3", 40111, 1, DataType.UINT16)
    energy = Register("Energy", 40136, 2, DataType.UINT32)
    current_snapshot_status = Register(
        "Current Snapshot Status", 40524, 1, DataType.UINT16)
    start_snapshot_status = Register(
        "Start Snapshot Status", 41286, 1, DataType.UINT16)
    end_snapshot_status = Register(
        "End Snapshot Status", 41540, 1, DataType.UINT16)
    current_ocmf = Register("currentOCMF", 41795, 496, DataType.STRING)
    start_ocmf = Register("startOCMF", 43295, 496, DataType.STRING)
    end_ocmf = Register("endOCMF", 43795, 496, DataType.STRING)
    meta1 = Register("Meta1", 40279, 70, DataType.STRING)
    meta2 = Register("Meta2", 40349, 50, DataType.STRING)
    meta3 = Register("Meta3", 40399, 50, DataType.STRING)
