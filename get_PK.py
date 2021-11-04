from modbus_tk import modbus_rtu, defines
import serial
from serial.serialutil import PARITY_EVEN, STOPBITS_ONE

PORT = "/dev/ttyUSB1"
BAUDRATE = 115200
BYTESIZE = 8
UNIT_ID = 42
TIMEOUT = 15

client = modbus_rtu.RtuMaster(serial.Serial(
    port=PORT, baudrate=BAUDRATE, bytesize=BYTESIZE, parity=PARITY_EVEN, stopbits=STOPBITS_ONE))
client.set_timeout(15)
data = client.execute(
    UNIT_ID, defines.READ_HOLDING_REGISTERS, 40449, 125)
size = data[0]
registers = data[1]
pk = data[2:size+2]
pk = [hex(i)[2:].zfill(4) for i in pk]
print("".join(pk).rstrip("0"))
