from definitions import Description, Register
from device import Bauer
from threading import Thread
from mediator import Mediator
from component import Component
import json


class Application(Component):
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator
        self.device = Bauer()

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

    def run(self):
        self.send_public_key()
        while True:
            msg = self.device.get_metrics()
            self.notify(json.dumps(msg))

    def send_public_key(self):
        msg = {
            "type": "publicKey",
            "data": self.device.get_public_key()
        }
        self.notify(json.dumps(msg))

    def send_snapshot(self, reg_status: Register, reg_ocmf: Register):
        try:
            ocmf = self.device.get_snapshot(reg_status, reg_ocmf)
            msg = {
                "type": "OCMF",
                "data": ocmf
            }
            self.notify(json.dumps(msg))
        except Exception as e:
            print(e)

    def send_current_snapshot(self):
        snapshot_t = Thread(target=self.send_snapshot, args=(
            self.device.registers.get(Description.CURRENT_SNAPSHOT_STATUS), self.device.registers.get(Description.CURRENT_OCMF)), daemon=True)
        snapshot_t.start()

    def send_start_snapshot(self):
        snapshot_t = Thread(target=self.send_snapshot, args=(
            self.device.registers.get(Description.START_SNAPSHOT_STATUS), self.device.registers.get(Description.START_OCMF)), daemon=True)
        snapshot_t.start()

    def send_end_snapshot(self):
        snapshot_t = Thread(target=self.send_snapshot, args=(
            self.device.registers.get(Description.END_SNAPSHOT_STATUS), self.device.registers.get(Description.END_OCMF)), daemon=True)
        snapshot_t.start()
