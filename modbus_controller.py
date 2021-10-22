from modbus_tk import modbus_rtu, utils, defines
import serial
from serial.serialutil import PARITY_EVEN, STOPBITS_ONE

logger = utils.create_logger("console")

PORT = "/dev/ttyO2"
BAUDRATE=115200
BYTESIZE=8
UNIT_ID = 44

class ModbusController:
    def __init__(self):
        self.client = modbus_rtu.RtuMaster(serial.Serial(
            port=PORT, baudrate=BAUDRATE, bytesize=BYTESIZE, parity=PARITY_EVEN, stopbits=STOPBITS_ONE))
        self.client.set_timeout(5.0)
        self.client.set_verbose(True)
        logger.info("connected")

    def read(self, addr, length):
        return self.client.execute(UNIT_ID, defines.READ_HOLDING_REGISTERS, addr, length)
