from abc import ABC, abstractmethod
from definitions import Current, DataType, Description, Energy, Exponent, Power, Register, Voltage, SnapshotStatus
from modbus_controller import ModbusController
import time
from modbus_tk import modbus


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

    @abstractmethod
    def set_max_baud_rate(self):
        raise NotImplementedError

    @abstractmethod
    def get_metrics(self):
        raise NotImplementedError

    @abstractmethod
    def get_snapshot(self):
        raise NotImplementedError

    @abstractmethod
    def get_public_key(self):
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
        Description.VOLTAGE_EXP: Exponent(40105, 1, DataType.INT16),
        Description.CURRENT: Current(40092, 1, DataType.UINT16),
        Description.CURRENT_L1: Current(40093, 1, DataType.UINT16),
        Description.CURRENT_L2: Current(40094, 1, DataType.UINT16),
        Description.CURRENT_L3: Current(40095, 1, DataType.UINT16),
        Description.CURRENT_EXP: Exponent(40096, 1, DataType.INT16),
        Description.POWER: Power(40108, 1, DataType.UINT16),
        Description.POWER_L1: Power(40109, 1, DataType.UINT16),
        Description.POWER_L2: Power(40110, 1, DataType.UINT16),
        Description.POWER_L3: Power(40111, 1, DataType.UINT16),
        Description.POWER_EXP: Exponent(40112, 1, DataType.INT16),
        Description.ENERGY: Energy(40136, 2, DataType.UINT32),
        Description.ENERGY_EXP: Exponent(40144, 1, DataType.INT16),
        Description.CURRENT_SNAPSHOT_STATUS: Register(40524, 1, DataType.UINT16),
        Description.START_SNAPSHOT_STATUS: Register(41286, 1, DataType.UINT16),
        Description.END_SNAPSHOT_STATUS: Register(41540, 1, DataType.UINT16),
        Description.CURRENT_OCMF: Register(41795, 496, DataType.STRING),
        Description.START_OCMF: Register(43295, 496, DataType.STRING),
        Description.END_OCMF: Register(43795, 496, DataType.STRING),
        Description.META_1: Register(40279, 70, DataType.STRING),
        Description.META_2: Register(40349, 50, DataType.STRING),
        Description.META_3: Register(40399, 50, DataType.STRING),
        Description.PUBLIC_KEY: Register(40449, 125, DataType.BLOB)
    }

    def __init__(self) -> None:
        super().__init__()
        self._modbus_controller = ModbusController()
        self._modbus_controller.connect_rtu_client(
            self.PORT, self.MAX_BAUD_RATE, self.BYTESIZE, self.PARITY, self.STOPBITS, self.TIMEOUT)
        try:
            baud = self._modbus_controller.read_reg(
                self.UNIT_ID, self.registers.get(Description.BAUD_RATE))
            print("Baud rate: {}".format(baud))
        except modbus.ModbusInvalidResponseError:
            self.set_max_baud_rate()
        finally:
            self.set_time()
            self.set_meta("BUGRA")

    def metrics_start(self):
        return self.registers.get(Description.CURRENT)

    def metrics_end(self):
        return self.registers.get(Description.ENERGY_EXP)

    def set_max_baud_rate(self):
        self._modbus_controller.client.close()
        self._modbus_controller.connect_rtu_client(
            self.PORT, self.DEFAULT_BAUD_RATE, self.BYTESIZE, self.PARITY, self.STOPBITS, self.TIMEOUT)
        self._modbus_controller.write_reg(self.UNIT_ID, self.registers.get(
            Description.BAUD_RATE), self.MAX_BAUD_RATE)
        self._modbus_controller.client.close()
        self._modbus_controller.connect_rtu_client(
            self.PORT, self.DEFAULT_BAUD_RATE, self.BYTESIZE, self.PARITY, self.STOPBITS, self.TIMEOUT)

    def set_time(self):
        t = int(time.time())
        try:
            tzone = int(time.tzname[0]) * 60
        except:
            tzone = 0
        time_reg = self.registers.get(Description.EPOCH_TIME)
        print("setting time: {} {}".format(time.ctime(t), tzone))
        output = self._modbus_controller._convert_to_uint16(t, time_reg.length)
        output.append(tzone)
        self._modbus_controller.write_multiple(self.UNIT_ID, time_reg, output)

    def get_ocmf(self, reg: Register):
        size = reg.length
        address = reg.address
        result = ""
        while size > 125:
            read_reg = Register(address, 125, reg.data_type)
            result += self._modbus_controller.read_reg(self.UNIT_ID, read_reg)
            size -= 125
            address += 125
        return result.replace("\u0000", "")

    def set_meta(self, data):
        self._modbus_controller.write_reg(
            self.UNIT_ID, self.registers.get(Description.META_1), data)

    def get_metrics(self):
        regs = [
            Description.CURRENT_L1,
            Description.CURRENT_L2,
            Description.CURRENT_L3,
            Description.CURRENT_EXP,
            Description.VOLTAGE_L1,
            Description.VOLTAGE_L2,
            Description.VOLTAGE_L3,
            Description.VOLTAGE_EXP,
            Description.POWER_L1,
            Description.POWER_L2,
            Description.POWER_L3,
            Description.POWER_EXP,
            Description.ENERGY,
            Description.ENERGY_EXP,
        ]
        reg_list = [self.registers.get(x) for x in regs]
        output = self._modbus_controller.read_multiple(
            self.UNIT_ID, reg_list)
        output = dict(zip([desc.value for desc in regs], output))

        current_exp = output[Description.CURRENT_EXP.value]
        voltage_exp = output[Description.VOLTAGE_EXP.value]
        power_exp = output[Description.POWER_EXP.value]
        energy_exp = output[Description.ENERGY_EXP.value]

        del output[Description.CURRENT_EXP.value]
        del output[Description.VOLTAGE_EXP.value]
        del output[Description.POWER_EXP.value]
        del output[Description.ENERGY_EXP.value]

        output[Description.CURRENT_L1.value] = int(output[Description.CURRENT_L1.value] * (10 ** current_exp) * 1000)
        output[Description.CURRENT_L2.value] = int(output[Description.CURRENT_L2.value] * (10 ** current_exp) * 1000)
        output[Description.CURRENT_L3.value] = int(output[Description.CURRENT_L3.value] * (10 ** current_exp) * 1000)

        output[Description.VOLTAGE_L1.value] = int(output[Description.VOLTAGE_L1.value] * (10 ** voltage_exp) * 1000)
        output[Description.VOLTAGE_L2.value] = int(output[Description.VOLTAGE_L2.value] * (10 ** voltage_exp) * 1000)
        output[Description.VOLTAGE_L3.value] = int(output[Description.VOLTAGE_L3.value] * (10 ** voltage_exp) * 1000)

        output[Description.POWER_L1.value] = int(output[Description.POWER_L1.value] * (10 ** power_exp))
        output[Description.POWER_L2.value] = int(output[Description.POWER_L2.value] * (10 ** power_exp))
        output[Description.POWER_L3.value] = int(output[Description.POWER_L3.value] * (10 ** power_exp))

        output[Description.ENERGY.value] = int(output[Description.ENERGY.value] * (10 ** energy_exp))

        return output

    def get_snapshot(self, reg_status: Register, reg_ocmf: Register):
        self._modbus_controller.write_reg(
            self.UNIT_ID, reg_status, SnapshotStatus.UPDATE.value)
        status = self._modbus_controller.read_reg(self.UNIT_ID, reg_status)
        while status == SnapshotStatus.UPDATE.value:
            status = self._modbus_controller.read_reg(self.UNIT_ID, reg_status)
        if status == SnapshotStatus.VALID.value:
            return self.get_ocmf(reg_ocmf)
        else:
            raise Exception("Snapshot failed: {}".format(
                SnapshotStatus(status)))

    def get_public_key(self):
        pk_reg = self.registers.get(Description.PUBLIC_KEY)
        data = self._modbus_controller.read_reg(self.UNIT_ID, pk_reg)
        size = data[0]
        pk = data[2:size+2]
        pk = [hex(i)[2:].zfill(4) for i in pk]
        return "".join(pk).rstrip("0").replace("\u0000", "")
