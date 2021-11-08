from component import Component
import zmq


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
