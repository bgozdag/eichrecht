from modbus_tk import modbus_rtu, defines, exceptions
import serial
from definitions import DataType, Register


class ModbusController:
    def __del__(self):
        print("closing socket")
        self.client.close()

    def connect_rtu_client(self, port, baudrate, bytesize, parity, stopbits, timeout):
        self.client = modbus_rtu.RtuMaster(serial.Serial(
            port=port, baudrate=baudrate, bytesize=bytesize, parity=parity,
            stopbits=stopbits))
        self.client.set_timeout(timeout)
        print("connected")

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
        elif data_type == DataType.BLOB:
            return data

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

    def read_reg(self, unit_id,  reg: Register):
        data = self.client.execute(
            unit_id, defines.READ_HOLDING_REGISTERS, reg.address, reg.length)
        result = self._convert_from_uint16(reg.data_type, data)
        print("{}: {}".format(reg.address, result))
        return result

    def read_multiple(self, unit_id, reg_start: Register, reg_end: Register):
        return self.client.execute(
            unit_id, defines.READ_HOLDING_REGISTERS, reg_start.address, reg_end.address + reg_end.length - reg_start.address)

    def write_reg(self, unit_id, reg: Register, data):
        try:
            print("Writing '{}' to: {}".format(data, reg.address))
            self.client.execute(unit_id, defines.WRITE_MULTIPLE_REGISTERS,
                                reg.address, output_value=self._convert_to_uint16(data, reg.length))
        except exceptions.ModbusError as e:
            print(e)

    def write_multiple(self, unit_id, reg_start: Register, data):
        try:
            self.client.execute(
                unit_id, defines.WRITE_MULTIPLE_REGISTERS, reg_start.address, output_value=data)
        except exceptions.ModbusError as e:
            print(e)
