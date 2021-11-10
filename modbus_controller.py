import time
from modbus_tk import modbus_rtu, utils, defines, exceptions
import serial
from definitions import DataType, Register
from device import Device

logger = utils.create_logger("console")


class ModbusController:
    def __init__(self, device: Device):
        self._device = device
        self.client = modbus_rtu.RtuMaster(serial.Serial(
            port=self._device.PORT, baudrate=self._device.MAX_BAUD_RATE, bytesize=self._device.BYTESIZE, parity=self._device.PARITY, stopbits=self._device.STOPBITS))
        self.client.set_timeout(self._device.TIMEOUT)
        self.client.set_verbose(True)
        logger.info("connected")

    def __del__(self):
        logger.warning("closing socket")
        self.client.close()

    def _convert_from_uint16(self, data_type: DataType, data):
        if data_type == DataType.INT16 or data_type == DataType.UINT16:
            return data[0]
        elif data_type == DataType.UINT32:
            return data[0] * 2**16 + data[1]
        elif data_type == DataType.STRING:
            string = ""
            for i in data:
                q, r = divmod(i, 2**8)
                string += chr(q) + chr(r)
            return string

    def _convert_to_uint16(self, data, size):
        result = []
        if type(data) == int:
            if data > 2**16-1:   # if data is uint32
                result.append(data // 2**16)
                result.append(data % 2**16)
            else:   # if data is uint16
                result.append(data)
        elif type(data) == str:
            for i in range(len(data)-1):
                if i % 2 == 0:
                    result.append(ord(data[i])*2**8 + ord(data[i+1]))
            if len(data) % 2 != 0:
                result.append(ord(data[-1])*2**8)
        for i in range(size - len(result)):
            result.append(0)
        return result

    def set_baud_rate(self):
        self.client.close()
        self.client = modbus_rtu.RtuMaster(serial.Serial(
            port=self._devicePORT, baudrate=self._device.DEFAULT_BAUDRATE, bytesize=self._device.BYTESIZE, parity=self._device.PARITY_EVEN, stopbits=self._device.STOPBITS_ONE))
        self.client.set_timeout(self._device.TIMEOUT)
        self.write(self._device.baud_rate, self._device.MAX_BAUD_RATE)
        self.client.close()
        self.client = modbus_rtu.RtuMaster(serial.Serial(
            port=self._device.PORT, baudrate=self._device.MAX_BAUD_RATE, bytesize=self._device.BYTESIZE, parity=self._device.PARITY_EVEN, stopbits=self._device.STOPBITS_ONE))
        self.client.set_timeout(self._device.TIMEOUT)

    def read_in_between(self, reg_start: Register, reg_end: Register):
        return self.client.execute(
            self._device.UNIT_ID, defines.READ_HOLDING_REGISTERS, reg_start.address, reg_end.address + reg_end.length - reg_start.address)

    def read_reg(self, reg: Register):
        data = self.client.execute(
            self._device.UNIT_ID, defines.READ_HOLDING_REGISTERS, reg.address, reg.length)
        result = self._convert_from_uint16(reg.data_type, data)
        logger.info("{}: {}".format(reg.address, result))
        return self._convert_from_uint16(reg.data_type, data)

    def write(self, reg: Register, data):
        try:
            logger.info("Writing '{}' to: {}".format(data, reg.address))
            self.client.execute(self._device.UNIT_ID, defines.WRITE_MULTIPLE_REGISTERS,
                                reg.address, output_value=self._convert_to_uint16(data, reg.length))
        except exceptions.ModbusError as e:
            logger.error(e)

    def set_time(self, reg: Register):
        t = int(time.time())
        try:
            tzone = int(time.tzname[0]) * 60
        except:
            tzone = 0
        logger.info("setting time: {} {}".format(time.ctime(t), tzone))
        output = self._convert_to_uint16(t, reg.length)
        output.append(tzone)
        try:
            self.client.execute(
                self._device.UNIT_ID, defines.WRITE_MULTIPLE_REGISTERS, reg.address, output_value=output)
        except exceptions.ModbusError as e:
            logger.error(e)

    def get_ocmf(self, reg: Register):
        size = reg.length
        address = reg.address
        result = ""
        while size > 125:
            data = self.client.execute(
                self._device.UNIT_ID, defines.READ_HOLDING_REGISTERS, address, 125)
            result += self._convert_from_uint16(reg.data_type, data)
            size -= 125
            address += 125
        return result.replace("\u0000", "")
