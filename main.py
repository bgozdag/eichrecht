from modbus_tk import modbus
from modbus_controller import ModbusController
from definitions import Bauer
from modbus_controller import logger


class App:
    def __init__(self) -> None:
        self.device = Bauer()
        self.mc = ModbusController(self.device.MAX_BAUD_RATE)
        try:
            logger.info("Manufacturer: {}".format(self.mc.read(self.device.manufacturer)))
            logger.info("Model: {}".format(self.mc.read(self.device.model)))
            logger.info("Options: {}".format(self.mc.read(self.device.options)))
            logger.info("Version: {}".format(self.mc.read(self.device.version)))
            logger.info("Serial number: {}".format(self.mc.read(self.device.serial_number)))
        except modbus.ModbusError as e:
            self.set_baud_rate()
    
    def set_baud_rate(self):
        current_baud_rate = self.mc.read(self.device.baud_rate)
        logger.info("Baud rate: {}".format(current_baud_rate))
        if current_baud_rate != self.device.MAX_BAUD_RATE:
            self.mc.write(self.device.baud_rate, self.device.MAX_BAUD_RATE)
            logger.info("Baud rate set to: self.device.MAX_BAUD_RATE")
            self.mc.reset_connection()


if __name__ == "__main__":
    app = App()
