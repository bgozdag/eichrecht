import time
from modbus_tk import modbus
from modbus_controller import ModbusController
from definitions import Bauer, Register, SnapshotStatus
from modbus_controller import logger


class App:
    def __init__(self) -> None:
        self.device = Bauer()
        self.modbus_controller = ModbusController(self.device.MAX_BAUD_RATE)
        try:
            logger.info("Baud rate: {}".format(self.modbus_controller.read(self.device.baud_rate)))
        except modbus.ModbusInvalidResponseError:
            self.modbus_controller.set_baud_rate(self.device.baud_rate, self.device.MAX_BAUD_RATE)
        finally:
            self.modbus_controller.set_time(self.device.epoch_time)
            logger.info("Manufacturer: {}".format(self.modbus_controller.read(self.device.manufacturer)))
            logger.info("Model: {}".format(self.modbus_controller.read(self.device.model)))
            logger.info("Options: {}".format(self.modbus_controller.read(self.device.options)))
            logger.info("Version: {}".format(self.modbus_controller.read(self.device.version)))
            logger.info("Serial number: {}".format(self.modbus_controller.read(self.device.serial_number)))
            # self.get_snapshot(self.device.ocmfStatus, self.device.ocmfSignature)
            self.query_metrics()

    def query_metrics(self):
        while True:
            voltage = self.modbus_controller.read_in_between(self.device.voltageL1, self.device.voltageL3)
            for i, v in enumerate(voltage):
                logger.info("Voltage{}: {}".format(i, v))
            current = self.modbus_controller.read_in_between(self.device.current, self.device.currentL3)
            for i, c in enumerate(current):
                logger.info("Current{}: {}".format(i, c))
            power = self.modbus_controller.read_in_between(self.device.power, self.device.powerL3)
            for i, p in enumerate(power):
                logger.info("Power{}: {}".format(i, p))
            logger.info("Energy: {}".format(self.modbus_controller.read(self.device.energy)))
    
    def get_snapshot(self, reg_status: Register, reg_signature: Register):
        status = self.modbus_controller.read(reg_status)
        logger.info("1 snapshot status: {}".format(SnapshotStatus(status)))
        if status == SnapshotStatus.UPDATE.value:
            logger.info("Update already in progress")
            return
        self.modbus_controller.write(reg_status, SnapshotStatus.UPDATE.value)
        status = self.modbus_controller.read(reg_status)
        logger.info("2 snapshot status: {}".format(SnapshotStatus(status)))
        while status == SnapshotStatus.UPDATE.value:
            status = self.modbus_controller.read(reg_status)
        logger.info("3 snapshot status: {}".format(SnapshotStatus(status)))
        if status == SnapshotStatus.VALID.value:
            logger.info("Signature: {}".format(self.modbus_controller.read(reg_signature)))
        else:
            logger.error("Snapshot failed: {}".format(SnapshotStatus(status).name))


if __name__ == "__main__":
    app = App()
