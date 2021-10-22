from modbus_controller import ModbusController
from definitions import Bauer
from modbus_controller import logger


class App:
    def __init__(self) -> None:
        self.device = Bauer()
        self.mc = ModbusController()
        logger.info(self.mc.read(self.device.manufacturer))
        logger.info(self.mc.read(self.device.model))
        logger.info(self.mc.read(self.device.options))
        logger.info(self.mc.read(self.device.version))
        logger.info(self.mc.read(self.device.serial_number))
    
    def set_baud_rate(self, target_baud_rate):
        current_baud_rate = self.mc.read(self.device.baud_rate)
        logger.info(current_baud_rate)
        # if current_baud_rate != target_baud_rate:
        #     self.mc.


if __name__ == "__main__":
    app = App()
