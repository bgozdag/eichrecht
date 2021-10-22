from modbus_tk import modbus_rtu, utils, defines
import serial
from serial.serialutil import PARITY_EVEN, STOPBITS_ONE
from definitions import DataType, Register

logger = utils.create_logger("console")

PORT = "/dev/ttyO2"
BAUDRATE = 19200
BYTESIZE = 8
UNIT_ID = 44


class ModbusController:
    def __init__(self):
        self.client = modbus_rtu.RtuMaster(serial.Serial(
            port=PORT, baudrate=BAUDRATE, bytesize=BYTESIZE, parity=PARITY_EVEN, stopbits=STOPBITS_ONE))
        self.client.set_timeout(5.0)
        self.client.set_verbose(True)
        logger.info("connected")

    def _convert_data(self, data_type: DataType, data):
        if data_type == DataType.INT16 or data_type == DataType.UINT16:
            return data[0]
        elif data_type == DataType.UINT32:
            return data[0] * 2**8 + data[1]
        elif data_type == DataType.STRING:
            return "".join([chr(i) for i in data])

    def read(self, reg: Register):
        try:
            data = self.client.execute(
                UNIT_ID, defines.READ_HOLDING_REGISTERS, reg.address, reg.length)
            return self._convert_data(reg.data_type, data)
        except Exception as e:
            logger.exception(e)
