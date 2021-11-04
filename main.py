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
            logger.info("Manufacturer: {}".format(self.modbus_controller.read(self.device.manufacturer)))
            logger.info("Model: {}".format(self.modbus_controller.read(self.device.model)))
            logger.info("Options: {}".format(self.modbus_controller.read(self.device.options)))
            logger.info("Version: {}".format(self.modbus_controller.read(self.device.version)))
            logger.info("Serial number: {}".format(self.modbus_controller.read(self.device.serial_number)))
            self.modbus_controller.set_time(self.device.epoch_time)
            self.get_snapshot(self.device.snapshot_status)
            self.query_metrics()

    def query_metrics(self):
        while True:
            query = self.modbus_controller.read_in_between(self.device.current, self.device.energy)
            queries = [
                self.device.current,
                self.device.currentL1,
                self.device.currentL2,
                self.device.currentL3,
                self.device.voltageL1,
                self.device.voltageL2,
                self.device.voltageL3,
                self.device.power,
                self.device.powerL1,
                self.device.powerL2,
                self.device.powerL3,
                self.device.energy,
            ]
            query_dict = {}
            start_address = self.device.current.address
            for i in range(len(query)):
                query_dict[start_address + i] = query[i]
            for x in queries:
                logger.info("{}: {}".format(x.name, query_dict[x.address]))

    def get_snapshot(self, reg_status: Register):
        self.modbus_controller.write(self.device.meta1, "VESTEL EVC04")
        status = self.modbus_controller.read(reg_status)
        if status == SnapshotStatus.UPDATE.value:
            logger.info("Update already in progress")
            return
        self.modbus_controller.write(reg_status, SnapshotStatus.UPDATE.value)
        status = self.modbus_controller.read(reg_status)
        while status == SnapshotStatus.UPDATE.value:
            status = self.modbus_controller.read(reg_status)
        if status == SnapshotStatus.VALID.value:
            logger.info("Signature: {}".format(self.modbus_controller.get_ocmf(self.device.ocmf)))
        else:
            logger.error("Snapshot failed: {}".format(SnapshotStatus(status).name))


if __name__ == "__main__":
    app = App()
