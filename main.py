from modbus_controller import ModbusController

def main():
    mc = ModbusController()
    print(mc.read(40004, 16))

if __name__ == "__main__":
    main()