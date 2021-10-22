from modbus_controller import ModbusController
from definitions import Bauer


def main():
    device = Bauer()
    mc = ModbusController()
    print(mc.read(device.baud_rate))


if __name__ == "__main__":
    main()
