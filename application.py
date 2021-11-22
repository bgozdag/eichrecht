from definitions import Description, Register
from device import Bauer
from threading import Thread
from mediator import Mediator
from component import Component
import json
import sqlite3
import sys

VFACTORY_DATABASE = "/run/media/mmcblk1p3/vfactory.db"


class Application(Component):

    def __init__(self, mediator: Mediator) -> None:
        if not self.is_enabled():
            sys.exit("Disabled from vfactory")
        self._mediator = mediator
        self.device = Bauer()

    def notify(self, message):
        self._mediator.notify(message, self)

    def receive(self, message):
        try:
            data = json.loads(message)
            if data["type"] == "ChargeSessionStatus":
                if data["status"] == "Started":
                    self.send_start_snapshot()
                elif data["status"] == "Stopped":
                    self.send_end_snapshot()
            elif data["type"] == "getPublicKey":
                self.device.get_public_key()
            elif data["type"] == "getCurrentSnapshot":
                self.send_current_snapshot()
        except Exception as e:
            print(e)

    def run(self):
        while True:
            metrics = self.device.get_metrics()
            for msg in metrics:
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
                "type": self.device.get_description(reg_ocmf).value,
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

    @staticmethod
    def is_enabled():
        try:
            conn = sqlite3.connect(VFACTORY_DATABASE, timeout=10.0)
            cursor = conn.cursor()
            query = "SELECT meterType FROM deviceDetails WHERE ID=1"
            cursor.execute(query)
            meter_type = cursor.fetchone()
            conn.close()
            if meter_type[0] == "Eichrecht":
                return True
            return False
        except:
            return False
