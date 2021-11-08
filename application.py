from definitions import Register, SnapshotStatus
from device import Bauer
from threading import Thread
from mediator import Mediator
from modbus_controller import ModbusController
from modbus_tk import modbus
from component import Component
from modbus_controller import logger
import json


class Application(Component):
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator
        self.device = Bauer()
        self.modbus_controller = ModbusController(self.device)
        try:
            self.modbus_controller.read_reg(self.device.baud_rate)
        except modbus.ModbusInvalidResponseError:
            self.modbus_controller.set_baud_rate()
        finally:
            self.modbus_controller.set_time(self.device.epoch_time)
            self.modbus_controller.write(self.device.meta1, "BUGRA")

    def notify(self, message):
        self._mediator.notify(message, self)

    def receive(self, message):
        print("{} received: {}".format(__class__.__name__, message))
        data = json.loads(message)
        if data["type"] == "ChargeSessionStatus":
            if data["status"] == "Started":
                self.get_start_snapshot()
            elif data["status"] == "Stopped":
                self.get_end_snapshot()

    def query_metrics(self):
        while True:
            query = self.modbus_controller.read_in_between(
                self.device.current, self.device.energy)
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
            msg = {
                "type": "metricsEvent",
                "data": []
            }
            for x in queries:
                msg["data"].append(
                    {"{}".format(x.name): "{}".format(query_dict[x.address])})
            self.notify(json.dumps(msg))

    def _get_snapshot(self, reg_status: Register, reg_ocmf: Register):
        self.modbus_controller.write(reg_status, SnapshotStatus.UPDATE.value)
        status = self.modbus_controller.read_reg(reg_status)
        while status == SnapshotStatus.UPDATE.value:
            status = self.modbus_controller.read_reg(reg_status)
        if status == SnapshotStatus.VALID.value:
            ocmf = self.modbus_controller.get_ocmf(reg_ocmf)
            msg = {
                "type": reg_ocmf.name,
                "data": ocmf
            }
            self.notify(json.dumps(msg))
        else:
            logger.error("Snapshot failed: {}".format(
                SnapshotStatus(status).name))

    def get_current_snapshot(self):
        snapshot_t = Thread(target=self._get_snapshot, args=(
            self.device.current_snapshot_status, self.device.current_ocmf), daemon=True)
        snapshot_t.start()

    def get_start_snapshot(self):
        snapshot_t = Thread(target=self._get_snapshot, args=(
            self.device.start_snapshot_status, self.device.start_ocmf), daemon=True)
        snapshot_t.start()

    def get_end_snapshot(self):
        snapshot_t = Thread(target=self._get_snapshot, args=(
            self.device.end_snapshot_status, self.device.end_ocmf), daemon=True)
        snapshot_t.start()
