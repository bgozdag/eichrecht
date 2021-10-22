from modbus_tk import modbus_rtu, utils, defines
import serial
from serial.serialutil import PARITY_EVEN, STOPBITS_ONE
from definitions import DataType, Register

logger = utils.create_logger("console")

PORT = "/dev/ttyO2"
DEFAULT_BAUDRATE = 19200
BYTESIZE = 8
UNIT_ID = 44


class ModbusController:
    def __init__(self, max_baud_rate):
        self.client = modbus_rtu.RtuMaster(serial.Serial(
            port=PORT, baudrate=max_baud_rate, bytesize=BYTESIZE, parity=PARITY_EVEN, stopbits=STOPBITS_ONE))
        self.client.set_timeout(5.0)
        self.client.set_verbose(True)
        logger.info("connected")

    def _convert_from_uint16(self, data_type: DataType, data):
        if data_type == DataType.INT16 or data_type == DataType.UINT16:
            return data[0]
        elif data_type == DataType.UINT32:
            return data[0] * 2**8 + data[1]
        elif data_type == DataType.STRING:
            string = ""
            for i in data:
                q, r = divmod(i, 2**8)
                string += chr(q) + chr(r)
            return string
    
    def _convert_to_uint16(self, data):
        result = []
        if type(data) == int:
            if data > 2**16-1:   # if data is uint32
                result.append(data // 2**16)
                result.append(data % 2**16)
            else:   # if data is uint16
                result.append(data)
        elif type(data) == str:
            # TODO
            pass
        return result


    def reset_connection(self):
        self.client.close()
        self.client = modbus_rtu.RtuMaster(serial.Serial(
            port=PORT, baudrate=DEFAULT_BAUDRATE, bytesize=BYTESIZE, parity=PARITY_EVEN, stopbits=STOPBITS_ONE))


    def read(self, reg: Register):
        data = self.client.execute(
            UNIT_ID, defines.READ_HOLDING_REGISTERS, reg.address, reg.length)
        return self._convert_from_uint16(reg.data_type, data)

    def write(self, reg: Register, data):
        self.client.execute(UNIT_ID, defines.WRITE_MULTIPLE_REGISTERS, reg.address, output_value=self._convert_to_uint16(data))
