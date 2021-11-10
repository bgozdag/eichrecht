from component import Component
import zmq
from threading import Thread


class MessageController(Component):

    def __init__(self, mediator) -> None:
        self._mediator = mediator
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.setsockopt_string(zmq.IDENTITY, "EICHRECHT")
        self.socket.connect("ipc:///var/lib/routing.ipc")

    def notify(self, message):
        self._mediator.notify(message, self)

    def receive(self, message):
        self.socket.send_string(message)

    def _listen(self):
        while True:
            data = self.socket.recv_string()
            self.notify(data)

    def listen(self):
        t = Thread(target=self._listen, daemon=True)
        t.start()
