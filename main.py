import time
from modbus_tk import modbus
from modbus_controller import ModbusController
from definitions import Bauer, Register, SnapshotStatus
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
            logger.info("Current Time: {}".format(time.ctime(self.mc.read(self.device.epoch_time))))
            logger.info("Manufacturer: {}".format(self.mc.read(self.device.manufacturer)))
            logger.info("Model: {}".format(self.mc.read(self.device.model)))
            logger.info("Options: {}".format(self.mc.read(self.device.options)))
            logger.info("Version: {}".format(self.mc.read(self.device.version)))
            logger.info("Serial number: {}".format(self.mc.read(self.device.serial_number)))
            self.get_snapshot(self.device.ocmfStatus, self.device.ocmfSignature)
            self.query_metrics()

    def query_metrics(self):
        while True:
            voltage = self.mc.read_in_between(self.device.voltageL1, self.device.voltageL3)
            for i, v in enumerate(voltage):
                logger.info("Voltage{}: {}".format(i, v))
            current = self.mc.read_in_between(self.device.current, self.device.currentL3)
            for i, c in enumerate(current):
                logger.info("Current{}: {}".format(i, c))
            power = self.mc.read_in_between(self.device.power, self.device.powerL3)
            for i, p in enumerate(power):
                logger.info("Power{}: {}".format(i, p))
            logger.info("Energy: {}".format(self.mc.read(self.device.energy)))
    
    def get_snapshot(self, reg_status: Register, reg_signature: Register):
        status = self.mc.read(reg_status)
        if status == SnapshotStatus.UPDATE.value:
            logger.info("Update already in progress")
            return
        self.mc.write(reg_status, SnapshotStatus.UPDATE.value)
        status = self.mc.read(reg_status)
        while status == SnapshotStatus.UPDATE.value:
            status = self.mc.read(reg_status)
        if status == SnapshotStatus.VALID.value:
            logger.info("Signature: {}".format(self.mc.read(reg_signature)))
        else:
            logger.error("Snapshot failed: {}".format(SnapshotStatus(status).name))


if __name__ == "__main__":
    app = App()
