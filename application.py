from definitions import Current, Description, Energy, Power, Register, SnapshotStatus, DataType, Voltage
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
            self.modbus_controller.read_reg(
                self.device.registers.get(Description.BAUD_RATE))
        except modbus.ModbusInvalidResponseError:
            self.modbus_controller.set_baud_rate()
        finally:
            self.modbus_controller.set_time(
                self.device.registers.get(Description.EPOCH_TIME))
            self.modbus_controller.write(
                self.device.registers.get(Description.META_1), "BUGRA")

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
                self.device.metrics_start(), self.device.metrics_end())
            metrics = [
                Description.CURRENT,
                Description.CURRENT_L1,
                Description.CURRENT_L2,
                Description.CURRENT_L3,
                Description.VOLTAGE_L1,
                Description.VOLTAGE_L2,
                Description.VOLTAGE_L3,
                Description.POWER,
                Description.POWER_L1,
                Description.POWER_L2,
                Description.POWER_L3,
                Description.ENERGY,
            ]
            query_dict = {}
            for i in range(len(query)):
                query_dict[self.device.metrics_start().address + i] = int(query[i])
            msg = {
                "type": "metricsEvent",
                "data": []
            }
            for desc in metrics:
                reg = self.device.registers.get(desc)
                if reg.data_type == DataType.UINT32:
                    value = self.modbus_controller._convert_from_uint16(
                        DataType.UINT32, [query_dict[reg.address], query_dict[reg.address + 1]])
                else:
                    value = query_dict[reg.address]
                # if type(reg) is Current:
                #     value *= 10 ** query_dict[self.device.registers.get(Description.CURRENT_EXP).address]
                # elif type(reg) is Voltage:
                #     value *= 10 ** query_dict[self.device.registers.get(Description.VOLTAGE_EXP).address]
                # elif type(reg) is Power:
                #     value *= 10 ** query_dict[self.device.registers.get(Description.POWER_EXP).address]
                # elif type(reg) is Energy:
                #     value *= 10 ** query_dict[self.device.registers.get(Description.ENERGY_EXP).address]
                msg["data"].append(
                    {"{}".format(desc.value): "{}".format(value)})
            logger.debug(msg)

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
            self.device.registers.get(Description.CURRENT_SNAPSHOT_STATUS), self.device.registers.get(Description.CURRENT_OCMF)), daemon=True)
        snapshot_t.start()

    def get_start_snapshot(self):
        snapshot_t = Thread(target=self._get_snapshot, args=(
            self.device.registers.get(Description.START_SNAPSHOT_STATUS), self.device.registers.get(Description.START_OCMF)), daemon=True)
        snapshot_t.start()

    def get_end_snapshot(self):
        snapshot_t = Thread(target=self._get_snapshot, args=(
            self.device.registers.get(Description.END_SNAPSHOT_STATUS), self.device.registers.get(Description.END_OCMF)), daemon=True)
        snapshot_t.start()
