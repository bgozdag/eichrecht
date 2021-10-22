import time
from modbus_tk import modbus
from modbus_controller import ModbusController
from definitions import Bauer
from modbus_controller import logger


class App:
    def __init__(self) -> None:
        self.device = Bauer()
        self.mc = ModbusController(self.device.MAX_BAUD_RATE)
        try:
            logger.info("Baud rate: {}".format(self.mc.read(self.device.baud_rate)))
        except modbus.ModbusInvalidResponseError as e:
            self.mc.set_baud_rate(self.device.baud_rate, self.device.MAX_BAUD_RATE)
        except Exception as e:
            logger.error(e)
        finally:
            logger.info("Manufacturer: {}".format(self.mc.read(self.device.manufacturer)))
            logger.info("Model: {}".format(self.mc.read(self.device.model)))
            logger.info("Options: {}".format(self.mc.read(self.device.options)))
            logger.info("Version: {}".format(self.mc.read(self.device.version)))
            logger.info("Serial number: {}".format(self.mc.read(self.device.serial_number)))
            self.query_metrics()

    def query_metrics(self):
        while True:
            logger.info("Voltage: {}".format(self.mc.read(self.device.voltage)))
            logger.info("VoltageL1: {}".format(self.mc.read(self.device.voltageL1)))
            logger.info("VoltageL2: {}".format(self.mc.read(self.device.voltageL2)))
            logger.info("VoltageL3: {}".format(self.mc.read(self.device.voltageL3)))
            time.sleep(0.1)


if __name__ == "__main__":
    app = App()
